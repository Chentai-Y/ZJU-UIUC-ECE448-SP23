# -*- coding: utf-8 -*-
import numpy as np

def trans_without_dup(mino):
    cur_mino = np.copy(mino)
    trans_list = []

    # record all transformattions 
    trans_list.append(cur_mino)
    
    trans_list.append(np.flip(cur_mino, 0))
    trans_list.append(np.flip(cur_mino, 1))
    for _ in range(3):
        cur_mino = np.rot90(cur_mino)
        trans_list.append(cur_mino)
        trans_list.append(np.flip(cur_mino, 0))
        trans_list.append(np.flip(cur_mino, 1))

    # get rid of duplication
    trans_list_no_dup = []
    trans_list_no_dup.append(trans_list[0])
    for mino in trans_list:
        # print("transformed:", mino)
        for no_dup_mino in trans_list_no_dup:
            
            if np.array_equal(mino, no_dup_mino):
                break
            elif len(trans_list_no_dup) == 0:
                trans_list_no_dup.append(mino)
            #elif no_dup_mino.all() == trans_list_no_dup[-1].all():
            elif np.array_equal(no_dup_mino, trans_list_no_dup[-1]):
                trans_list_no_dup.append(mino)
    
    return trans_list_no_dup

def place_available(mino, i, j, board):
    # to judge if this mino can place at this position of the board, i & j are the x & y coordinate of upper left block of mino
    # if the mino can be placed here, return 1 and the tiled board, otherwise return 0 and initial board
    rol, col = mino.shape
    initial_board = board
    ava_flag = 1
    for x in range(rol):
        if ava_flag == 0:
            break
        for y in range(col):
            if mino[x][y] != 0 and board[x+i][y+j] == 1:
                ava_flag = 0
                break
            else:
                board[x+i][y+j] = mino[x][y]

    if ava_flag == 1:
        return 1, board
    else: 
        return 0, initial_board
    

def all_assignments(mino, board):
    board_list = []
    tiling_info = []
    board_row, board_col = board.shape
    all_mino_list = trans_without_dup(mino)
    for item in all_mino_list:
        mino_row, mino_col = item.shape
        for i in range(board_row - mino_row +1):
            for j in range(board_col - mino_col +1):
                cur_board = np.copy(board)
                flag, placed_board = place_available(item, i, j, cur_board)
                
                if flag == 1:
                    board_list.append(placed_board)
                    tiling_info.append((item, i, j))
                elif flag == 0:
                    continue
    return board_list, tiling_info


def algorithm_X(matrix, partial, initial_r):
    # baseed on Donald Knuth's X Algorithm for solving exact cover problem, find out the exact cover partial
    # Algorithm X solves exact cover problem recursive, nondeterministic, depth-first, backtracking
    row, col = matrix.shape
    if col == 0: # if no matrix left, recursion is done 
        return partial
    else:
        least_space_col = matrix.sum(axis = 0).argmin()
        if matrix.sum(axis = 0)[least_space_col] == 0: # this branch cannot work, go back to upper level and choose another path
            return None
        cur_partial = partial
        for x in range(row):
            if matrix[x][least_space_col] == 0:
                continue
            else:
                cur_matrix = matrix
                selected_row_index = initial_r[x]
                cur_partial.append(selected_row_index)
                cur_row = []
                cur_col = []
                for j in range(col):
                    if cur_matrix[x][j] != 1:
                        continue
                    cur_col.append(j)
                    for i in range(row):
                        if cur_matrix[i][j] == 1 and i not in cur_row:
                            cur_row.append(i)

                cur_matrix = np.delete(cur_matrix, cur_row, axis=0)
                cur_matrix = np.delete(cur_matrix, cur_col, axis=1)
                new_r = [] # rows left after deleting, using original index
                for index in range(row):
                    if index not in cur_row:
                        new_r.append(initial_r[index])

                path = algorithm_X(cur_matrix, cur_partial, new_r)

                if path != None:
                    return path 
                else:
                    cur_partial.remove(selected_row_index)

                


def solve(board, pents):
    """
    This is the function you will implement. It will take in a numpy array of the board
    as well as a list of n tiles in the form of numpy arrays. The solution returned
    is of the form [(p1, (row1, col1))...(pn,  (rown, coln))]
    where pi is a tile (may be rotated or flipped), and (rowi, coli) is 
    the coordinate of the upper left corner of pi in the board (lowest row and column index 
    that the tile covers).
    
    -Use np.flip and np.rot90 to manipulate pentominos.
    
    -You may assume there will always be a solution.
    """
    
    board = 1 - board # now the void position is 0 and occupied is 1
    board_oneline = board.ravel()
    delete_list = [] # positions where is originally "0", not allowed for tiling
    for j in range(np.shape(board_oneline)[0]):
        if board_oneline[j] == 1:
            delete_list.append(j + len(pents))
    delete_list = [np.array(delete_list)]
    

    exact_cover_matrix = []
    tiling_info = []
    for i in range(len(pents)):
        all_assignment_board, all_assignment_info = all_assignments(pents[i], board)
        for item in all_assignment_board:
            # make sure every mino is used for tiling
            item = np.append(np.zeros(len(pents)), item)
            item = np.delete(item, delete_list)
            item[i] = 1
            exact_cover_matrix.append(item)
        tiling_info.extend(all_assignment_info)

    exact_cover_matrix = np.array(exact_cover_matrix)
    exact_cover_matrix[exact_cover_matrix > 0] = 1 # occupied position all set to 1

    # use Algorithm_X to search for exact cover path
    result_list = algorithm_X(exact_cover_matrix, [], list(range(exact_cover_matrix.shape[0])))
    return_val = []
    for i in result_list:
        return_val.append((tiling_info[i][0], (tiling_info[i][1], tiling_info[i][2]))) # (mino, x, y)
    return return_val