#!/usr/bin/env python
#coding:utf-8

# hint source: http://stackoverflow.com/questions/22342854/what-is-the-optimal-algorithm-for-the-game-2048
from math import pow

class Heuristic:
    def heurisiticEval(self, grid):
        # the smoothness heuristic measures the value difference between neighboring tiles
        smoothweight = 0.1
        
        # the score for free tiles. we penalize having too few free tiles
        emptyweight = 5


        maxWeight = 2

        heurTup = self.smoothAndMono(grid)
        gridmax = grid.getMaxTile() * maxWeight
        gridempty = emptyweight * len(grid.getAvailableCells())
        gridSmoothness = heurTup[0] * smoothweight
        gridMono = heurTup[1]
        gridHighVal = heurTup[2]

        return gridmax + gridempty + gridSmoothness + gridMono + gridHighVal

    def smoothAndMono(self, grid):
        smoothness = 0
        mono = 0
        highVal = 1

        # iterate over the grid
        for x in range(4):
            for y in range(4):
                # save the current tile value
                value = grid.getCellValue((x, y))

                # increment the 
                highVal += pow(value, 2)
                if value:

                    # SMOOTHNESS
                    # each value in the current row
                    for row in range(4):
                        # compare each val in row to current val
                        # subtract from smoothness var the abs value of the difference
                        smoothness -= abs(value - grid.getCellValue((row, y)))
                    
                    # repeat above but for all values in the column
                    for col in range(4):
                        smoothness -= abs(value - grid.getCellValue((x, col)))
                    
                    # MONOTONICITY
                    if value == grid.getCellValue((x-1, y)):
                        mono += value
                    if value == grid.getCellValue((x+1, y)):
                        mono += value
                    if value == grid.getCellValue((x, y+1)):
                        mono += value
                    if value == grid.getCellValue((x, y-1)):
                        mono += value
        return smoothness, mono, highVal


# http://stackoverflow.com/questions/22342854/what-is-the-optimal-algorithm-for-the-game-2048