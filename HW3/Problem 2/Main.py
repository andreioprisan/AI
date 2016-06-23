# Braden Katzman - bmk2137
# Columbia University
# Artificial Intelligence Summer 2016
# HW3 - Question 2
# Description: 
#	Support vector classifiers in the sklearn package to learn 
# 	a classification model for a chessboard-like dataset
import time

import matplotlib.pyplot as plt
import load_build
import SVMs

if __name__ == '__main__':
	print "start"
	start_time = time.time()

	# load the raw data
	tup = load_build.load('chessboard.csv')

	vectors = load_build.buildVectors()

	# split data into training and testing
	data = SVMs.testSplit(vectors, load_build.getLabels())

	# get the support vector of training data
	sv = data[0][0]

	# get the test vector
	testv = data[1][0]


	print "\ntotal program execution = {t} seconds".format(t=(time.time()-start_time))
	print "exiting...\n"