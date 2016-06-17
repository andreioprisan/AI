#!/usr/bin/env python
#coding:utf-8

# hint source: http://stackoverflow.com/questions/22342854/what-is-the-optimal-algorithm-for-the-game-2048
# source: http://www.ranjaykrishna.com/blog/can-an-artificial-intelligence-win-2048
from math import pow

# 3D list of the gradients for each corner

gradients = [
    [[ 3,  2,  1,  0],
     [ 2,  1,  0, -1],
     [ 1,  0, -1, -2],
     [ 0, -1, -2, -3]],
    [[ 0,  1,  2,  3],
     [-1,  0,  1,  2],
     [-2, -1,  0,  1],
     [-3, -2, -1, -0]],
    [[ 0, -1, -2, -3],
     [ 1,  0, -1, -2],
     [ 2,  1,  0, -1],
     [ 0, -1, -2, -3]],
    [[-3, -2, -1,  0],
     [-2, -1,  0,  1],
     [-1,  0,  1,  2],
     [ 0,  1,  2,  3]]
]

class Heuristic:
    def heurisiticEval(self, grid):

        smoothWeight = 0.1
        gradientWeight = 3
        freeWeight = 2
        maxTileWeight = 0.2
        cornerWeight = 0.1

        # compute smoothness heuristic and apply weight
        smoothness = self.smoothness(grid) * smoothWeight

        # compute gradient score heuristic
        gradientScore = self.gradient_heur(grid) * gradientWeight

        # use the number of free tiles with weight as heuristic score
        freeTiles = len(grid.getAvailableCells()) * freeWeight

        maxTileHeur = grid.getMaxTile() * maxTileWeight

        # reward max tile in corner
        cornerHeur = 0
        maxTile = grid.getMaxTile()
        if maxTile == grid.getCellValue((3,3)) or maxTile == grid.getCellValue((0,3)) or maxTile == grid.getCellValue((0,0)) or maxTile == grid.getCellValue((3,0)):
            cornerHeur += (maxTile * cornerWeight)
        else:
            cornerHeur -= (maxTile * cornerWeight)

        return smoothness + gradientScore + freeTiles + maxTileHeur + cornerHeur

    # the smoothness heuristic measures the value difference between neighboring tiles
    def smoothness(self, grid):
        smoothness = 0

        # iterate over the grid
        for x in range(4):
            for y in range(4):
                # save the current tile value
                value = grid.getCellValue((x, y))

                # increment the 
                # highVal += pow(value, 2)
                if value:
                    # each value in the current row
                    for row in range(4):
                        smoothness -= abs(value - grid.getCellValue((row, y)))
                    
                    # each value in the current column
                    for col in range(4):
                        smoothness -= abs(value - grid.getCellValue((x, col)))


        return smoothness

    def gradient_heur(self, grid):
        gradient_scores = [0, 0, 0, 0]

        # use gradient_idx to reference both the gradient 2D array and the score in the list
        for gradient_idx in range(4):

            # iterate over the grid
            for row in range(4):
                for col in range(4):
                    gradient_scores[gradient_idx] += (gradients[gradient_idx][row][col] * grid.getCellValue((row, col)))


        return max(gradient_scores)


    # def monotonicity(self, grid):
    #     mono = 0
    #     cornerWeight = 1.5
    #     rewardWeight = 1.0
    #     penaltyWeight = 2.0

    #     # monotonicity - reward max tile in corner
    #     maxTile = grid.getMaxTile()
    #     if maxTile == grid.getCellValue((3,3)) or maxTile == grid.getCellValue((0,3)) or maxTile == grid.getCellValue((0,0)) or maxTile == grid.getCellValue((3,0)):
    #         mono += (maxTile * cornerWeight)
    #     else:
    #         mono -= (maxTile * cornerWeight)

    #     # scores: decrease down, decrease up, decrease right, decrease left
    #     decrD = 0
    #     decrU = 0
    #     decrR = 0
    #     decrL = 0

    #     # iterate over the grid four times, rewarding decrease in the given direction and penalizing otherwise

    #     # right -->
    #     row = 0
    #     col = 0
    #     while row < 4:
    #         while col < 3:
    #             curr = grid.getCellValue((row, col))
    #             nxt = grid.getCellValue((row, col+1))

    #             if curr > nxt: # reward
    #                 decrR += ((curr - nxt) * rewardWeight)
    #             elif curr < nxt: # penalize
    #                 decrR -= ((nxt - curr) * penaltyWeight)

    #             col += 1
    #         row += 1

    #     # left <--
    #     row = 0
    #     col = 3
    #     while row < 4:
    #         while col > 0:
    #             curr = grid.getCellValue((row, col))
    #             nxt = grid.getCellValue((row, col-1))

    #             if curr > nxt: # reward
    #                 decrL += ((curr - nxt) * rewardWeight)
    #             elif curr < nxt: # penalize
    #                 decrL -= ((nxt - curr) * penaltyWeight)

    #             col -= 1
    #         row += 1


    #     # up ^
    #     row = 3 
    #     col = 0
    #     while col < 4:
    #         while row > 0:
    #             curr = grid.getCellValue((row, col))
    #             nxt = grid.getCellValue((row-1, col))

    #             if curr > nxt: # reward
    #                 decrU += ((curr - nxt) * rewardWeight)
    #             elif curr < nxt:
    #                 decrU += ((nxt - curr) * penaltyWeight)

    #             row -= 1
    #         col += 1

    #     # down v
    #     row = 0
    #     col = 0
    #     while col < 4:
    #         while row < 3:
    #             curr = grid.getCellValue((row, col))
    #             nxt = grid.getCellValue((row+1, col))

    #             if curr > nxt: # reward
    #                 decrD += ((curr - nxt) * rewardWeight)
    #             elif curr < nxt:
    #                 decrD += ((nxt - curr) * penaltyWeight)

    #             row += 1
    #         col += 1



    #     # # iterate over grid, compute values for columns (left-right)
    #     # for row in range(4):
    #     #     for col in range(4):
    #     #         if col < 3:
    #     #             curr = grid.getCellValue((row, col))
    #     #             nxt = grid.getCellValue((row, col+1))

    #     #             if curr > nxt:
    #     #                 decrLR += (curr - nxt)
    #     #             elif curr < nxt:
    #     #                 incrLR += (nxt - curr)

    #     # # iterate over grid, compute values for rows (up-down)
    #     # for col in range(4):
    #     #     for row in range(4):
    #     #         if row < 3:
    #     #             curr = grid.getCellValue((row, col))
    #     #             nxt = grid.getCellValue((row+1, col))

    #     #             if curr > nxt:
    #     #                 decrUD += (curr - nxt)
    #     #             elif curr < nxt:
    #     #                 incrUD += (nxt - curr)


    #     scores = [decrD, decrU, decrR, decrL]

    #     mono += max(scores)

    #     return mono

# http://stackoverflow.com/questions/22342854/what-is-the-optimal-algorithm-for-the-game-2048