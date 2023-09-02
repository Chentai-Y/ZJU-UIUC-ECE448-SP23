from time import sleep
from math import inf
from random import randint
import time

class ultimateTicTacToe:
    def __init__(self):
        """
        Initialization of the game.
        """
        self.board=[['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_']]
        self.maxPlayer='X'
        self.minPlayer='O'
        self.empty='_'
        self.maxDepth=3
        #The start indexes of each local board
        self.globalIdx=[(0,0),(0,3),(0,6),(3,0),(3,3),(3,6),(6,0),(6,3),(6,6)]

        #Start local board index for reflex agent playing
        self.startBoardIdx=4
        #self.startBoardIdx=randint(0,8)

        #utility value for reflex offensive and reflex defensive agents
        self.winnerMaxUtility=10000
        self.twoInARowMaxUtility=500
        self.preventThreeInARowMaxUtility=100
        self.cornerMaxUtility=30

        self.winnerMinUtility=-10000
        self.twoInARowMinUtility=-100
        self.preventThreeInARowMinUtility=-500
        self.cornerMinUtility=-30

        self.expandedNodes=0
        self.currPlayer=True

    def printGameBoard(self):
        """
        This function prints the current game board.
        """
        print('\n'.join([' '.join([str(cell) for cell in row]) for row in self.board[:3]])+'\n')
        print('\n'.join([' '.join([str(cell) for cell in row]) for row in self.board[3:6]])+'\n')
        print('\n'.join([' '.join([str(cell) for cell in row]) for row in self.board[6:9]])+'\n')



    def RuleTwo(self, player_cur, player_opp):
        """

        Help to count numbers for Rule2

        """
        scoreboard = 0

        for i in range(9):
            row, col = self.globalIdx[i]

            # 2-in-row
            if self.board[row][col] == self.board[row+1][col] == player_cur and self.board[row+2][col] == player_opp:
                scoreboard += 1
            elif self.board[row+1][col] == self.board[row+2][col] == player_cur and self.board[row][col] == player_opp:
                scoreboard += 1
            elif self.board[row][col] == self.board[row+2][col] == player_cur and self.board[row+1][col] == player_opp:
                scoreboard += 1
            if self.board[row][col+1] == self.board[row+1][col+1] == player_cur and self.board[row+2][col+1] == player_opp:
                scoreboard += 1
            elif self.board[row+1][col+1] == self.board[row+2][col+1] == player_cur and self.board[row][col+1] == player_opp:
                scoreboard += 1
            elif self.board[row][col+1] == self.board[row+2][col+1] == player_cur and self.board[row+1][col+1] == player_opp:
                scoreboard += 1
            if self.board[row][col+2] == self.board[row+1][col+2] == player_cur and self.board[row+2][col+2] == player_opp:
                scoreboard += 1
            elif self.board[row+1][col+2] == self.board[row+2][col+2] == player_cur and self.board[row][col+2] == player_opp:
                scoreboard += 1
            elif self.board[row][col+2] == self.board[row+2][col+2] == player_cur and self.board[row+1][col+2] == player_opp:
                scoreboard += 1
            # 2-in-col
            if self.board[row][col] == self.board[row][col+1] == player_cur and self.board[row][col+2] == player_opp:
                scoreboard += 1
            elif self.board[row][col] == self.board[row][col+2] == player_cur and self.board[row][col+1] == player_opp:
                scoreboard += 1
            elif self.board[row][col+1] == self.board[row][col+2] == player_cur and self.board[row][col] == player_opp:
                scoreboard += 1
            if self.board[row+1][col] == self.board[row+1][col+1] == player_cur and self.board[row+1][col+2] == player_opp:
                scoreboard += 1
            elif self.board[row+1][col] == self.board[row+1][col+2] == player_cur and self.board[row+1][col+1] == player_opp:
                scoreboard += 1
            elif self.board[row+1][col+1] == self.board[row+1][col+2] == player_cur and self.board[row+1][col] == player_opp:
                scoreboard += 1
            if self.board[row+2][col] == self.board[row+2][col+1] == player_cur and self.board[row+2][col+2] == player_opp:
                scoreboard += 1
            elif self.board[row+2][col] == self.board[row+2][col+2] == player_cur and self.board[row+2][col+1] == player_opp:
                scoreboard += 1
            elif self.board[row+2][col+1] == self.board[row+2][col+2] == player_cur and self.board[row+2][col] == player_opp:
                scoreboard += 1
            # 2-in-diagonal
            if self.board[row][col] == self.board[row+1][col+1] == player_cur and self.board[row+2][col+2] == player_opp:
                scoreboard += 1
            elif self.board[row+1][col+1] == self.board[row+2][col+2] == player_cur and self.board[row][col] == player_opp:
                scoreboard += 1
            elif self.board[row][col] == self.board[row+2][col+2] == player_cur and self.board[row+1][col+1] == player_opp:
                scoreboard += 1
            if self.board[row+2][col] == self.board[row+1][col+1] == player_cur and self.board[row][col+2] == player_opp:
                scoreboard += 1
            elif self.board[row+1][col+1] == self.board[row][col+2] == player_cur and self.board[row+2][col] == player_opp:
                scoreboard += 1
            elif self.board[row+2][col] == self.board[row][col+2] == player_cur and self.board[row+1][col+1] == player_opp:
                scoreboard += 1
        return scoreboard
    




    def evaluatePredifined(self, isMax):
        """
        This function implements the evaluation function for ultimate tic tac toe for predifined agent.
        input args:
        isMax(bool): boolean variable indicates whether it's maxPlayer or minPlayer.
                     True for maxPlayer, False for minPlayer
        output:
        score(float): estimated utility score for maxPlayer or minPlayer
        """
        #YOUR CODE HERE

        # Rule 1: If the offensive agent wins (form three-in-a-row), set the utility score to be 10000

        if self.checkWinner() == 1 and isMax:
            return self.winnerMaxUtility
        if self.checkWinner() == -1 and not isMax:
            return self.winnerMinUtility

        score = 0


        # Rule 2
                
         # Rule 2.1: For each unblocked two-in-a-row, increment the utility score by 500.
        if isMax:
            score += self.RuleTwo(self.maxPlayer,self.empty) * 500
            score += self.RuleTwo(self.minPlayer,self.maxPlayer) * 100
        else:
            score -= self.RuleTwo(self.minPlayer,self.empty) * 100
            score -= self.RuleTwo(self.maxPlayer,self.minPlayer) * 500


         # Rule 2.2: For each prevention, increment the utility score by 100.


        # for i in range(9):
        #     player_cur = ''
        #     player_opp = ''
        #     if isMax:  #(offensive) 
        #         player_cur = self.maxPlayer
        #         player_opp = self.minPlayer
        #     if not isMax: #(defensive) 
        #         player_cur = self.minPlayer
        #         player_opp = self.maxPlayer

            # row, col = self.globalIdx[i]
        #     # 2-in-row
        #     if self.board[row][col] == self.board[row+1][col] == player_cur and self.board[row+2][col] == self.empty:
        #         scoreboard += 500
        #     elif self.board[row+1][col] == self.board[row+2][col] == player_cur and self.board[row][col] == self.empty:
        #         scoreboard += 500
        #     elif self.board[row][col] == self.board[row+2][col] == player_cur and self.board[row+1][col] == self.empty:
        #         scoreboard += 500
        #     if self.board[row][col+1] == self.board[row+1][col+1] == player_cur and self.board[row+2][col+1] == self.empty:
        #         scoreboard += 500
        #     elif self.board[row+1][col+1] == self.board[row+2][col+1] == player_cur and self.board[row][col+1] == self.empty:
        #         scoreboard += 500
        #     elif self.board[row][col+1] == self.board[row+2][col+1] == player_cur and self.board[row+1][col+1] == self.empty:
        #         scoreboard += 500
        #     if self.board[row][col+2] == self.board[row+1][col+2] == player_cur and self.board[row+2][col+2] == self.empty:
        #         scoreboard += 500
        #     elif self.board[row+1][col+2] == self.board[row+2][col+2] == player_cur and self.board[row][col+2] == self.empty:
        #         scoreboard += 500
        #     elif self.board[row][col+2] == self.board[row+2][col+2] == player_cur and self.board[row+1][col+2] == self.empty:
        #         scoreboard += 500
        #     # 2-in-col
        #     if self.board[row][col] == self.board[row][col+1] == player_cur and self.board[row][col+2] == self.empty:
        #         scoreboard += 500
        #     elif self.board[row][col] == self.board[row][col+2] == player_cur and self.board[row][col+1] == self.empty:
        #         scoreboard += 500
        #     elif self.board[row][col+1] == self.board[row][col+2] == player_cur and self.board[row][col] == self.empty:
        #         scoreboard += 500
        #     if self.board[row+1][col] == self.board[row+1][col+1] == player_cur and self.board[row+1][col+2] == self.empty:
        #         scoreboard += 500
        #     elif self.board[row+1][col] == self.board[row+1][col+2] == player_cur and self.board[row+1][col+1] == self.empty:
        #         scoreboard += 500
        #     elif self.board[row+1][col+1] == self.board[row+1][col+2] == player_cur and self.board[row+1][col] == self.empty:
        #         scoreboard += 500
        #     if self.board[row+2][col] == self.board[row+2][col+1] == player_cur and self.board[row+2][col+2] == self.empty:
        #         scoreboard += 500
        #     elif self.board[row+2][col] == self.board[row+2][col+2] == player_cur and self.board[row+2][col+1] == self.empty:
        #         scoreboard += 500
        #     elif self.board[row+2][col+1] == self.board[row+2][col+2] == player_cur and self.board[row+2][col] == self.empty:
        #         scoreboard += 500
        #     # 2-in-diagonal
        #     if self.board[row][col] == self.board[row+1][col+1] == player_cur and self.board[row+2][col+2] == self.empty:
        #         scoreboard += 500
        #     elif self.board[row+1][col+1] == self.board[row+2][col+2] == player_cur and self.board[row][col] == self.empty:
        #         scoreboard += 500
        #     elif self.board[row][col] == self.board[row+2][col+2] == player_cur and self.board[row+1][col+1] == self.empty:
        #         scoreboard += 500
        #     if self.board[row+2][col] == self.board[row+1][col+1] == player_cur and self.board[row][col+2] == self.empty:
        #         scoreboard += 500
        #     elif self.board[row+1][col+1] == self.board[row][col+2] == player_cur and self.board[row+2][col] == self.empty:
        #         scoreboard += 500
        #     elif self.board[row+2][col] == self.board[row][col+2] == player_cur and self.board[row+1][col+1] == self.empty:
        #         scoreboard += 500

        #     # 2-opp-row & 1-cur-row
        #     if self.board[row][col] == self.board[row+1][col] == player_opp and self.board[row+2][col] == player_cur:
        #         scoreboard += 100
        #     elif self.board[row+1][col] == self.board[row+2][col] == player_opp and self.board[row][col] == player_cur:
        #         scoreboard += 100
        #     elif self.board[row][col] == self.board[row+2][col] == player_opp and self.board[row+1][col] == player_cur:
        #         scoreboard += 100
        #     if self.board[row][col+1] == self.board[row+1][col+1] == player_opp and self.board[row+2][col+1] == player_cur:
        #         scoreboard += 100
        #     elif self.board[row+1][col+1] == self.board[row+2][col+1] == player_opp and self.board[row][col+1] == player_cur:
        #         scoreboard += 100
        #     elif self.board[row][col+1] == self.board[row+2][col+1] == player_opp and self.board[row+1][col+1] == player_cur:
        #         scoreboard += 100
        #     if self.board[row][col+2] == self.board[row+1][col+2] == player_opp and self.board[row+2][col+2] == player_cur:
        #         scoreboard += 100
        #     elif self.board[row+1][col+2] == self.board[row+2][col+2] == player_opp and self.board[row][col+2] == player_cur:
        #         scoreboard += 100
        #     elif self.board[row][col+2] == self.board[row+2][col+2] == player_opp and self.board[row+1][col+2] == player_cur:
        #         scoreboard += 100
        #     # 2-opp-col & 1-cur-col
        #     if self.board[row][col] == self.board[row][col+1] == player_opp and self.board[row][col+2] == player_cur:
        #         scoreboard += 100
        #     elif self.board[row][col] == self.board[row][col+2] == player_opp and self.board[row][col+1] == player_cur:
        #         scoreboard += 100
        #     elif self.board[row][col+1] == self.board[row][col+2] == player_opp and self.board[row][col] == player_cur:
        #         scoreboard += 100
        #     if self.board[row+1][col] == self.board[row+1][col+1] == player_opp and self.board[row+1][col+2] == player_cur:
        #         scoreboard += 100
        #     elif self.board[row+1][col] == self.board[row+1][col+2] == player_opp and self.board[row+1][col+1] == player_cur:
        #         scoreboard += 100
        #     elif self.board[row+1][col+1] == self.board[row+1][col+2] == player_opp and self.board[row+1][col] == player_cur:
        #         scoreboard += 100
        #     if self.board[row+2][col] == self.board[row+2][col+1] == player_opp and self.board[row+2][col+2] == player_cur:
        #         scoreboard += 100
        #     elif self.board[row+2][col] == self.board[row+2][col+2] == player_opp and self.board[row+2][col+1] == player_cur:
        #         scoreboard += 100
        #     elif self.board[row+2][col+1] == self.board[row+2][col+2] == player_opp and self.board[row+2][col] == player_cur:
        #         scoreboard += 100
        #     # 2-opp-diagonal & 1-cur-diagonal
        #     if self.board[row][col] == self.board[row+1][col+1] == player_opp and self.board[row+2][col+2] == player_cur:
        #         scoreboard += 100
        #     elif self.board[row+1][col+1] == self.board[row+2][col+2] == player_opp and self.board[row][col] == player_cur:
        #         scoreboard += 100
        #     elif self.board[row][col] == self.board[row+2][col+2] == player_opp and self.board[row+1][col+1] == player_cur:
        #         scoreboard += 100
        #     if self.board[row+2][col] == self.board[row+1][col+1] == player_opp and self.board[row][col+2] == player_cur:
        #         scoreboard += 100
        #     elif self.board[row+1][col+1] == self.board[row][col+2] == player_opp and self.board[row+2][col] == player_cur:
        #         scoreboard += 100
        #     elif self.board[row+2][col] == self.board[row][col+2] == player_opp and self.board[row+1][col+1] == player_cur:
        #         scoreboard += 100

        # if isMax:
        #     score = score + scoreboard
        # else:
        #     score = score - scoreboard


        # Rule 3: For each corner taken by the offensive/defensive agent, increment/decrement the utility score by 30.
        if score == 0:
            for i in range(9):
                row3, col3 = self.globalIdx[i]
                if isMax:  #(offensive)
                    player_cur = self.maxPlayer
                    if self.board[row3][col3] == player_cur:
                        score += 30
                    if self.board[row3+2][col3] == player_cur:
                        score += 30
                    if self.board[row3][col3+2] == player_cur:
                        score += 30
                    if self.board[row3+2][col3+2] == player_cur:
                        score += 30
                if not isMax: #(defensive) 
                    player_cur = self.minPlayer
                    if self.board[row3][col3] == player_cur:
                        score -= 30
                    if self.board[row3+2][col3] == player_cur:
                        score -= 30
                    if self.board[row3][col3+2] == player_cur:
                        score -= 30
                    if self.board[row3+2][col3+2] == player_cur:
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
        #YOUR CODE HERE
        if self.checkWinner() == 1:
            return self.winnerMaxUtility
        if self.checkWinner() == -1:
            return self.winnerMinUtility

        score = 0


        # Rule 2
                
         # Rule 2.1: For each unblocked two-in-a-row, increment the utility score by 500.
        if isMax:
            score += self.RuleTwo(self.maxPlayer,self.empty) * 500
            score += self.RuleTwo(self.minPlayer,self.maxPlayer) * 100
        else:
            score -= self.RuleTwo(self.minPlayer,self.empty) * 100
            score -= self.RuleTwo(self.maxPlayer,self.minPlayer) * 500

        # # Rule 2
        # for i in range(9):
        #     player_cur = ''
        #     player_opp = ''
        #     if isMax:  #(offensive) 
        #         player_cur = self.maxPlayer
        #         player_opp = self.minPlayer
        #     if not isMax: #(defensive) 
        #         player_cur = self.minPlayer
        #         player_opp = self.maxPlayer
                
        #     row, col = self.globalIdx[i]
         
        # # Rule 2.1: For each unblocked two-in-a-row, increment the utility score by 500.
        #     # 2-in-row
        #     if self.board[row][col] == self.board[row+1][col] == player_cur and self.board[row+2][col] == self.empty:
        #         scoreboard += 500
        #     elif self.board[row+1][col] == self.board[row+2][col] == player_cur and self.board[row][col] == self.empty:
        #         scoreboard += 500
        #     elif self.board[row][col] == self.board[row+2][col] == player_cur and self.board[row+1][col] == self.empty:
        #         scoreboard += 500
        #     if self.board[row][col+1] == self.board[row+1][col+1] == player_cur and self.board[row+2][col+1] == self.empty:
        #         scoreboard += 500
        #     elif self.board[row+1][col+1] == self.board[row+2][col+1] == player_cur and self.board[row][col+1] == self.empty:
        #         scoreboard += 500
        #     elif self.board[row][col+1] == self.board[row+2][col+1] == player_cur and self.board[row+1][col+1] == self.empty:
        #         scoreboard += 500
        #     if self.board[row][col+2] == self.board[row+1][col+2] == player_cur and self.board[row+2][col+2] == self.empty:
        #         scoreboard += 500
        #     elif self.board[row+1][col+2] == self.board[row+2][col+2] == player_cur and self.board[row][col+2] == self.empty:
        #         scoreboard += 500
        #     elif self.board[row][col+2] == self.board[row+2][col+2] == player_cur and self.board[row+1][col+2] == self.empty:
        #         scoreboard += 500
        #     # 2-in-col
        #     if self.board[row][col] == self.board[row][col+1] == player_cur and self.board[row][col+2] == self.empty:
        #         scoreboard += 500
        #     elif self.board[row][col] == self.board[row][col+2] == player_cur and self.board[row][col+1] == self.empty:
        #         scoreboard += 500
        #     elif self.board[row][col+1] == self.board[row][col+2] == player_cur and self.board[row][col] == self.empty:
        #         scoreboard += 500
        #     if self.board[row+1][col] == self.board[row+1][col+1] == player_cur and self.board[row+1][col+2] == self.empty:
        #         scoreboard += 500
        #     elif self.board[row+1][col] == self.board[row+1][col+2] == player_cur and self.board[row+1][col+1] == self.empty:
        #         scoreboard += 500
        #     elif self.board[row+1][col+1] == self.board[row+1][col+2] == player_cur and self.board[row+1][col] == self.empty:
        #         scoreboard += 500
        #     if self.board[row+2][col] == self.board[row+2][col+1] == player_cur and self.board[row+2][col+2] == self.empty:
        #         scoreboard += 500
        #     elif self.board[row+2][col] == self.board[row+2][col+2] == player_cur and self.board[row+2][col+1] == self.empty:
        #         scoreboard += 500
        #     elif self.board[row+2][col+1] == self.board[row+2][col+2] == player_cur and self.board[row+2][col] == self.empty:
        #         scoreboard += 500
        #     # 2-in-diagonal
        #     if self.board[row][col] == self.board[row+1][col+1] == player_cur and self.board[row+2][col+2] == self.empty:
        #         scoreboard += 500
        #     elif self.board[row+1][col+1] == self.board[row+2][col+2] == player_cur and self.board[row][col] == self.empty:
        #         scoreboard += 500
        #     elif self.board[row][col] == self.board[row+2][col+2] == player_cur and self.board[row+1][col+1] == self.empty:
        #         scoreboard += 500
        #     if self.board[row+2][col] == self.board[row+1][col+1] == player_cur and self.board[row][col+2] == self.empty:
        #         scoreboard += 500
        #     elif self.board[row+1][col+1] == self.board[row][col+2] == player_cur and self.board[row+2][col] == self.empty:
        #         scoreboard += 500
        #     elif self.board[row+2][col] == self.board[row][col+2] == player_cur and self.board[row+1][col+1] == self.empty:
        #         scoreboard += 500

        # # Rule 2.2: For each prevention, increment the utility score by 100.
        #     # 2-opp-row & 1-cur-row
        #     if self.board[row][col] == self.board[row+1][col] == player_opp and self.board[row+2][col] == player_cur:
        #         scoreboard += 100
        #     elif self.board[row+1][col] == self.board[row+2][col] == player_opp and self.board[row][col] == player_cur:
        #         scoreboard += 100
        #     elif self.board[row][col] == self.board[row+2][col] == player_opp and self.board[row+1][col] == player_cur:
        #         scoreboard += 100
        #     if self.board[row][col+1] == self.board[row+1][col+1] == player_opp and self.board[row+2][col+1] == player_cur:
        #         scoreboard += 100
        #     elif self.board[row+1][col+1] == self.board[row+2][col+1] == player_opp and self.board[row][col+1] == player_cur:
        #         scoreboard += 100
        #     elif self.board[row][col+1] == self.board[row+2][col+1] == player_opp and self.board[row+1][col+1] == player_cur:
        #         scoreboard += 100
        #     if self.board[row][col+2] == self.board[row+1][col+2] == player_opp and self.board[row+2][col+2] == player_cur:
        #         scoreboard += 100
        #     elif self.board[row+1][col+2] == self.board[row+2][col+2] == player_opp and self.board[row][col+2] == player_cur:
        #         scoreboard += 100
        #     elif self.board[row][col+2] == self.board[row+2][col+2] == player_opp and self.board[row+1][col+2] == player_cur:
        #         scoreboard += 100
        #     # 2-opp-col & 1-cur-col
        #     if self.board[row][col] == self.board[row][col+1] == player_opp and self.board[row][col+2] == player_cur:
        #         scoreboard += 100
        #     elif self.board[row][col] == self.board[row][col+2] == player_opp and self.board[row][col+1] == player_cur:
        #         scoreboard += 100
        #     elif self.board[row][col+1] == self.board[row][col+2] == player_opp and self.board[row][col] == player_cur:
        #         scoreboard += 100
        #     if self.board[row+1][col] == self.board[row+1][col+1] == player_opp and self.board[row+1][col+2] == player_cur:
        #         scoreboard += 100
        #     elif self.board[row+1][col] == self.board[row+1][col+2] == player_opp and self.board[row+1][col+1] == player_cur:
        #         scoreboard += 100
        #     elif self.board[row+1][col+1] == self.board[row+1][col+2] == player_opp and self.board[row+1][col] == player_cur:
        #         scoreboard += 100
        #     if self.board[row+2][col] == self.board[row+2][col+1] == player_opp and self.board[row+2][col+2] == player_cur:
        #         scoreboard += 100
        #     elif self.board[row+2][col] == self.board[row+2][col+2] == player_opp and self.board[row+2][col+1] == player_cur:
        #         scoreboard += 100
        #     elif self.board[row+2][col+1] == self.board[row+2][col+2] == player_opp and self.board[row+2][col] == player_cur:
        #         scoreboard += 100
        #     # 2-opp-diagonal & 1-cur-diagonal
        #     if self.board[row][col] == self.board[row+1][col+1] == player_opp and self.board[row+2][col+2] == player_cur:
        #         scoreboard += 100
        #     elif self.board[row+1][col+1] == self.board[row+2][col+2] == player_opp and self.board[row][col] == player_cur:
        #         scoreboard += 100
        #     elif self.board[row][col] == self.board[row+2][col+2] == player_opp and self.board[row+1][col+1] == player_cur:
        #         scoreboard += 100
        #     if self.board[row+2][col] == self.board[row+1][col+1] == player_opp and self.board[row][col+2] == player_cur:
        #         scoreboard += 100
        #     elif self.board[row+1][col+1] == self.board[row][col+2] == player_opp and self.board[row+2][col] == player_cur:
        #         scoreboard += 100
        #     elif self.board[row+2][col] == self.board[row][col+2] == player_opp and self.board[row+1][col+1] == player_cur:
        #         scoreboard += 100
            
        # if isMax:
        #     score = score + scoreboard
        # else:
        #     score = score - scoreboard

        # Rule 3: For each corner taken by the offensive/defensive agent, increment/decrement the utility score by 30.
        if score == 0:
            for i in range(9):
                row3, col3 = self.globalIdx[i]
                if isMax:  #(offensive)
                    player_cur = self.maxPlayer
                    player_opp = self.minPlayer 
                    if self.board[row3][col3] == player_cur:
                        score += 30
                    elif self.board[row3+2][col3] == player_cur:
                        score += 30
                    elif self.board[row3][col3+2] == player_cur:
                        score += 30
                    elif self.board[row3+2][col3+2] == player_cur:
                        score += 30
                if not isMax: #(defensive) 
                    player_cur = self.minPlayer
                    player_opp = self.maxPlayer
                    if self.board[row3][col3] == player_cur:
                        score -= 30
                    elif self.board[row3+2][col3] == player_cur:
                        score -= 30
                    elif self.board[row3][col3+2] == player_cur:
                        score -= 30
                    elif self.board[row3+2][col3+2] == player_cur:
                        score -= 30

        # Rule 4: Calculate the distance between the pieces on the board.
        max_distances = []
        for i in range(3):
            for j in range(3):
                if isMax:
                    if self.board[i][j] == self.maxPlayer:
                        distances = []
                        for x in range(3):
                            for y in range(3):
                                if self.board[x][y] != self.maxPlayer:
                                    distances.append((abs(x-i)+abs(y-j)))
                        max_distances.append(max(distances))
                    if len(max_distances) > 0:
                        score += (10 - max(max_distances))
                if not isMax:
                    if self.board[i][j] == self.minPlayer:
                        distances = []
                        for x in range(3):
                            for y in range(3):
                                if self.board[x][y] != self.minPlayer:
                                    distances.append((abs(x-i)+abs(y-j)))
                        max_distances.append(max(distances))
                    if len(max_distances) > 0:
                        score -= (10 - max(max_distances))
        

        return score




    def checkMovesLeft(self):
        """
        This function checks whether any legal move remains on the board.
        output:
        movesLeft(bool): boolean variable indicates whether any legal move remains
                        on the board.
        """
        #YOUR CODE HERE
        movesLeft = False
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == self.empty:
                    movesLeft = True
        return movesLeft






    def checkWinner(self):
        #Return termimnal node status for maximizer player 1-win,0-tie,-1-lose
        """
        This function checks whether there is a winner on the board.
        output:
        winner(int): Return 0 if there is no winner.
                     Return 1 if maxPlayer is the winner.
                     Return -1 if miniPlayer is the winner.
        """
        #YOUR CODE HERE
        winner_sym = ''
        for i in range(9):
            row, col = self.globalIdx[i]
            if self.board[row][col] == self.board[row+1][col] == self.board[row+2][col] != self.empty:
                winner_sym = self.board[row][col]
            elif self.board[row][col+1] == self.board[row+1][col+1] == self.board[row+2][col+1] != self.empty:
                winner_sym = self.board[row][col+1]
            elif self.board[row][col+2] == self.board[row+1][col+2] == self.board[row+2][col+2] != self.empty:
                winner_sym = self.board[row][col+2]
            elif self.board[row][col] == self.board[row][col+1] == self.board[row][col+2] != self.empty:
                winner_sym = self.board[row][col]
            elif self.board[row+1][col] == self.board[row+1][col+1] == self.board[row+1][col+2] != self.empty:
                winner_sym = self.board[row+1][col]
            elif self.board[row+2][col] == self.board[row+2][col+1] == self.board[row+2][col+2] != self.empty:
                winner_sym = self.board[row+2][col]
            elif self.board[row][col] == self.board[row+1][col+1] == self.board[row+2][col+2] != self.empty:
                winner_sym = self.board[row][col]
            elif self.board[row+2][col] == self.board[row+1][col+1] == self.board[row][col+2] != self.empty:
                winner_sym = self.board[row+2][col]
            if winner_sym == self.maxPlayer:
                return 1
            if winner_sym == self.minPlayer:
                return -1
        return 0


    def nextBoardIdx(self,i,j):
        return 3*(i%3) + j%3



    def alphabeta(self,depth,currBoardIdx,alpha,beta,isMax):
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
        bestValue(float):the bestValue that current player may have
        """
        #YOUR CODE HERE
        bestValue=0.0
        if (depth == self.maxDepth) or (self.checkWinner() != 0) or (not self.checkMovesLeft()):
            self.expandedNodes += 1
            return self.evaluatePredifined(self.currPlayer)

        # for max player, alpha
        if isMax:
            x,y = self.globalIdx[currBoardIdx]
            bestValue = -inf
            for i in range(3):
                for j in range(3):
                    if self.board[x+i][y+j] == self.empty:
                        self.board[x+i][y+j] = self.maxPlayer
                        NowValue = self.alphabeta(depth+1,self.nextBoardIdx(x+i,y+j),alpha,beta,not isMax)
                        self.board[x+i][y+j] = self.empty
                        bestValue = max(NowValue,bestValue)
                        alpha = max(alpha,bestValue)
                        if beta <= alpha:
                            return bestValue
            return bestValue

        # for min player, beta
        else:
            x,y = self.globalIdx[currBoardIdx]
            bestValue = inf
            for i in range(3):
                for j in range(3):
                    if self.board[x+i][y+j] == self.empty:
                        self.board[x+i][y+j] = self.minPlayer
                        NowValue = self.alphabeta(depth+1,self.nextBoardIdx(x+i,y+j),alpha,beta,not isMax)
                        self.board[x+i][y+j] = self.empty
                        bestValue = min(NowValue,bestValue)
                        beta = min(beta,bestValue)
                        if beta <= alpha:
                            return bestValue
            return bestValue


    def alphabeta2(self,depth,currBoardIdx,alpha,beta,isMax):
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
        bestValue(float):the bestValue that current player may have
        """
        #YOUR CODE HERE
        bestValue=0.0
        if (depth == self.maxDepth) or (self.checkWinner() != 0) or (not self.checkMovesLeft()):
            self.expandedNodes += 1
            return self.evaluateDesigned(self.currPlayer)

        # for max player, alpha
        if isMax:
            x,y = self.globalIdx[currBoardIdx]
            bestValue = -inf
            for i in range(3):
                for j in range(3):
                    if self.board[x+i][y+j] == self.empty:
                        self.board[x+i][y+j] = self.maxPlayer
                        NowValue = self.alphabeta2(depth+1,self.nextBoardIdx(x+i,y+j),alpha,beta,not isMax)
                        self.board[x+i][y+j] = self.empty
                        bestValue = max(NowValue,bestValue)
                        alpha = max(alpha,bestValue)
                        if beta <= alpha:
                            return bestValue
            return bestValue

        # for min player, beta
        else:
            x,y = self.globalIdx[currBoardIdx]
            bestValue = inf
            for i in range(3):
                for j in range(3):
                    if self.board[x+i][y+j] == self.empty:
                        self.board[x+i][y+j] = self.minPlayer
                        NowValue = self.alphabeta2(depth+1,self.nextBoardIdx(x+i,y+j),alpha,beta,not isMax)
                        self.board[x+i][y+j] = self.empty
                        bestValue = min(NowValue,bestValue)
                        beta = min(beta,bestValue)
                        if beta <= alpha:
                            return bestValue
            return bestValue





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
        #YOUR CODE HERE
        bestValue=0.0
        if (depth == self.maxDepth) or (self.checkWinner() != 0) or (not self.checkMovesLeft()):
            self.expandedNodes += 1
            return self.evaluatePredifined(self.currPlayer)

        # for max player
        if isMax:
            x,y = self.globalIdx[currBoardIdx]
            bestValue = -inf
            for i in range(3):
                for j in range(3):
                    if self.board[x+i][y+j] == self.empty:
                        self.board[x+i][y+j] = self.maxPlayer
                        NowValue = self.minimax(depth+1, self.nextBoardIdx(x+i,y+j), not isMax)
                        self.board[x+i][y+j] = self.empty
                        bestValue = max(NowValue,bestValue)
            return bestValue

        # for min player
        else:
            x,y = self.globalIdx[currBoardIdx]
            bestValue = inf
            for i in range(3):
                for j in range(3):
                    if self.board[x+i][y+j] == self.empty:
                        self.board[x+i][y+j] = self.minPlayer
                        NowValue = self.minimax(depth+1, self.nextBoardIdx(x+i,y+j), not isMax)
                        self.board[x+i][y+j] = self.empty
                        bestValue = min(NowValue,bestValue)
            return bestValue
        



    def minimax2(self, depth, currBoardIdx, isMax):

        #YOUR CODE HERE
        bestValue=0.0
        if (depth == self.maxDepth) or (self.checkWinner() != 0) or (not self.checkMovesLeft()):
            self.expandedNodes += 1
            return self.evaluateDesigned(self.currPlayer)

        # for max player
        if isMax:
            x,y = self.globalIdx[currBoardIdx]
            bestValue = -inf
            for i in range(3):
                for j in range(3):
                    if self.board[x+i][y+j] == self.empty:
                        self.board[x+i][y+j] = self.maxPlayer
                        NowValue = self.minimax2(depth+1, self.nextBoardIdx(x+i,y+j), not isMax)
                        self.board[x+i][y+j] = self.empty
                        bestValue = max(NowValue,bestValue)
            return bestValue

        # for min player
        else:
            x,y = self.globalIdx[currBoardIdx]
            bestValue = inf
            for i in range(3):
                for j in range(3):
                    if self.board[x+i][y+j] == self.empty:
                        self.board[x+i][y+j] = self.minPlayer
                        NowValue = self.minimax2(depth+1, self.nextBoardIdx(x+i,y+j), not isMax)
                        self.board[x+i][y+j] = self.empty
                        bestValue = min(NowValue,bestValue)
            return bestValue

    def playGamePredifinedAgent(self,maxFirst,isMinimaxOffensive,isMinimaxDefensive):
        """
        This function implements the processes of the game of predifined offensive agent vs defensive agent.
        input args:
        maxFirst(bool): boolean variable indicates whether maxPlayer or minPlayer plays first.
                        True for maxPlayer plays first, and False for minPlayer plays first.
        isMinimaxOffensive(bool):boolean variable indicates whether it's using minimax or alpha-beta pruning algorithm for offensive agent.
                        True is minimax and False is alpha-beta.
        isMinimaxDefensive(bool):boolean variable indicates whether it's using minimax or alpha-beta pruning algorithm for defensive agent.
                        True is minimax and False is alpha-beta.
        output:
        bestMove(list of tuple): list of bestMove coordinates at each step
        bestValue(list of float): list of bestValue at each move
        expandedNodes(list of int): list of expanded nodes at each move
        gameBoards(list of 2d lists): list of game board positions at each move
        winner(int): 1 for maxPlayer is the winner, -1 for minPlayer is the winner, and 0 for tie.
        """
        #YOUR CODE HERE
        bestMove=[]
        bestValue=[]
        gameBoards=[]
        currBoardIdx = self.startBoardIdx
        curplayer = maxFirst
        expandedNodes = []
        self.expandedNodes = 0

        alpha = -inf
        beta = inf
        while (self.checkWinner() == 0) and (self.checkMovesLeft()):
            if curplayer:
                self.currPlayer = True
                x,y = self.globalIdx[currBoardIdx]
                best_Move = (-1,-1)
                best_Value = -inf
                for i in range(3):
                    for j in range(3):
                        if self.board[x+i][y+j] == self.empty:
                            self.board[x+i][y+j] = self.maxPlayer
                            currBoardIdx = self.nextBoardIdx(x+i, y+j)
                            if isMinimaxOffensive:
                                Now_Value = self.minimax(1, currBoardIdx, not curplayer)
                            if not isMinimaxOffensive:
                                Now_Value = self.alphabeta(1, currBoardIdx,alpha, beta, not curplayer)
                            self.board[x+i][y+j] = self.empty
                            if Now_Value > best_Value:
                                best_Move = (x+i, y+j)
                                best_Value = max(Now_Value,best_Value)

                self.board[best_Move[0]][best_Move[1]] = self.maxPlayer
                currBoardIdx = self.nextBoardIdx(best_Move[0],best_Move[1])
                bestMove.append(best_Move)
                bestValue.append(best_Value)
                gameBoards.append(self.board)
                expandedNodes.append(self.expandedNodes)
                self.printGameBoard()
                curplayer = not curplayer

            else:
                self.currPlayer = False
                x,y = self.globalIdx[currBoardIdx]
                best_Move = (-1,-1)
                best_Value = inf
                for i in range(3):
                    for j in range(3):
                        if self.board[x+i][y+j] == self.empty:
                            self.board[x+i][y+j] = self.minPlayer
                            currBoardIdx = self.nextBoardIdx(x+i, y+j)
                            if isMinimaxDefensive:
                                Now_Value = self.minimax(1, currBoardIdx, not curplayer)
                            if not isMinimaxDefensive:
                                Now_Value = self.alphabeta(1, currBoardIdx,alpha, beta, not curplayer)
                            self.board[x+i][y+j] = self.empty
                            if Now_Value < best_Value:
                                best_Move = (x+i, y+j)
                                best_Value = min(Now_Value,best_Value)

                self.board[best_Move[0]][best_Move[1]] = self.minPlayer
                currBoardIdx = self.nextBoardIdx(best_Move[0],best_Move[1])
                bestMove.append(best_Move)
                bestValue.append(best_Value)
                gameBoards.append(self.board)
                expandedNodes.append(self.expandedNodes)
                self.printGameBoard()
                curplayer = not curplayer

        
        winner = self.checkWinner()

        return gameBoards, bestMove, expandedNodes, bestValue, winner

    def playGameYourAgent(self):
        """
        This function implements the processes of the game of your own agent vs predifined offensive agent.
        input args:
        output:
        bestMove(list of tuple): list of bestMove coordinates at each step
        gameBoards(list of 2d lists): list of game board positions at each move
        winner(int): 1 for maxPlayer is the winner, -1 for minPlayer is the winner, and 0 for tie.
        """
        #YOUR CODE HERE
        bestMove=[]
        bestValue=[]
        gameBoards=[]
        winner=0
        currBoardIdx = self.startBoardIdx
        curplayer = True
        expandedNodes = []
        self.expandedNodes = 0

        alpha = -inf
        beta = inf
        while (self.checkWinner() == 0) and (self.checkMovesLeft()):
            if curplayer:
                self.currPlayer = True
                x,y = self.globalIdx[currBoardIdx]
                best_Move = (-1,-1)
                best_Value = -inf
                for i in range(3):
                    for j in range(3):
                        if self.board[x+i][y+j] == self.empty:
                            self.board[x+i][y+j] = self.maxPlayer
                            currBoardIdx = self.nextBoardIdx(x+i,y+j)
                            Now_Value = self.alphabeta(1, currBoardIdx,alpha, beta, not curplayer)
                            self.board[x+i][y+j] = self.empty
                            if Now_Value > best_Value:
                                best_Move = (x+i, y+j)
                                best_Value = max(Now_Value,best_Value)

                self.board[best_Move[0]][best_Move[1]] = self.maxPlayer
                currBoardIdx = self.nextBoardIdx(best_Move[0],best_Move[1])
                bestMove.append(best_Move)
                bestValue.append(best_Value)
                gameBoards.append(self.board)
                expandedNodes.append(self.expandedNodes)
                self.printGameBoard()
                curplayer = not curplayer


            else:
                self.currPlayer = False
                x,y = self.globalIdx[currBoardIdx]
                best_Move = (-1,-1)
                best_Value = inf
                for i in range(3):
                    for j in range(3):
                        if self.board[x+i][y+j] == self.empty:
                            self.board[x+i][y+j] = self.minPlayer
                            currBoardIdx = self.nextBoardIdx(x+i,y+j)
                            Now_Value = self.minimax2(1, currBoardIdx, not curplayer)
                            self.board[x+i][y+j] = self.empty
                            if Now_Value < best_Value:
                                best_Move = (x+i, y+j)
                                best_Value = min(Now_Value,best_Value)

                self.board[best_Move[0]][best_Move[1]] = self.minPlayer
                currBoardIdx = self.nextBoardIdx(best_Move[0],best_Move[1])
                bestMove.append(best_Move)
                bestValue.append(best_Value)
                gameBoards.append(self.board)
                expandedNodes.append(self.expandedNodes)
                self.printGameBoard()
                curplayer = not curplayer

        
        winner = self.checkWinner()
        return gameBoards, bestMove, expandedNodes, bestValue, winner


    def playGameYourAgent2(self):
        """

        """
        #YOUR CODE HERE
        bestMove=[]
        bestValue=[]
        gameBoards=[]
        winner=0
        currBoardIdx = self.startBoardIdx
        curplayer = True
        expandedNodes = []
        self.expandedNodes = 0

        alpha = -inf
        beta = inf
        while (self.checkWinner() == 0) and (self.checkMovesLeft()):
            if curplayer:
                self.currPlayer = True
                x,y = self.globalIdx[currBoardIdx]
                best_Move = (-1,-1)
                best_Value = -inf
                for i in range(3):
                    for j in range(3):
                        if self.board[x+i][y+j] == self.empty:
                            self.board[x+i][y+j] = self.maxPlayer
                            currBoardIdx = self.nextBoardIdx(x+i,y+j)
                            Now_Value = self.minimax(1, currBoardIdx, not curplayer)
                            self.board[x+i][y+j] = self.empty
                            if Now_Value > best_Value:
                                best_Move = (x+i, y+j)
                                best_Value = max(Now_Value,best_Value)

                self.board[best_Move[0]][best_Move[1]] = self.maxPlayer
                currBoardIdx = self.nextBoardIdx(best_Move[0],best_Move[1])
                bestMove.append(best_Move)
                bestValue.append(best_Value)
                gameBoards.append(self.board)
                expandedNodes.append(self.expandedNodes)
                self.printGameBoard()
                curplayer = not curplayer


            else:
                self.currPlayer = False
                x,y = self.globalIdx[currBoardIdx]
                best_Move = (-1,-1)
                best_Value = inf
                for i in range(3):
                    for j in range(3):
                        if self.board[x+i][y+j] == self.empty:
                            self.board[x+i][y+j] = self.minPlayer
                            currBoardIdx = self.nextBoardIdx(x+i,y+j)
                            Now_Value = self.minimax2(1, currBoardIdx, not curplayer)
                            self.board[x+i][y+j] = self.empty
                            if Now_Value < best_Value:
                                best_Move = (x+i, y+j)
                                best_Value = min(Now_Value,best_Value)

                self.board[best_Move[0]][best_Move[1]] = self.minPlayer
                currBoardIdx = self.nextBoardIdx(best_Move[0],best_Move[1])
                bestMove.append(best_Move)
                bestValue.append(best_Value)
                gameBoards.append(self.board)
                expandedNodes.append(self.expandedNodes)
                self.printGameBoard()
                curplayer = not curplayer

        
        winner = self.checkWinner()
        return gameBoards, bestMove, expandedNodes, bestValue, winner


    def playGameYourAgent3(self):
        """

        """
        #YOUR CODE HERE
        bestMove=[]
        bestValue=[]
        gameBoards=[]
        winner=0
        currBoardIdx = self.startBoardIdx
        curplayer = True
        expandedNodes = []
        self.expandedNodes = 0

        alpha = -inf
        beta = inf
        while (self.checkWinner() == 0) and (self.checkMovesLeft()):
            if curplayer:
                self.currPlayer = True
                x,y = self.globalIdx[currBoardIdx]
                best_Move = (-1,-1)
                best_Value = -inf
                for i in range(3):
                    for j in range(3):
                        if self.board[x+i][y+j] == self.empty:
                            self.board[x+i][y+j] = self.maxPlayer
                            currBoardIdx = self.nextBoardIdx(x+i,y+j)
                            Now_Value = self.alphabeta(1, currBoardIdx,alpha, beta, not curplayer)
                            self.board[x+i][y+j] = self.empty
                            if Now_Value > best_Value:
                                best_Move = (x+i, y+j)
                                best_Value = max(Now_Value,best_Value)

                self.board[best_Move[0]][best_Move[1]] = self.maxPlayer
                currBoardIdx = self.nextBoardIdx(best_Move[0],best_Move[1])
                bestMove.append(best_Move)
                bestValue.append(best_Value)
                gameBoards.append(self.board)
                expandedNodes.append(self.expandedNodes)
                self.printGameBoard()
                curplayer = not curplayer


            else:
                self.currPlayer = False
                x,y = self.globalIdx[currBoardIdx]
                best_Move = (-1,-1)
                best_Value = inf
                for i in range(3):
                    for j in range(3):
                        if self.board[x+i][y+j] == self.empty:
                            self.board[x+i][y+j] = self.minPlayer
                            currBoardIdx = self.nextBoardIdx(x+i,y+j)
                            Now_Value = self.alphabeta2(1, currBoardIdx,alpha, beta, not curplayer)
                            self.board[x+i][y+j] = self.empty
                            if Now_Value < best_Value:
                                best_Move = (x+i, y+j)
                                best_Value = min(Now_Value,best_Value)

                self.board[best_Move[0]][best_Move[1]] = self.minPlayer
                currBoardIdx = self.nextBoardIdx(best_Move[0],best_Move[1])
                bestMove.append(best_Move)
                bestValue.append(best_Value)
                gameBoards.append(self.board)
                expandedNodes.append(self.expandedNodes)
                self.printGameBoard()
                curplayer = not curplayer

        
        winner = self.checkWinner()
        return gameBoards, bestMove, expandedNodes, bestValue, winner

    def playGameYourAgent4(self):
        """

        """
        #YOUR CODE HERE
        bestMove=[]
        bestValue=[]
        gameBoards=[]
        winner=0
        currBoardIdx = self.startBoardIdx
        curplayer = True
        expandedNodes = []
        self.expandedNodes = 0

        alpha = -inf
        beta = inf
        while (self.checkWinner() == 0) and (self.checkMovesLeft()):
            if curplayer:
                self.currPlayer = True
                x,y = self.globalIdx[currBoardIdx]
                best_Move = (-1,-1)
                best_Value = -inf
                for i in range(3):
                    for j in range(3):
                        if self.board[x+i][y+j] == self.empty:
                            self.board[x+i][y+j] = self.maxPlayer
                            currBoardIdx = self.nextBoardIdx(x+i,y+j)
                            Now_Value = self.minimax(1, currBoardIdx, not curplayer)
                            self.board[x+i][y+j] = self.empty
                            if Now_Value > best_Value:
                                best_Move = (x+i, y+j)
                                best_Value = max(Now_Value,best_Value)

                self.board[best_Move[0]][best_Move[1]] = self.maxPlayer
                currBoardIdx = self.nextBoardIdx(best_Move[0],best_Move[1])
                bestMove.append(best_Move)
                bestValue.append(best_Value)
                gameBoards.append(self.board)
                expandedNodes.append(self.expandedNodes)
                self.printGameBoard()
                curplayer = not curplayer


            else:
                self.currPlayer = False
                x,y = self.globalIdx[currBoardIdx]
                best_Move = (-1,-1)
                best_Value = inf
                for i in range(3):
                    for j in range(3):
                        if self.board[x+i][y+j] == self.empty:
                            self.board[x+i][y+j] = self.minPlayer
                            currBoardIdx = self.nextBoardIdx(x+i,y+j)
                            Now_Value = self.alphabeta2(1, currBoardIdx,alpha, beta, not curplayer)
                            self.board[x+i][y+j] = self.empty
                            if Now_Value < best_Value:
                                best_Move = (x+i, y+j)
                                best_Value = min(Now_Value,best_Value)

                self.board[best_Move[0]][best_Move[1]] = self.minPlayer
                currBoardIdx = self.nextBoardIdx(best_Move[0],best_Move[1])
                bestMove.append(best_Move)
                bestValue.append(best_Value)
                gameBoards.append(self.board)
                expandedNodes.append(self.expandedNodes)
                self.printGameBoard()
                curplayer = not curplayer

        
        winner = self.checkWinner()
        return gameBoards, bestMove, expandedNodes, bestValue, winner


    def playGameHuman(self):
        """
        This function implements the processes of the game of your own agent vs a human.
        output:
        bestMove(list of tuple): list of bestMove coordinates at each step
        gameBoards(list of 2d lists): list of game board positions at each move
        winner(int): 1 for maxPlayer is the winner, -1 for minPlayer is the winner, and 0 for tie.
        """
        #YOUR CODE HERE
        bestMove=[]
        bestValue=[]
        gameBoards=[]
        winner=0
        currBoardIdx = self.startBoardIdx
        curplayer = True
        expandedNodes = []
        self.expandedNodes = 0
        alpha = -inf
        beta = inf
        while (self.checkWinner() == 0) and (self.checkMovesLeft()):
            if curplayer:
                self.currPlayer = True
                x,y = self.globalIdx[currBoardIdx]
                best_Move = (-1,-1)
                best_Value = -inf
                for i in range(3):
                    for j in range(3):
                        if self.board[x+i][y+j] == self.empty:
                            self.board[x+i][y+j] = self.maxPlayer
                            currBoardIdx = self.nextBoardIdx(x+i,y+j)
                            Now_Value = self.alphabeta2(1, currBoardIdx, alpha, beta, not curplayer)
                            #Now_Value = self.minimax2(1, currBoardIdx, not curplayer)
                            self.board[x+i][y+j] = self.empty
                            if Now_Value > best_Value:
                                best_Move = (x+i, y+j)
                                best_Value = max(Now_Value,best_Value)

                self.board[best_Move[0]][best_Move[1]] = self.maxPlayer
                currBoardIdx = self.nextBoardIdx(best_Move[0],best_Move[1])
                bestMove.append(best_Move)
                bestValue.append(best_Value)
                gameBoards.append(self.board)
                expandedNodes.append(self.expandedNodes)
                self.printGameBoard()
                curplayer = not curplayer
            
            else:
                self.currPlayer = False
                x, y = self.globalIdx[currBoardIdx]

                print("Your turn, on board:", currBoardIdx)
                y = input('row:')
                x = input('col:')
                put_y = self.globalIdx[currBoardIdx][1] + int(x)
                put_x = self.globalIdx[currBoardIdx][0] + int(y)
                #put_y = int(x)
                #put_x = int(y)
                self.board[put_x][put_y] = self.maxPlayer
                currBoardIdx = self.nextBoardIdx(put_x, put_y)
                self.board[put_x][put_y] = self.minPlayer
                currBoardIdx = self.nextBoardIdx(put_x, put_y)
                gameBoards.append(self.board)
                self.printGameBoard()
                curplayer = not curplayer

        winner = self.checkWinner()

        return gameBoards, bestMove, expandedNodes, bestValue, winner

if __name__=="__main__":
    uttt=ultimateTicTacToe()
    # feel free to write your own test code
    start = time.time()

    #gameBoards, bestMove, expandedNodes, bestValue, winner=uttt.playGamePredifinedAgent(True,True,False)
    #gameBoards, best_coord, expandedNodes, bestValue, winner = uttt.playGameYourAgent4()
    gameBoards, best_coord, expandedNodes, bestValue, winner = uttt.playGameHuman()

    print(expandedNodes)
    print(bestValue)
    print("time spent: ", time.time() - start)
    if winner == 1:
        print("The winner is maxPlayer!!!")
    elif winner == -1:
        print("The winner is minPlayer!!!")
    else:
        print("Tie. No winner:(")
