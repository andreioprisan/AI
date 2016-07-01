#!/usr/bin/env python
#coding:utf-8

# Braden Katzman - bmk2137
# Columbia University
# COMS W4701 - Artificial Intelligence
# Summer 2016
# HW4 - Constraint Satisfaction Problems --> Sudoku

import time

ROW = "ABCDEFGHI"
COL = "123456789"
ROWRANGE = ["ABC", "DEF", "GHI"]
COLRANGE = ["123", "456", "789"]

# utility function to print each sudoku
def printSudoku(sudoku):
    print "-----------------"
    for i in ROW:
        for j in COL:
            print sudoku[i + j],
        print ""

# write soduku to file
def writeSudoku(f):
    f.write("-----------------\n")
    for i in ROW:
        for j in COL:
            f.write(repr(sudoku[i + j])),
        f.write("\n")


# check that every variables' domain has only one value
def checkSudoku(sudoku, domain):
    solved = True
    for key in sudoku.keys():
        if not len(domain[key]) == 1:
            solved = False
    return solved


# ensure that every value in sudoku is assigned to nonzero
def solvedSudoku(sudoku):
    solved = True
    for key in sudoku:
    	# update solved if zero value
        if sudoku[key] == 0:
            solved = False
    return solved

# ensure that the arrangement meets the constraints
def constraintValid(sudoku, neighbors):
    valid = True
    for key in sudoku:
        if sudoku[key] == 0:
            continue
        for neighbor in neighbors[key]:
            if sudoku[key] == sudoku[neighbor[1]]:
                valid = False
    return valid


# accessor method for neighbors of given key
def getNeighbors(key):
    neighbors = []
    for row in ROW:
        if key == row+key[1]:
            continue
        neighbors.insert(0, (key, row+key[1]))

    for col in COL:
        if key == key[0]+col:
            continue
        neighbors.insert(0, (key, key[0]+col))

    for inRow in ROWRANGE:
        if key[0] in inRow:
            for inCol in COLRANGE:
                if key[1] in inCol:
                    for let in inRow:
                        for ter in inCol:
                            if not key == let+ter:
                                neighbors.insert(0, (key, let+ter))
    return neighbors


# accessor method for min value given sudoku and domain
def getMinVal(sudoku, domain):
    minVal = ""
    min = 10
    for key in sudoku.keys():
        if len(domain[key]) < min and sudoku[key] == 0:
            minVal = key
            min = len(domain[key])
    return minVal


# return tuple of arcs, neighbors, domain
def queueArcs(sudoku, domain, neighbors):
    queue = []
    for key in sudoku.keys():
        neighbors[key] = getNeighbors(key)
        queue.extend(neighbors[key])
        domain[key] = list(COL)
    domain = pruneDomain(domain, sudoku, neighbors)
    return queue, neighbors, domain

# prune the given domain
def pruneDomain(domain, sudoku, neighbors):
    inDomain = domain.copy()
    for key in sudoku:
        if sudoku[key] != 0:
            inDomain[key] = [repr(sudoku[key])]
        else:
            for y in neighbors[key]:
                if sudoku[y[1]] in range(1, 10):
                    if repr(sudoku[y[1]]) in inDomain[key]:
                        inDomain[key].remove(repr(sudoku[y[1]]))
    return inDomain

# mutator method for removing given values
def removeVals(xi, xj, domain):
    removed = False
    for x in domain[xi]:
        if x in domain[xj] and len(domain[xj]) == 1:
            domain[xi].remove(x)
            removed = True
    return removed

# AC-3 algorithm for CSPs
def ac3(sudoku, domain, neighbors):
    queue, neighbors, domain = queueArcs(sudoku, domain, neighbors)
    while len(queue) != 0:
        xi, xj = queue.pop()
        if removeVals(xi, xj, domain):
            for xk in neighbors[xi]:
                queue.append((xk[1], xi))
    return domain


# recursively backtrack
def backtrackingRecurse(sudoku, domain, neighbors, ticker=0):
    if solvedSudoku(sudoku):
        return sudoku
    key = getMinVal(sudoku, domain)
    for testVal in domain[key]:
        testVal = int(testVal)
        sudoku[key] = testVal
        domainIn = pruneDomain(domain, sudoku, neighbors)
        if constraintValid(sudoku, neighbors):
            result = backtrackingRecurse(sudoku, domainIn, neighbors, ticker)
            if result is not False:
                return sudoku
        sudoku[key] = 0
    return False


# backtracking algorithm
def backtracking(sudoku, domain, neighbors):
    for key in sudoku.keys():
        neighbors[key] = getNeighbors(key)
        domain[key] = list(COL)
    domain = pruneDomain(domain, sudoku, neighbors)
    return backtrackingRecurse(sudoku, domain, neighbors)


# Reading of sudoku list from file
print "start"
t0 = time.time()
try:
    f = open("sudokus.txt", "r")
    sudokuList = f.read()
except:
    print "Error in reading the sudoku file."
    exit()

print "\nsolving sudokus using AC-3"

# count number of sudokus solved by AC-3
num_ac3_solved = 0
for line in sudokuList.split("\n"):
    # Parse sudokuList to individual sudoku in dict, e.g. sudoku["A2"] = 1
    sudoku = {ROW[i] + COL[j]: int(line[9*i+j]) for i in range(9) for j in range(9)}

    # write your AC3 algorithms here, update num_ac3_solved
    neighbors = {}
    domain = {}

    # run AC_3 on current sudoku
    domain = ac3(sudoku, domain, neighbors)
    if checkSudoku(sudoku, domain) == True:
        print "found winning sudoku #{num} using AC-3:".format(num=num_ac3_solved+1)
        num_ac3_solved += 1
        

print "\nsolved {n} sudoku puzzles using AC-3 algorithm in {s} seconds".format(n=num_ac3_solved, s=(time.time()-t0))
t1 = time.time()


# solve all sudokus by backtracking
print "\nsolving sudokus using backtracking. writing goal state boards to output.txt"
num_sol = 0
f = open("output.txt", 'w')
for line in sudokuList.split("\n"):
    # Parse sudokuList to individual sudoku in dict, e.g. sudoku["A2"] = 1
    sudoku = {ROW[i] + COL[j]: int(line[9*i+j]) for i in range(9) for j in range(9)}
    domain = {}
    neighbors = {}
    # write your backtracking algorithms here
    # printSudoku(sudoku)

    # call backtracking algorithm on current sudoku puzzle
    sudoku = backtracking(sudoku, domain, neighbors)

    if sudoku is not False:
        print "\nfound winning sudoku #{num} using backtracking:".format(num=num_sol+1)
    	printSudoku(sudoku)
        num_sol += 1
        writeSudoku(f)

print "\nsolved {n} sudoku puzzles using backtracking in {s} seconds".format(n=num_sol, s=(time.time()-t1))
print "\ntotal execution time: {t} seconds".format(t=(time.time()-t0))
print "exiting..."