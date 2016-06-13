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


class PlayerAI(BaseAI):
    def getMove(self, grid):
    # I'm too naive, please change me!
    #     moves = grid.getAvailableMoves()
    #     return moves[randint(0, len(moves) - 1)] if moves else None
        return self.iterativeDepthTime(grid)

    def iterativeDepthTime(self, grid):
        depth = 1
        bestMove = 1
        moveTime = .95
        startAlpha = -10000
        startBeta = 10000
        start = time.time()
        runTime = 0

        #uses iterative deepening to find best possible move in allotted time
        while runTime < moveTime:
            someBest = self.alphaBeta(depth, startAlpha, startBeta, grid, start)
            bestMove = someBest[0]
            depth += 1
            runTime += time.time() - start

        return bestMove

    def alphaBeta(self, depth, alpha, beta, grid, start):
        best = alpha
        moves = grid.getAvailableMoves()
        if len(moves):
            bestMove = moves[0]
        else:
            return 0, -10000, -10000
        heuristic = Heuristic()
        minVal = beta

        # for every possible move the AI can make
        for move in moves:
        	# create a clone of the grid
            newGrid = grid.clone()


            newGrid.move(move)
            #leaf of depth limited search tree
            if depth <= 0:
                cost = heuristic.heurisiticEval(newGrid)
            #if depth >= 0, make an insert to every possible tile then select the smallest
            else:
                #insert to every possible tile position, assume insert is a 2 due to 90% probability
                minInsert = (0,0)
                for x in newGrid.getAvailableCells():
                    tileGrid = newGrid.clone()
                    tileGrid.insertTile(x, 2)
                    if time.time() - start > 0.8:
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