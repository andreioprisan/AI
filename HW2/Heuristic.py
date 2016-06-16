#!/usr/bin/env python
#coding:utf-8

# hint source: http://stackoverflow.com/questions/22342854/what-is-the-optimal-algorithm-for-the-game-2048
from math import pow

class Heuristic:
    def heurisiticEval(self, grid):

        smoothWeight = 0.1
        monotonicityWeight = 1.0
        freeWeight = 5.0
        maxTileWeight = 1.0

        # compute smoothness heuristic and apply weight
        smoothness = self.smoothness(grid) * smoothWeight

        # compute monotonicity heuristic and apply weight
        monotonicity = self.monotonicity(grid) * monotonicityWeight

        # use the max tile with weight as heuristic score
        maxValHeur = grid.getMaxTile() * maxTileWeight

        # use the number of free tiles with weight as heuristic score
        freeTiles = len(grid.getAvailableCells()) * freeWeight

        return smoothness + monotonicity + maxValHeur + freeTiles
        # return gridmax + gridempty + gridSmoothness + gridMono + gridHighVal

    # the smoothness heuristic measures the value difference between neighboring tiles
    def smoothness(self, grid):
        smoothness = 0
        # highVal = 1


        # iterate by row, exploring each column before moving to the next row
        for row in range(4):
            for col in range(4):
                # check the current cell's neighbors to its right and down, if the board permits
                curr = grid.getCellValue((row, col))

                # not on right or bottom borders
                if col < 3 and row < 3:
                    right = grid.getCellValue((row, col+1))
                    down = grid.getCellValue((row+1, col))

                    if curr == right:
                        smoothness += curr

                    if curr == down:
                        smoothness += curr

                # on the right border, can only compare downward
                elif col == 3 and row < 3: 
                    down = grid.getCellValue((row+1, col))
                    if curr == down:
                        smoothness += curr

                # on the bottom border, can only compare right
                elif col < 3 and row == 3:
                    right = grid.getCellValue((row, col+1))

                    if curr == right:
                        smoothness += curr


        # # iterate over the grid
        # for x in range(4):
        #     for y in range(4):
        #         # save the current tile value
        #         value = grid.getCellValue((x, y))

        #         # increment the 
        #         # highVal += pow(value, 2)
        #         if value:

        #             # SMOOTHNESS
        #             # each value in the current row
        #             for row in range(4):
        #                 smoothness -= abs(value - grid.getCellValue((row, y)))
                    
        #             # repeat above but for all values in the column
        #             for col in range(4):
        #                 smoothness -= abs(value - grid.getCellValue((x, col)))


        return smoothness
        # return smoothness, mono, highVal

    def monotonicity(self, grid):
        mono = 0
        cornerWeight = 2.0

        # monotonicity - reward max tile in corner
        maxTile = grid.getMaxTile()
        if maxTile == grid.getCellValue((3,3)) or maxTile == grid.getCellValue((0,3)) or maxTile == grid.getCellValue((0,0)) or maxTile == grid.getCellValue((3,0)):
            mono += (maxTile * cornerWeight)

        # scores: increase up-down, decrease up-down, increase left-right, decrease left-right
        incrUD = 0
        decrUD = 0
        incrLR = 0
        decrLR = 0

        # iterate over grid, compute values for columns (left-right)
        for row in range(4):
            for col in range(4):
                if col < 3:
                    curr = grid.getCellValue((row, col))
                    next = grid.getCellValue((row, col+1))

                    if curr > next:
                        decrLR += (curr - next)
                    elif curr < next:
                        incrLR += (next - curr)

        # iterate over grid, compute values for rows (up-down)
        for col in range(4):
            for row in range(4):
                if row < 3:
                    curr = grid.getCellValue((row, col))
                    next = grid.getCellValue((row+1, col))

                    if curr > next:
                        decrUD += (curr - next)
                    elif curr < next:
                        incrUD += (next - curr)


        scores = [incrUD, decrUD, incrLR, decrLR]

        mono += max(scores)

        return mono
        


# http://stackoverflow.com/questions/22342854/what-is-the-optimal-algorithm-for-the-game-2048