# # -*- coding: utf-8 -*-
# import numpy as np


# def all_transformation_list(pent):
#     ret = []
#     cur_block = np.copy(pent)
#     for _ in range(4):
#         cur_block = np.rot90(cur_block)
#         ret.append(cur_block)
#     cur_block = np.flip(cur_block, 0)
#     for _ in range(4):
#         cur_block = np.rot90(cur_block)
#         ret.append(cur_block)

#     # get rid of duplication
#     no_dup = []
#     for item in ret:
#         dup_flag = False
#         for no_dup_item in no_dup:
#             if np.array_equal(no_dup_item, item):
#                 dup_flag = True
#                 break
#         if not dup_flag:
#             no_dup.append(item)

#     return no_dup


# def all_positions(board, pent):
#     """ Find all positions to place the pentominoes. """
#     ret = []
#     info = []
#     for cur in all_transformation_list(pent):
#         rows, cols = cur.shape
#         for i in range(board.shape[0] - rows + 1):
#             for j in range(board.shape[1] - cols + 1):
#                 cur_board = np.copy(board)
#                 fail = 0
#                 for x in range(rows):
#                     if fail == 1:
#                         break
#                     for y in range(cols):
#                         if cur[x][y] != 0 and cur_board[i+x][j+y] == 1:
#                             fail = 1
#                             break
#                         cur_board[i+x][j+y] = cur[x][y]
#                 if fail == 0:
#                     ret.append(cur_board)
#                     info.append((cur, i, j))
#     return ret, info


# def exact_cover(matrix):
#     return exact_cover_helper(matrix, [], list(range(matrix.shape[0])))


# def exact_cover_helper(A, partial, original_r):
#     row, col = A.shape
#     if col == 0:
#         return partial
#     else:
#         c = A.sum(axis=0).argmin()
#         if A.sum(axis=0)[c] == 0:
#             return None
#         partial_temp = partial
#         for r in range(row):
#             B = A
#             if B[r][c] != 1:
#                 continue
#             r_index = original_r[r]
#             partial_temp.append(r_index)
#             col_temp = []
#             row_temp = []
#             for j in range(col):
#                 if B[r][j] != 1:
#                     continue
#                 col_temp.append(j)
#                 for i in range(row):
#                     if B[i][j] == 1:
#                         if i not in row_temp:
#                             row_temp.append(i)
#             # Delete each row i such that A[i,j] = 1
#             # then delete column j.
#             B = np.delete(B, row_temp, axis=0)
#             B = np.delete(B, col_temp, axis=1)
#             new_index = [x for x in list(range(row)) if x not in row_temp]
#             new_r = [original_r[x] for x in new_index]
#             answer = exact_cover_helper(B, partial_temp, new_r)
#             if answer != None:
#                 return answer
#             partial_temp.remove(r_index)


# def solve(board, pents):
#     """
#     This is the function you will implement. It will take in a numpy array of the board
#     as well as a list of n tiles in the form of numpy arrays. The solution returned
#     is of the form [(p1, (row1, col1))...(pn,  (rown, coln))]
#     where pi is a tile (may be rotated or flipped), and (rowi, coli) is 
#     the coordinate of the upper left corner of pi in the board (lowest row and column index 
#     that the tile covers).
#     -Use np.flip and np.rot90 to manipulate pentominos.
#     -You can assume there will always be a solution.
#     """
#     board = 1 - board
#     # print(board)
#     flat_board = board.ravel()
#     list_to_delete = np.where(flat_board == 1)
#     list_to_delete = [x + len(pents) for x in list_to_delete]

#     matrix = []
#     info_matrix = []
#     for i in range(len(pents)):
#         all_pos_list, all_pos_info = all_positions(board, pents[i])
#         for item in all_pos_list:
#             item = np.append(np.zeros(len(pents)), item)
#             item = np.delete(item, list_to_delete)
#             item[i] = 1
#             matrix.append(item)
#         info_matrix.extend(all_pos_info)

#     # matrix is the big 2000 * 72 for exact cover algorithm X
#     matrix = np.array(matrix)
#     # print("matrix row numbers:", len(matrix))

#     matrix[matrix > 0] = 1
#     result_list = exact_cover(matrix)

#     return_val = []
#     for i in result_list:
#         info = info_matrix[i]
#         # print(info)
#         return_val.append((info[0], (info[1], info[2])))
#     return return_val


# ==============================================================================2=============================================================================================
# ============================================================================================================================================================================
# ============================================================================================================================================================================
# ============================================================================================================================================================================
# ============================================================================================================================================================================
# ============================================================================================================================================================================
# ============================================================================================================================================================================
# ===========================================================================UTTT============================================================================================



from time import sleep
from math import inf
from random import randint
import time


class ultimateTicTacToe:
    def __init__(self):
        """
        Initialization of the game.
        """
        self.board = [['_', '_', '_', '_', '_', '_', '_', '_', '_'],
                      ['_', '_', '_', '_', '_', '_', '_', '_', '_'],
                      ['_', '_', '_', '_', '_', '_', '_', '_', '_'],
                      ['_', '_', '_', '_', '_', '_', '_', '_', '_'],
                      ['_', '_', '_', '_', '_', '_', '_', '_', '_'],
                      ['_', '_', '_', '_', '_', '_', '_', '_', '_'],
                      ['_', '_', '_', '_', '_', '_', '_', '_', '_'],
                      ['_', '_', '_', '_', '_', '_', '_', '_', '_'],
                      ['_', '_', '_', '_', '_', '_', '_', '_', '_']]
        self.maxPlayer = 'X'
        self.minPlayer = 'O'
        self.maxDepth = 3
        # The start indexes of each local board
        self.globalIdx = [(0, 0), (0, 3), (0, 6), (3, 0), (3, 3), (3, 6), (6, 0), (6, 3), (6, 6)]

        # Start local board index for reflex agent playing
        self.startBoardIdx = 4
        #self.startBoardIdx = randint(0, 8)

        # utility value for reflex offensive and reflex defensive agents
        self.winnerMaxUtility = 10000
        self.twoInARowMaxUtility = 500
        self.preventThreeInARowMaxUtility = 100
        self.cornerMaxUtility = 30

        self.winnerMinUtility = -10000
        self.twoInARowMinUtility = -100
        self.preventThreeInARowMinUtility = -500
        self.cornerMinUtility = -30

        self.expandedNodes = 0
        self.currPlayer = True

    def getNextBoardIdx(self, i, j):
        return (i % 3) * 3 + j % 3

    def printGameBoard(self):
        """
        This function prints the current game board.
        """
        print('\n'.join([' '.join([str(cell) for cell in row])
                         for row in self.board[:3]])+'\n')
        print('\n'.join([' '.join([str(cell) for cell in row])
                         for row in self.board[3:6]])+'\n')
        print('\n'.join([' '.join([str(cell) for cell in row])
                         for row in self.board[6:9]])+'\n')

    def evaluatePredifined(self, isMax):
        """
        This function implements the evaluation function for ultimate tic tac toe for predifined agent.
        input args:
        isMax(bool): boolean variable indicates whether it's maxPlayer or minPlayer.
                     True for maxPlayer, False for minPlayer
        output:
        score(float): estimated utility score for maxPlayer or minPlayer
        """
        # YOUR CODE HERE
        if self.checkWinner() == 1 and isMax:
            return 10000
        elif self.checkWinner() == -1 and not isMax:
            return -10000

        score = 0

        counter_500 = 0
        counter_100 = 0
        for i in range(9):
            row, col = self.globalIdx[i]

            cur_player = ''
            opponent_player = ''
            if isMax:
                cur_player = self.maxPlayer
                opponent_player = self.minPlayer
            else:
                cur_player = self.minPlayer
                opponent_player = self.maxPlayer
            # 500
            # ROW
            if self.board[row][col] == self.board[row][col+1] == cur_player and self.board[row][col+2] == '_':
                counter_500 += 1
            elif self.board[row][col+1] == self.board[row][col+2] == cur_player and self.board[row][col] == '_':
                counter_500 += 1
            elif self.board[row][col] == self.board[row][col+2] == cur_player and self.board[row][col+1] == '_':
                counter_500 += 1

            if self.board[row+1][col] == self.board[row+1][col+1] == cur_player and self.board[row+1][col+2] == '_':
                counter_500 += 1
            elif self.board[row+1][col+1] == self.board[row+1][col+2] == cur_player and self.board[row+1][col] == '_':
                counter_500 += 1
            elif self.board[row+1][col] == self.board[row+1][col+2] == cur_player and self.board[row+1][col+1] == '_':
                counter_500 += 1

            if self.board[row+2][col] == self.board[row+2][col+1] == cur_player and self.board[row+2][col+2] == '_':
                counter_500 += 1
            elif self.board[row+2][col+1] == self.board[row+2][col+2] == cur_player and self.board[row+2][col] == '_':
                counter_500 += 1
            elif self.board[row+2][col] == self.board[row+2][col+2] == cur_player and self.board[row+2][col+1] == '_':
                counter_500 += 1
            # COL
            if self.board[row][col] == self.board[row+1][col] == cur_player and self.board[row+2][col] == '_':
                counter_500 += 1
            elif self.board[row+1][col] == self.board[row+2][col] == cur_player and self.board[row][col] == '_':
                counter_500 += 1
            elif self.board[row][col] == self.board[row+2][col] == cur_player and self.board[row+1][col] == '_':
                counter_500 += 1

            if self.board[row][col+1] == self.board[row+1][col+1] == cur_player and self.board[row+2][col+1] == '_':
                counter_500 += 1
            elif self.board[row+1][col+1] == self.board[row+2][col+1] == cur_player and self.board[row][col+1] == '_':
                counter_500 += 1
            elif self.board[row][col+1] == self.board[row+2][col+1] == cur_player and self.board[row+1][col+1] == '_':
                counter_500 += 1

            if self.board[row][col+2] == self.board[row+1][col+2] == cur_player and self.board[row+2][col+2] == '_':
                counter_500 += 1
            elif self.board[row+1][col+2] == self.board[row+2][col+2] == cur_player and self.board[row][col+2] == '_':
                counter_500 += 1
            elif self.board[row][col+2] == self.board[row+2][col+2] == cur_player and self.board[row+1][col+2] == '_':
                counter_500 += 1
            # DIA
            if self.board[row][col] == self.board[row+1][col+1] == cur_player and self.board[row+2][col+2] == '_':
                counter_500 += 1
            elif self.board[row+2][col+2] == self.board[row+1][col+1] == cur_player and self.board[row][col] == '_':
                counter_500 += 1
            elif self.board[row+2][col+2] == self.board[row][col] == cur_player and self.board[row+1][col+1] == '_':
                counter_500 += 1

            if self.board[row][col+2] == self.board[row+1][col+1] == cur_player and self.board[row+2][col] == '_':
                counter_500 += 1
            elif self.board[row][col+2] == self.board[row+2][col] == cur_player and self.board[row+1][col+1] == '_':
                counter_500 += 1
            elif self.board[row+1][col+1] == self.board[row+2][col] == cur_player and self.board[row][col+2] == '_':
                counter_500 += 1
            # 100
            # ROW
            if self.board[row][col] == self.board[row][col+1] == opponent_player and self.board[row][col+2] == cur_player:
                counter_100 += 1
            elif self.board[row][col+1] == self.board[row][col+2] == opponent_player and self.board[row][col] == cur_player:
                counter_100 += 1
            elif self.board[row][col] == self.board[row][col+2] == opponent_player and self.board[row][col+1] == cur_player:
                counter_100 += 1

            if self.board[row+1][col] == self.board[row+1][col+1] == opponent_player and self.board[row+1][col+2] == cur_player:
                counter_100 += 1
            elif self.board[row+1][col+1] == self.board[row+1][col+2] == opponent_player and self.board[row+1][col] == cur_player:
                counter_100 += 1
            elif self.board[row+1][col] == self.board[row+1][col+2] == opponent_player and self.board[row+1][col+1] == cur_player:
                counter_100 += 1

            if self.board[row+2][col] == self.board[row+2][col+1] == opponent_player and self.board[row+2][col+2] == cur_player:
                counter_100 += 1
            elif self.board[row+2][col+1] == self.board[row+2][col+2] == opponent_player and self.board[row+2][col] == cur_player:
                counter_100 += 1
            elif self.board[row+2][col] == self.board[row+2][col+2] == opponent_player and self.board[row+2][col+1] == cur_player:
                counter_100 += 1

            # COL
            if self.board[row][col] == self.board[row+1][col] == opponent_player and self.board[row+2][col] == cur_player:
                counter_100 += 1
            elif self.board[row+1][col] == self.board[row+2][col] == opponent_player and self.board[row][col] == cur_player:
                counter_100 += 1
            elif self.board[row][col] == self.board[row+2][col] == opponent_player and self.board[row+1][col] == cur_player:
                counter_100 += 1

            if self.board[row][col+1] == self.board[row+1][col+1] == opponent_player and self.board[row+2][col+1] == cur_player:
                counter_100 += 1
            elif self.board[row+1][col+1] == self.board[row+2][col+1] == opponent_player and self.board[row][col+1] == cur_player:
                counter_100 += 1
            elif self.board[row][col+1] == self.board[row+2][col+1] == opponent_player and self.board[row+1][col+1] == cur_player:
                counter_100 += 1

            if self.board[row][col+2] == self.board[row+1][col+2] == opponent_player and self.board[row+2][col+2] == cur_player:
                counter_100 += 1
            elif self.board[row+1][col+2] == self.board[row+2][col+2] == opponent_player and self.board[row][col+2] == cur_player:
                counter_100 += 1
            elif self.board[row][col+2] == self.board[row+2][col+2] == opponent_player and self.board[row+1][col+2] == cur_player:
                counter_100 += 1
            # DIA
            if self.board[row][col] == self.board[row+1][col+1] == opponent_player and self.board[row+2][col+2] == cur_player:
                counter_100 += 1
            elif self.board[row+2][col+2] == self.board[row+1][col+1] == opponent_player and self.board[row][col] == cur_player:
                counter_100 += 1
            elif self.board[row+2][col+2] == self.board[row][col] == opponent_player and self.board[row+1][col+1] == cur_player:
                counter_100 += 1

            if self.board[row][col+2] == self.board[row+1][col+1] == opponent_player and self.board[row+2][col] == cur_player:
                counter_100 += 1
            elif self.board[row][col+2] == self.board[row+2][col] == opponent_player and self.board[row+1][col+1] == cur_player:
                counter_100 += 1
            elif self.board[row+1][col+1] == self.board[row+2][col] == opponent_player and self.board[row][col+2] == cur_player:
                counter_100 += 1

        if isMax:
            score = score + 500 * counter_500 + 100 * counter_100
        else:
            score = score - (100 * counter_500 + 500 * counter_100)

        if score == 0:
            for i in range(9):
                row, col = self.globalIdx[i]
                for y, x in [(row, col), (row+2, col), (row, col+2), (row+2, col+2)]:
                    if self.board[y][x] == self.maxPlayer and isMax:
                        score += 30
                    elif self.board[y][x] == self.minPlayer and not isMax:
                        score -= 30
        return score

    def evaluateDesigned(self, isMax):
        """
        This function implements the evaluation function for ultimate tic tac toe for your own agent.
        input args:
        isMax(bool): boolean variable indicates whether it's maxPlayer or minPlayer.
                     True for maxPlayer, False for minPlayer
        output:
        score(float): estimated utility score for maxPlayer or minPlayer
        """
        # YOUR CODE HERE
        if self.checkWinner() == 1:
            return 10000
        elif self.checkWinner() == -1:
            return -10000

        score = 0

        counter_500 = 0
        counter_100 = 0
        for i in range(9):
            row, col = self.globalIdx[i]

            cur_player = ''
            opponent_player = ''
            if isMax:
                cur_player = self.maxPlayer
                opponent_player = self.minPlayer
            else:
                cur_player = self.minPlayer
                opponent_player = self.maxPlayer
            # 500
            # ROW
            if self.board[row][col] == self.board[row][col+1] == cur_player and self.board[row][col+2] == '_':
                counter_500 += 1
            elif self.board[row][col+1] == self.board[row][col+2] == cur_player and self.board[row][col] == '_':
                counter_500 += 1
            elif self.board[row][col] == self.board[row][col+2] == cur_player and self.board[row][col+1] == '_':
                counter_500 += 1

            if self.board[row+1][col] == self.board[row+1][col+1] == cur_player and self.board[row+1][col+2] == '_':
                counter_500 += 1
            elif self.board[row+1][col+1] == self.board[row+1][col+2] == cur_player and self.board[row+1][col] == '_':
                counter_500 += 1
            elif self.board[row+1][col] == self.board[row+1][col+2] == cur_player and self.board[row+1][col+1] == '_':
                counter_500 += 1

            if self.board[row+2][col] == self.board[row+2][col+1] == cur_player and self.board[row+2][col+2] == '_':
                counter_500 += 1
            elif self.board[row+2][col+1] == self.board[row+2][col+2] == cur_player and self.board[row+2][col] == '_':
                counter_500 += 1
            elif self.board[row+2][col] == self.board[row+2][col+2] == cur_player and self.board[row+2][col+1] == '_':
                counter_500 += 1
            # COL
            if self.board[row][col] == self.board[row+1][col] == cur_player and self.board[row+2][col] == '_':
                counter_500 += 1
            elif self.board[row+1][col] == self.board[row+2][col] == cur_player and self.board[row][col] == '_':
                counter_500 += 1
            elif self.board[row][col] == self.board[row+2][col] == cur_player and self.board[row+1][col] == '_':
                counter_500 += 1

            if self.board[row][col+1] == self.board[row+1][col+1] == cur_player and self.board[row+2][col+1] == '_':
                counter_500 += 1
            elif self.board[row+1][col+1] == self.board[row+2][col+1] == cur_player and self.board[row][col+1] == '_':
                counter_500 += 1
            elif self.board[row][col+1] == self.board[row+2][col+1] == cur_player and self.board[row+1][col+1] == '_':
                counter_500 += 1

            if self.board[row][col+2] == self.board[row+1][col+2] == cur_player and self.board[row+2][col+2] == '_':
                counter_500 += 1
            elif self.board[row+1][col+2] == self.board[row+2][col+2] == cur_player and self.board[row][col+2] == '_':
                counter_500 += 1
            elif self.board[row][col+2] == self.board[row+2][col+2] == cur_player and self.board[row+1][col+2] == '_':
                counter_500 += 1
            # DIA
            if self.board[row][col] == self.board[row+1][col+1] == cur_player and self.board[row+2][col+2] == '_':
                counter_500 += 1
            elif self.board[row+2][col+2] == self.board[row+1][col+1] == cur_player and self.board[row][col] == '_':
                counter_500 += 1
            elif self.board[row+2][col+2] == self.board[row][col] == cur_player and self.board[row+1][col+1] == '_':
                counter_500 += 1

            if self.board[row][col+2] == self.board[row+1][col+1] == cur_player and self.board[row+2][col] == '_':
                counter_500 += 1
            elif self.board[row][col+2] == self.board[row+2][col] == cur_player and self.board[row+1][col+1] == '_':
                counter_500 += 1
            elif self.board[row+1][col+1] == self.board[row+2][col] == cur_player and self.board[row][col+2] == '_':
                counter_500 += 1
            # 100
            # ROW
            if self.board[row][col] == self.board[row][col+1] == opponent_player and self.board[row][col+2] == cur_player:
                counter_100 += 1
            elif self.board[row][col+1] == self.board[row][col+2] == opponent_player and self.board[row][col] == cur_player:
                counter_100 += 1
            elif self.board[row][col] == self.board[row][col+2] == opponent_player and self.board[row][col+1] == cur_player:
                counter_100 += 1

            if self.board[row+1][col] == self.board[row+1][col+1] == opponent_player and self.board[row+1][col+2] == cur_player:
                counter_100 += 1
            elif self.board[row+1][col+1] == self.board[row+1][col+2] == opponent_player and self.board[row+1][col] == cur_player:
                counter_100 += 1
            elif self.board[row+1][col] == self.board[row+1][col+2] == opponent_player and self.board[row+1][col+1] == cur_player:
                counter_100 += 1

            if self.board[row+2][col] == self.board[row+2][col+1] == opponent_player and self.board[row+2][col+2] == cur_player:
                counter_100 += 1
            elif self.board[row+2][col+1] == self.board[row+2][col+2] == opponent_player and self.board[row+2][col] == cur_player:
                counter_100 += 1
            elif self.board[row+2][col] == self.board[row+2][col+2] == opponent_player and self.board[row+2][col+1] == cur_player:
                counter_100 += 1

            # COL
            if self.board[row][col] == self.board[row+1][col] == opponent_player and self.board[row+2][col] == cur_player:
                counter_100 += 1
            elif self.board[row+1][col] == self.board[row+2][col] == opponent_player and self.board[row][col] == cur_player:
                counter_100 += 1
            elif self.board[row][col] == self.board[row+2][col] == opponent_player and self.board[row+1][col] == cur_player:
                counter_100 += 1

            if self.board[row][col+1] == self.board[row+1][col+1] == opponent_player and self.board[row+2][col+1] == cur_player:
                counter_100 += 1
            elif self.board[row+1][col+1] == self.board[row+2][col+1] == opponent_player and self.board[row][col+1] == cur_player:
                counter_100 += 1
            elif self.board[row][col+1] == self.board[row+2][col+1] == opponent_player and self.board[row+1][col+1] == cur_player:
                counter_100 += 1

            if self.board[row][col+2] == self.board[row+1][col+2] == opponent_player and self.board[row+2][col+2] == cur_player:
                counter_100 += 1
            elif self.board[row+1][col+2] == self.board[row+2][col+2] == opponent_player and self.board[row][col+2] == cur_player:
                counter_100 += 1
            elif self.board[row][col+2] == self.board[row+2][col+2] == opponent_player and self.board[row+1][col+2] == cur_player:
                counter_100 += 1
            # DIA
            if self.board[row][col] == self.board[row+1][col+1] == opponent_player and self.board[row+2][col+2] == cur_player:
                counter_100 += 1
            elif self.board[row+2][col+2] == self.board[row+1][col+1] == opponent_player and self.board[row][col] == cur_player:
                counter_100 += 1
            elif self.board[row+2][col+2] == self.board[row][col] == opponent_player and self.board[row+1][col+1] == cur_player:
                counter_100 += 1

            if self.board[row][col+2] == self.board[row+1][col+1] == opponent_player and self.board[row+2][col] == cur_player:
                counter_100 += 1
            elif self.board[row][col+2] == self.board[row+2][col] == opponent_player and self.board[row+1][col+1] == cur_player:
                counter_100 += 1
            elif self.board[row+1][col+1] == self.board[row+2][col] == opponent_player and self.board[row][col+2] == cur_player:
                counter_100 += 1

        if isMax:
            score = score + 500 * counter_500 + 100 * counter_100
        else:
            score = score - (100 * counter_500 + 500 * counter_100)

        for i in range(9):
            row, col = self.globalIdx[i]
            for y, x in [(row, col), (row+2, col), (row, col+2), (row+2, col+2)]:
                if self.board[y][x] == self.maxPlayer:
                    score += 30
                elif self.board[y][x] == self.minPlayer:
                    score -= 30
        return score

    def checkMovesLeft(self):
        """
        This function checks whether any legal move remains on the board.
        output:
        movesLeft(bool): boolean variable indicates whether any legal move remains
                        on the board.
        """
        # YOUR CODE HERE
        movesLeft = False
        if any('_' in sublist for sublist in self.board):
            movesLeft = True
        return movesLeft

    def checkWinner(self):
        # Return termimnal node status for maximizer player 1-win,0-tie,-1-lose
        """
        This function checks whether there is a winner on the board.
        output:
        winner(int): Return 0 if there is no winner.
                     Return 1 if maxPlayer is the winner.
                     Return -1 if miniPlayer is the winner.
        """
        # YOUR CODE HERE
        win_symbol = ''
        for i in range(9):
            row, col = self.globalIdx[i]
            if self.board[row][col] == self.board[row+1][col] == self.board[row+2][col] != '_':
                win_symbol = self.board[row][col]
            elif self.board[row][col+1] == self.board[row+1][col+1] == self.board[row+2][col+1] != '_':
                win_symbol = self.board[row][col+1]
            elif self.board[row][col+2] == self.board[row+1][col+2] == self.board[row+2][col+2] != '_':
                win_symbol = self.board[row][col+2]
            elif self.board[row][col] == self.board[row][col+1] == self.board[row][col+2] != '_':
                win_symbol = self.board[row][col]
            elif self.board[row+1][col] == self.board[row+1][col+1] == self.board[row+1][col+2] != '_':
                win_symbol = self.board[row+1][col]
            elif self.board[row+2][col] == self.board[row+2][col+1] == self.board[row+2][col+2] != '_':
                win_symbol = self.board[row+2][col]
            elif self.board[row][col] == self.board[row+1][col+1] == self.board[row+2][col+2] != '_':
                win_symbol = self.board[row][col]
            elif self.board[row][col+2] == self.board[row+1][col+1] == self.board[row+2][col] != '_':
                win_symbol = self.board[row][col+2]
            if win_symbol == 'X':
                return 1
            elif win_symbol == 'O':
                return -1
        return 0

    def alphabeta(self, depth, currBoardIdx, alpha, beta, isMax):
        """
        This function implements alpha-beta algorithm for ultimate tic-tac-toe game.
        input args:
        depth(int): current depth level
        currBoardIdx(int): current local board index
        alpha(float): alpha value
        beta(float): beta value
        isMax(bool):boolean variable indicates whether it's maxPlayer or minPlayer.
                     True for maxPlayer, False for minPlayer
        output:
        best_value(float):the best_value that current player may have
        """
        # YOUR CODE HERE
        if (depth == self.maxDepth) or (not self.checkMovesLeft()) or (self.checkWinner() != 0):
            self.expandedNodes += 1
            return self.evaluatePredifined(self.currPlayer)

        if isMax:
            # max from child
            best_value = -inf
            y, x = self.globalIdx[currBoardIdx]
            for j in range(3):
                for i in range(3):
                    if self.board[y+j][x+i] == '_':
                        self.board[y+j][x+i] = self.maxPlayer
                        cur_value = self.alphabeta(depth+1, self.getNextBoardIdx(y+j, x+i), alpha, beta, not isMax)
                        self.board[y+j][x+i] = '_'
                        best_value = max(best_value, cur_value)
                        alpha = max(alpha, best_value)
                        if beta <= alpha:
                            return best_value
            return best_value
        else:
            # min from child
            best_value = inf
            y, x = self.globalIdx[currBoardIdx]
            for j in range(3):
                for i in range(3):
                    if self.board[y+j][x+i] == '_':
                        self.board[y+j][x+i] = self.minPlayer
                        cur_value = self.alphabeta(depth+1, self.getNextBoardIdx(y+j, x+i), alpha, beta, not isMax)
                        self.board[y+j][x+i] = '_'
                        best_value = min(best_value, cur_value)
                        beta = min(beta, best_value)
                        if beta <= alpha:
                            return best_value
            return best_value

    def minimax(self, depth, currBoardIdx, isMax):
        """
        This function implements minimax algorithm for ultimate tic-tac-toe game.
        input args:
        depth(int): current depth level
        currBoardIdx(int): current local board index
        alpha(float): alpha value
        beta(float): beta value
        isMax(bool):boolean variable indicates whether it's maxPlayer or minPlayer.
                     True for maxPlayer, False for minPlayer
        output:
        bestValue(float):the bestValue that current player may have
        """
        # YOUR CODE HERE
        if (depth == self.maxDepth) or (not self.checkMovesLeft()) or (self.checkWinner() != 0):
            self.expandedNodes += 1
            return self.evaluatePredifined(self.currPlayer)

        if isMax:
            # max from child
            best_value = -inf
            y, x = self.globalIdx[currBoardIdx]
            for j in range(3):
                for i in range(3):
                    if self.board[y+j][x+i] == '_':
                        self.board[y+j][x+i] = self.maxPlayer
                        cur_value = self.minimax(depth+1, self.getNextBoardIdx(y+j, x+i), not isMax)
                        self.board[y+j][x+i] = '_'
                        best_value = max(best_value, cur_value)
            return best_value
        else:
            # min from child
            best_value = inf
            y, x = self.globalIdx[currBoardIdx]
            for j in range(3):
                for i in range(3):
                    if self.board[y+j][x+i] == '_':
                        self.board[y+j][x+i] = self.minPlayer
                        cur_value = self.minimax(depth+1, self.getNextBoardIdx(y+j, x+i), not isMax)
                        self.board[y+j][x+i] = '_'
                        best_value = min(best_value, cur_value)
            return best_value

    def playGamePredifinedAgent(self, maxFirst, isMinimaxOffensive, isMinimaxDefensive):
        """
        This function implements the processes of the game of predifined offensive agent vs defensive agent.
        input args:
        maxFirst(bool): boolean variable indicates whether maxPlayer or minPlayer plays first.
                        True for maxPlayer plays first, and False for minPlayer plays first.
        isMinimaxOffensive(bool):boolean variable indicates whether it's using minimax or alpha-beta pruning algorithm for offensive agent.
                        True is minimax and False is alpha-beta.
        isMinimaxOffensive(bool):boolean variable indicates whether it's using minimax or alpha-beta pruning algorithm for defensive agent.
                        True is minimax and False is alpha-beta.
        output:
        bestMove(list of tuple): list of bestMove coordinates at each step
        bestValue(list of float): list of bestValue at each move
        expandedNodes(list of int): list of expanded nodes at each move
        gameBoards(list of 2d lists): list of game board positions at each move
        winner(int): 1 for maxPlayer is the winner, -1 for minPlayer is the winner, and 0 for tie.
        """
        # YOUR CODE HERE
        cur_player = maxFirst
        cur_board = self.startBoardIdx
        self.expandedNodes = 0
        bestMove = []
        bestValue = []
        gameBoards = []
        expandedNodes = []

        alpha = -inf
        beta = inf
        while self.checkMovesLeft() and self.checkWinner() == 0:
            if cur_player:
                self.currPlayer = True
                y, x = self.globalIdx[cur_board]
                best_coord = (-1, -1)
                best_value = -inf
                for j in range(3):
                    for i in range(3):
                        if self.board[y+j][x+i] == '_':
                            self.board[y+j][x+i] = self.maxPlayer
                            cur_board = self.getNextBoardIdx(y+j, x+i)
                            if isMinimaxOffensive:
                                cur_value = self.minimax(1, cur_board, not cur_player)
                            else:
                                cur_value = self.alphabeta(1, cur_board, alpha, beta, not cur_player)
                            self.board[y+j][x+i] = '_'
                            if cur_value > best_value:
                                best_coord = (y+j, x+i)
                                best_value = cur_value
                self.board[best_coord[0]][best_coord[1]] = self.maxPlayer
                cur_board = self.getNextBoardIdx(best_coord[0], best_coord[1])
                bestMove.append(best_coord)
                bestValue.append(best_value)
                gameBoards.append(self.board)
                expandedNodes.append(self.expandedNodes)
                self.printGameBoard()
                cur_player = not cur_player
            else:
                self.currPlayer = False
                y, x = self.globalIdx[cur_board]
                best_coord = (-1, -1)
                best_value = inf
                for j in range(3):
                    for i in range(3):
                        if self.board[y+j][x+i] == '_':
                            self.board[y+j][x+i] = self.minPlayer
                            cur_board = self.getNextBoardIdx(y+j, x+i)
                            if isMinimaxDefensive:
                                cur_value = self.minimax(1, cur_board, not cur_player)
                            else:
                                cur_value = self.alphabeta(1, cur_board, alpha, beta, not cur_player)
                            self.board[y+j][x+i] = '_'
                            if cur_value < best_value:
                                best_coord = (y+j, x+i)
                                best_value = cur_value
                self.board[best_coord[0]][best_coord[1]] = self.minPlayer
                cur_board = self.getNextBoardIdx(best_coord[0], best_coord[1])
                bestMove.append(best_coord)
                bestValue.append(best_value)
                gameBoards.append(self.board)
                expandedNodes.append(self.expandedNodes)
                self.printGameBoard()
                cur_player = not cur_player

        winner = self.checkWinner()
        return gameBoards, bestMove, expandedNodes, bestValue, winner

    def my_minimax(self, depth, currBoardIdx, isMax):
        """
        This function implements minimax algorithm for ultimate tic-tac-toe game.
        input args:
        depth(int): current depth level
        currBoardIdx(int): current local board index
        alpha(float): alpha value
        beta(float): beta value
        isMax(bool):boolean variable indicates whether it's maxPlayer or minPlayer.
                     True for maxPlayer, False for minPlayer
        output:
        bestValue(float):the bestValue that current player may have
        """
        # YOUR CODE HERE
        if (depth == self.maxDepth) or (not self.checkMovesLeft()) or (self.checkWinner() != 0):
            self.expandedNodes += 1
            return self.evaluateDesigned(self.currPlayer)

        if isMax:
            # max from child
            best_value = -inf
            y, x = self.globalIdx[currBoardIdx]
            for j in range(3):
                for i in range(3):
                    if self.board[y+j][x+i] == '_':
                        self.board[y+j][x+i] = self.maxPlayer
                        cur_value = self.my_minimax(depth+1, self.getNextBoardIdx(y+j, x+i), not isMax)
                        self.board[y+j][x+i] = '_'
                        best_value = max(best_value, cur_value)
            return best_value
        else:
            # min from child
            best_value = inf
            y, x = self.globalIdx[currBoardIdx]
            for j in range(3):
                for i in range(3):
                    if self.board[y+j][x+i] == '_':
                        self.board[y+j][x+i] = self.minPlayer
                        cur_value = self.my_minimax(depth+1, self.getNextBoardIdx(y+j, x+i), not isMax)
                        self.board[y+j][x+i] = '_'
                        best_value = min(best_value, cur_value)
            return best_value

    def playGameYourAgent(self):
        """
        This function implements the processes of the game of your own agent vs predifined offensive agent.
        input args:
        output:
        best_coord(list of tuple): list of best_coord coordinates at each step
        gameBoards(list of 2d lists): list of game board positions at each move
        winner(int): 1 for maxPlayer is the winner, -1 for minPlayer is the winner, and 0 for tie.
        """
        # YOUR CODE HERE
        cur_player = True  # true max first, false min first
        cur_board = self.startBoardIdx
        self.expandedNodes = 0
        bestMove = []
        bestValue = []
        gameBoards = []
        expandedNodes = []
        alpha = -inf
        beta = inf

        while self.checkMovesLeft() and self.checkWinner() == 0:
            if cur_player:
                self.currPlayer = True
                y, x = self.globalIdx[cur_board]
                best_coord = (-1, -1)
                best_value = -inf
                for j in range(3):
                    for i in range(3):
                        if self.board[y+j][x+i] == '_':
                            self.board[y+j][x+i] = self.maxPlayer
                            cur_board = self.getNextBoardIdx(y+j, x+i)
                            cur_value = self.alphabeta(1, cur_board, alpha, beta, not cur_player)
                            self.board[y+j][x+i] = '_'
                            if cur_value > best_value:
                                best_coord = (y+j, x+i)
                                best_value = cur_value
                self.board[best_coord[0]][best_coord[1]] = self.maxPlayer
                cur_board = self.getNextBoardIdx(best_coord[0], best_coord[1])
                bestMove.append(best_coord)
                bestValue.append(best_value)
                gameBoards.append(self.board)
                expandedNodes.append(self.expandedNodes)
                self.printGameBoard()
                cur_player = not cur_player
            else:
                self.currPlayer = False
                y, x = self.globalIdx[cur_board]
                best_coord = (-1, -1)
                best_value = inf
                for j in range(3):
                    for i in range(3):
                        if self.board[y+j][x+i] == '_':
                            self.board[y+j][x+i] = self.minPlayer
                            cur_board = self.getNextBoardIdx(y+j, x+i)
                            cur_value = self.my_minimax(1, cur_board, not cur_player)
                            self.board[y+j][x+i] = '_'
                            if cur_value < best_value:
                                best_coord = (y+j, x+i)
                                best_value = cur_value
                self.board[best_coord[0]][best_coord[1]] = self.minPlayer
                cur_board = self.getNextBoardIdx(best_coord[0], best_coord[1])
                bestMove.append(best_coord)
                bestValue.append(best_value)
                gameBoards.append(self.board)
                expandedNodes.append(self.expandedNodes)
                self.printGameBoard()
                cur_player = not cur_player

        winner = self.checkWinner()
        return gameBoards, bestMove, expandedNodes, bestValue, winner

    def playGameHuman(self):
        """
        This function implements the processes of the game of your own agent vs a human.
        output:
        best_coord(list of tuple): list of best_coord coordinates at each step
        gameBoards(list of 2d lists): list of game board positions at each move
        winner(int): 1 for maxPlayer is the winner, -1 for minPlayer is the winner, and 0 for tie.
        """
        # YOUR CODE HERE
        cur_player = True  # true max first, false min first
        cur_board = self.startBoardIdx
        self.expandedNodes = 0
        bestMove = []
        bestValue = []
        gameBoards = []
        expandedNodes = []

        while self.checkMovesLeft() and self.checkWinner() == 0:
            if cur_player:
                self.currPlayer = True
                y, x = self.globalIdx[cur_board]
                best_coord = (-1, -1)
                best_value = -inf
                for j in range(3):
                    for i in range(3):
                        if self.board[y+j][x+i] == '_':
                            self.board[y+j][x+i] = self.maxPlayer
                            cur_board = self.getNextBoardIdx(y+j, x+i)
                            cur_value = self.my_minimax(1, cur_board, not cur_player)
                            self.board[y+j][x+i] = '_'
                            if cur_value > best_value:
                                best_coord = (y+j, x+i)
                                best_value = cur_value
                self.board[best_coord[0]][best_coord[1]] = self.maxPlayer
                cur_board = self.getNextBoardIdx(best_coord[0], best_coord[1])
                bestMove.append(best_coord)
                bestValue.append(best_value)
                gameBoards.append(self.board)
                expandedNodes.append(self.expandedNodes)
                self.printGameBoard()
                cur_player = not cur_player
            else:
                self.currPlayer = False
                y, x = self.globalIdx[cur_board]

                print("put in board:", cur_board)
                x = input('x:')
                y = input('y:')
                put_y = self.globalIdx[cur_board][0] + int(y)
                put_x = self.globalIdx[cur_board][1] + int(x)
                self.board[put_y][put_x] = self.maxPlayer
                cur_board = self.getNextBoardIdx(put_x, put_y)

                self.board[put_y][put_x] = self.minPlayer
                cur_board = self.getNextBoardIdx(put_y, put_x)
                gameBoards.append(self.board)
                self.printGameBoard()
                cur_player = not cur_player

        winner = self.checkWinner()
        return gameBoards, bestMove, expandedNodes, bestValue, winner

    def ec_checkWinner(self):
        counter_x = counter_y = 0
        win_symbol = ''
        coor = (-1, -1)
        for i in range(9):
            row, col = self.globalIdx[i]
            if self.board[row][col] == self.board[row+1][col] == self.board[row+2][col] != '_':
                win_symbol = self.board[row][col]
                coor = (row, col)
            elif self.board[row][col+1] == self.board[row+1][col+1] == self.board[row+2][col+1] != '_':
                win_symbol = self.board[row][col+1]
                coor = (row, col+1)
            elif self.board[row][col+2] == self.board[row+1][col+2] == self.board[row+2][col+2] != '_':
                win_symbol = self.board[row][col+2]
                coor = (row, col+2)
            elif self.board[row][col] == self.board[row][col+1] == self.board[row][col+2] != '_':
                win_symbol = self.board[row][col]
                coor = (row, col)
            elif self.board[row+1][col] == self.board[row+1][col+1] == self.board[row+1][col+2] != '_':
                win_symbol = self.board[row+1][col]
                coor = (row+1, col)
            elif self.board[row+2][col] == self.board[row+2][col+1] == self.board[row+2][col+2] != '_':
                win_symbol = self.board[row+2][col]
                coor = (row+2, col)
            elif self.board[row][col] == self.board[row+1][col+1] == self.board[row+2][col+2] != '_':
                win_symbol = self.board[row][col]
                coor = (row, col)
            elif self.board[row][col+2] == self.board[row+1][col+1] == self.board[row+2][col] != '_':
                win_symbol = self.board[row][col+2]
                coor = (row, col+2)
            if win_symbol == 'X':
                counter_x += 1
                i = coor[0]
                j = coor[1]
                idxx=0
                if (i >= 0 and i < 3 and j >= 0 and j < 3):
                    idxx = 0
                elif (i >= 0 and i < 3 and j >= 3 and j < 6):
                    idxx = 1
                elif (i >= 0 and i < 3 and j >= 6 and j < 9):
                    idxx = 2
                elif (i >= 3 and i < 6 and j >= 0 and j < 3):
                    idxx = 3
                elif (i >= 3 and i < 6 and j >= 3 and j < 6):
                    idxx = 4
                elif (i >= 3 and i < 6 and j >= 6 and j < 9):
                    idxx = 5
                elif (i >= 6 and i < 9 and j >= 0 and j < 3):
                    idxx = 6
                elif (i >= 6 and i < 9 and j >= 3 and j < 6):
                    idxx = 7
                elif (i >= 6 and i < 9 and j >= 6 and j < 9):
                    idxx = 8
                cd = self.globalIdx[idxx]
                for j in range(3):
                    for i in range(3):
                        if self.board[cd[0]+j][cd[1]+i] == '_':
                            self.board[cd[0]+j][cd[1]+i] = 'A'
            elif win_symbol == 'O':
                counter_y += 1
                i = coor[0]
                j = coor[1]
                idxx=0
                if (i >= 0 and i < 3 and j >= 0 and j < 3):
                    idxx = 0
                elif (i >= 0 and i < 3 and j >= 3 and j < 6):
                    idxx = 1
                elif (i >= 0 and i < 3 and j >= 6 and j < 9):
                    idxx = 2
                elif (i >= 3 and i < 6 and j >= 0 and j < 3):
                    idxx = 3
                elif (i >= 3 and i < 6 and j >= 3 and j < 6):
                    idxx = 4
                elif (i >= 3 and i < 6 and j >= 6 and j < 9):
                    idxx = 5
                elif (i >= 6 and i < 9 and j >= 0 and j < 3):
                    idxx = 6
                elif (i >= 6 and i < 9 and j >= 3 and j < 6):
                    idxx = 7
                elif (i >= 6 and i < 9 and j >= 6 and j < 9):
                    idxx = 8
                cd = self.globalIdx[idxx]
                for j in range(3):
                    for i in range(3):
                        if self.board[cd[0]+j][cd[1]+i] == '_':
                            self.board[cd[0]+j][cd[1]+i] = 'A'
        if counter_x == 3:
            return 1
        elif counter_y == 3:
            return -1
        return 0


    def ec_evaluateDesigned(self, isMax):
        score = 0
        counter_500 = 0
        counter_100 = 0
        for i in range(9):
            row, col = self.globalIdx[i]

            cur_player = ''
            opponent_player = ''
            if isMax:
                cur_player = self.maxPlayer
                opponent_player = self.minPlayer
            else:
                cur_player = self.minPlayer
                opponent_player = self.maxPlayer
            # 500
            # ROW
            if self.board[row][col] == self.board[row][col+1] == cur_player and self.board[row][col+2] == '_':
                counter_500 += 1
            elif self.board[row][col+1] == self.board[row][col+2] == cur_player and self.board[row][col] == '_':
                counter_500 += 1
            elif self.board[row][col] == self.board[row][col+2] == cur_player and self.board[row][col+1] == '_':
                counter_500 += 1

            if self.board[row+1][col] == self.board[row+1][col+1] == cur_player and self.board[row+1][col+2] == '_':
                counter_500 += 1
            elif self.board[row+1][col+1] == self.board[row+1][col+2] == cur_player and self.board[row+1][col] == '_':
                counter_500 += 1
            elif self.board[row+1][col] == self.board[row+1][col+2] == cur_player and self.board[row+1][col+1] == '_':
                counter_500 += 1

            if self.board[row+2][col] == self.board[row+2][col+1] == cur_player and self.board[row+2][col+2] == '_':
                counter_500 += 1
            elif self.board[row+2][col+1] == self.board[row+2][col+2] == cur_player and self.board[row+2][col] == '_':
                counter_500 += 1
            elif self.board[row+2][col] == self.board[row+2][col+2] == cur_player and self.board[row+2][col+1] == '_':
                counter_500 += 1
            # COL
            if self.board[row][col] == self.board[row+1][col] == cur_player and self.board[row+2][col] == '_':
                counter_500 += 1
            elif self.board[row+1][col] == self.board[row+2][col] == cur_player and self.board[row][col] == '_':
                counter_500 += 1
            elif self.board[row][col] == self.board[row+2][col] == cur_player and self.board[row+1][col] == '_':
                counter_500 += 1

            if self.board[row][col+1] == self.board[row+1][col+1] == cur_player and self.board[row+2][col+1] == '_':
                counter_500 += 1
            elif self.board[row+1][col+1] == self.board[row+2][col+1] == cur_player and self.board[row][col+1] == '_':
                counter_500 += 1
            elif self.board[row][col+1] == self.board[row+2][col+1] == cur_player and self.board[row+1][col+1] == '_':
                counter_500 += 1

            if self.board[row][col+2] == self.board[row+1][col+2] == cur_player and self.board[row+2][col+2] == '_':
                counter_500 += 1
            elif self.board[row+1][col+2] == self.board[row+2][col+2] == cur_player and self.board[row][col+2] == '_':
                counter_500 += 1
            elif self.board[row][col+2] == self.board[row+2][col+2] == cur_player and self.board[row+1][col+2] == '_':
                counter_500 += 1
            # DIA
            if self.board[row][col] == self.board[row+1][col+1] == cur_player and self.board[row+2][col+2] == '_':
                counter_500 += 1
            elif self.board[row+2][col+2] == self.board[row+1][col+1] == cur_player and self.board[row][col] == '_':
                counter_500 += 1
            elif self.board[row+2][col+2] == self.board[row][col] == cur_player and self.board[row+1][col+1] == '_':
                counter_500 += 1

            if self.board[row][col+2] == self.board[row+1][col+1] == cur_player and self.board[row+2][col] == '_':
                counter_500 += 1
            elif self.board[row][col+2] == self.board[row+2][col] == cur_player and self.board[row+1][col+1] == '_':
                counter_500 += 1
            elif self.board[row+1][col+1] == self.board[row+2][col] == cur_player and self.board[row][col+2] == '_':
                counter_500 += 1
            # 100
            # ROW
            if self.board[row][col] == self.board[row][col+1] == opponent_player and self.board[row][col+2] == cur_player:
                counter_100 += 1
            elif self.board[row][col+1] == self.board[row][col+2] == opponent_player and self.board[row][col] == cur_player:
                counter_100 += 1
            elif self.board[row][col] == self.board[row][col+2] == opponent_player and self.board[row][col+1] == cur_player:
                counter_100 += 1

            if self.board[row+1][col] == self.board[row+1][col+1] == opponent_player and self.board[row+1][col+2] == cur_player:
                counter_100 += 1
            elif self.board[row+1][col+1] == self.board[row+1][col+2] == opponent_player and self.board[row+1][col] == cur_player:
                counter_100 += 1
            elif self.board[row+1][col] == self.board[row+1][col+2] == opponent_player and self.board[row+1][col+1] == cur_player:
                counter_100 += 1

            if self.board[row+2][col] == self.board[row+2][col+1] == opponent_player and self.board[row+2][col+2] == cur_player:
                counter_100 += 1
            elif self.board[row+2][col+1] == self.board[row+2][col+2] == opponent_player and self.board[row+2][col] == cur_player:
                counter_100 += 1
            elif self.board[row+2][col] == self.board[row+2][col+2] == opponent_player and self.board[row+2][col+1] == cur_player:
                counter_100 += 1

            # COL
            if self.board[row][col] == self.board[row+1][col] == opponent_player and self.board[row+2][col] == cur_player:
                counter_100 += 1
            elif self.board[row+1][col] == self.board[row+2][col] == opponent_player and self.board[row][col] == cur_player:
                counter_100 += 1
            elif self.board[row][col] == self.board[row+2][col] == opponent_player and self.board[row+1][col] == cur_player:
                counter_100 += 1

            if self.board[row][col+1] == self.board[row+1][col+1] == opponent_player and self.board[row+2][col+1] == cur_player:
                counter_100 += 1
            elif self.board[row+1][col+1] == self.board[row+2][col+1] == opponent_player and self.board[row][col+1] == cur_player:
                counter_100 += 1
            elif self.board[row][col+1] == self.board[row+2][col+1] == opponent_player and self.board[row+1][col+1] == cur_player:
                counter_100 += 1

            if self.board[row][col+2] == self.board[row+1][col+2] == opponent_player and self.board[row+2][col+2] == cur_player:
                counter_100 += 1
            elif self.board[row+1][col+2] == self.board[row+2][col+2] == opponent_player and self.board[row][col+2] == cur_player:
                counter_100 += 1
            elif self.board[row][col+2] == self.board[row+2][col+2] == opponent_player and self.board[row+1][col+2] == cur_player:
                counter_100 += 1
            # DIA
            if self.board[row][col] == self.board[row+1][col+1] == opponent_player and self.board[row+2][col+2] == cur_player:
                counter_100 += 1
            elif self.board[row+2][col+2] == self.board[row+1][col+1] == opponent_player and self.board[row][col] == cur_player:
                counter_100 += 1
            elif self.board[row+2][col+2] == self.board[row][col] == opponent_player and self.board[row+1][col+1] == cur_player:
                counter_100 += 1

            if self.board[row][col+2] == self.board[row+1][col+1] == opponent_player and self.board[row+2][col] == cur_player:
                counter_100 += 1
            elif self.board[row][col+2] == self.board[row+2][col] == opponent_player and self.board[row+1][col+1] == cur_player:
                counter_100 += 1
            elif self.board[row+1][col+1] == self.board[row+2][col] == opponent_player and self.board[row][col+2] == cur_player:
                counter_100 += 1

        if isMax:
            score = score + 500 * counter_500 + 100 * counter_100
        else:
            score = score - (100 * counter_500 + 500 * counter_100)

        for i in range(9):
            row, col = self.globalIdx[i]
            for y, x in [(row, col), (row+2, col), (row, col+2), (row+2, col+2)]:
                if self.board[y][x] == self.maxPlayer:
                    score += 30
                elif self.board[y][x] == self.minPlayer:
                    score -= 30
        return score

    def my_minimax1(self, depth, currBoardIdx, isMax):
        if (depth == self.maxDepth) or (not self.checkMovesLeft()):
            self.expandedNodes += 1
            return self.ec_evaluateDesigned(self.currPlayer)

        if isMax:
            # max from child
            best_value = -inf
            y, x = self.globalIdx[currBoardIdx]
            for j in range(3):
                for i in range(3):
                    if self.board[y+j][x+i] == '_':
                        self.board[y+j][x+i] = self.maxPlayer
                        cur_value = self.my_minimax(depth+1, self.getNextBoardIdx(y+j, x+i), not isMax)
                        self.board[y+j][x+i] = '_'
                        best_value = max(best_value, cur_value)
            return best_value
        else:
            # min from child
            best_value = inf
            y, x = self.globalIdx[currBoardIdx]
            for j in range(3):
                for i in range(3):
                    if self.board[y+j][x+i] == '_':
                        self.board[y+j][x+i] = self.minPlayer
                        cur_value = self.my_minimax(depth+1, self.getNextBoardIdx(y+j, x+i), not isMax)
                        self.board[y+j][x+i] = '_'
                        best_value = min(best_value, cur_value)
            return best_value

    def ec_playGame(self):
        cur_player = True # true max first, false min first
        cur_board = self.startBoardIdx
        self.expandedNodes = 0
        bestMove = []
        bestValue = []
        gameBoards = []
        expandedNodes = []

        while self.checkMovesLeft():
            if self.ec_checkWinner() != 0:
                break
            if cur_player:
                self.currPlayer = True
                y, x = self.globalIdx[cur_board]
                best_coord = (-1, -1)
                best_value = -inf
                for j in range(3):
                    for i in range(3):
                        if self.board[y+j][x+i] == '_':
                            self.board[y+j][x+i] = self.maxPlayer
                            cur_board = self.getNextBoardIdx(y+j, x+i)
                            cur_value = self.my_minimax(1, cur_board, not cur_player)
                            self.board[y+j][x+i] = '_'
                            if cur_value > best_value:
                                best_coord = (y+j, x+i)
                                best_value = cur_value
                self.board[best_coord[0]][best_coord[1]] = self.maxPlayer
                cur_board = self.getNextBoardIdx(best_coord[0], best_coord[1])
                bestMove.append(best_coord)
                bestValue.append(best_value)
                gameBoards.append(self.board)
                expandedNodes.append(self.expandedNodes)
                self.printGameBoard()
                cur_player = not cur_player
                if self.ec_checkWinner() != 0 or not self.checkMovesLeft():
                    break
            else:
                self.currPlayer = False
                y, x = self.globalIdx[cur_board]
                best_coord = (-1, -1)
                best_value = inf
                for j in range(3):
                    for i in range(3):
                        if self.board[y+j][x+i] == '_':
                            self.board[y+j][x+i] = self.minPlayer
                            cur_board = self.getNextBoardIdx(y+j, x+i)
                            cur_value = self.my_minimax1(1, cur_board, not cur_player)
                            self.board[y+j][x+i] = '_'
                            if cur_value < best_value:
                                best_coord = (y+j, x+i)
                                best_value = cur_value
                self.board[best_coord[0]][best_coord[1]] = self.minPlayer
                cur_board = self.getNextBoardIdx(best_coord[0], best_coord[1])
                bestMove.append(best_coord)
                bestValue.append(best_value)
                gameBoards.append(self.board)
                expandedNodes.append(self.expandedNodes)
                self.printGameBoard()
                cur_player = not cur_player
                if self.ec_checkWinner() != 0 or not self.checkMovesLeft():
                    break

        winner = self.ec_checkWinner()
        return gameBoards, bestMove, expandedNodes, bestValue, winner
if __name__ == "__main__":
    uttt = ultimateTicTacToe()

    start = time.time()
    gameBoards, best_coord, expandedNodes, best_value, winner = uttt.playGamePredifinedAgent(True, True, True)


    #gameBoards, best_coord, expandedNodes, best_value, winner = uttt.playGameYourAgent()

    #gameBoards, best_coord, expandedNodes, best_value, winner = uttt.playGameHuman()
    #gameBoards, best_coord, expandedNodes, best_value, winner = uttt.ec_playGame()
    print(expandedNodes)
    print(best_value)
    
    print("time spent: ", time.time() - start)


    if winner == 1:
        print("The winner is maxPlayer!!!")
    elif winner == -1:
        print("The winner is minPlayer!!!")
    else:
        print("Tie. No winner:(")