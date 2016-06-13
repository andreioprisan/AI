#!/usr/bin/env python
#coding:utf-8
from math import pow

class Heuristic:
    #from the provided hint, modified a bit
    def heurisiticEval(self, grid):
        smoothweight = 0.1
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

        for x in range(4):
            for y in range(4):
                value = grid.getCellValue((x, y))
                highVal += pow(value, 2)
                if value:
                    for row in range(4):
                        smoothness -= abs(value - grid.getCellValue((row, y)))
                    for col in range(4):
                        smoothness -= abs(value - grid.getCellValue((x, col)))
                    if value == grid.getCellValue((x-1, y)):
                        mono += value
                    if value == grid.getCellValue((x+1, y)):
                        mono += value
                    if value == grid.getCellValue((x, y + 1)):
                        mono += value
                    if value == grid.getCellValue((x, y-1)):
                        mono += value
        return smoothness, mono, highVal