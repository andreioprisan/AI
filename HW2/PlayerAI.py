# #!/usr/bin/env python
# #coding:utf-8

# from random import randint
# from BaseAI import BaseAI

# class PlayerAI(BaseAI):
# 	def getMove(self, grid):
# 		# I'm too naive, please change me!
# 		moves = grid.getAvailableMoves()
# 		return moves[randint(0, len(moves) - 1)] if moves else None


#!/usr/bin/env python
#coding:utf-8

import time
from Heuristic import Heuristic
from BaseAI import BaseAI
from random import randint


# build heuristic module
heuristic = Heuristic()

class PlayerAI(BaseAI):
    def getMove(self, grid):
    # I'm too naive, please change me!
    #     moves = grid.getAvailableMoves()
    #     return moves[randint(0, len(moves) - 1)] if moves else None
        return self.iterativeDepthTime(grid)

    def iterativeDepthTime(self, grid):
       # start at root
        depth = 1
        bestMove = 1

        # set time limit at 1 sec
        moveTime = 1

        # initialize alpha and beta to high and low values
        startAlpha = -10000
        startBeta = 10000

        # start a timer to track the time for each move
        start = time.time()

        # use iterative deepening to find best possible move in allotted time
        while (time.time() - start) < moveTime:
            # use alpha beta pruning to efficiently find a good move
            someBest = self.alphaBeta(depth, startAlpha, startBeta, grid, start)
            bestMove = someBest[0]
            depth += 1

        return bestMove

    # alpha beta pruning
    # params:
    #    - depth: the current depth in the iteratively deepning search algorithm. starts at 1, incremented by 1 on each iteration
    #    - alpha: the lowest value seen thus far
    #    - beta: the highest value seen thus far
    #    - grid: the current configuration of the board
    #    - start: the timer
    def alphaBeta(self, depth, alpha, beta, grid, start):
        # set alpha to the smallest value so far to iteratively improve
        best = alpha

        # get the available moves given the current board configuration
        moves = grid.getAvailableMoves()
        
        # if the game isn't over, naively set the best move to the first legal move in the list 
        if len(moves):
            bestMove = moves[0]
        else: # return 0 if game is over
            return 0, -10000, -10000

        # set beta to the largest value so far to iteratively improve
        minVal = beta

        # for every possible move the AI can make
        for move in moves:
        	# create a clone of the grid
            newGrid = grid.clone()

            # apply the move to the clone
            newGrid.move(move)

            # if leaf of depth limited search tree
            if depth <= 0:
                cost = heuristic.heurisiticEval(newGrid)
            #if depth >= 0, make an insert to every possible tile then select the smallest
            else:
                # insert to every possible tile position, assume insert is a 2 due to 90% probability
                minInsert = (0,0)
                for x in newGrid.getAvailableCells():
                    tileGrid = newGrid.clone()
                    tileGrid.insertTile(x, 2)
                    if (time.time() - start) > 1:
                        return bestMove, best, minVal
                    low = heuristic.heurisiticEval(tileGrid)

                    if minVal > low:
                        minVal = low
                        minInsert = x

                newGrid.insertTile(minInsert, 2)
                prune = self.alphaBeta(depth-1, minVal, beta, newGrid, start)
                cost = prune[1]

            if best < cost:
                best = cost
                bestMove = move
        return bestMove, best, minVal