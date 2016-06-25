# Braden Katzman - bmk2137
# Columbia University
# Artificial Intelligence Summer 2016
# HW3 - Question 2
# Description: 
#	Support vector classifiers in the sklearn package to learn 
# 	a classification model for a chessboard-like dataset
import time

import load_build
import SVMs
import LogisticRegression as lr
import DecisionTree as dec_tree
import Plot

if __name__ == '__main__':
	print "start"
	start_time = time.time()

	# load the raw data
	tup = load_build.load('chessboard.csv')

	vectors = load_build.buildVectors()

	# split data into training and testing
	data = load_build.testSplit(vectors, load_build.getLabels())

	# get the support vector of training data
	sv = data[0][0]

	# get the test vector
	testv = data[1][0]

	# build and train linear, polynomial, and radial basis function SVMs
	# linearSVM = SVMs.linearSVM(100)
	# linearSVM = SVMs.trainSVM(linearSVM, sv, data[0][1])

	# polynomialSVM = SVMs.polynomialSVM(100., 5)
	# polynomialSVM = SVMs.trainSVM(polynomialSVM, sv, data[0][1])

	# rbfSVM = SVMs.rbfSVM(1000., 1)
	# rbfSVM = SVMs.trainSVM(rbfSVM, sv, data[0][1])

	# # SVMs.runCVAndOptimize(sv, data[0][1]) # REPORT THE SCORES PRINTED IN TRAIN METHOD

	# # test the three SVMs and report their accuracies
	# SVMs.accuracyTest(linearSVM, polynomialSVM, rbfSVM, data[1][0], data[1][1])

	# build a logistic regression classifier
	logReg = lr.logReg(100.) # NEED TO RUN THE OPTIMIZATION AND FIND THE BEST VALUE TO USE HERE
	logReg = lr.trainLogReg(logReg, sv, data[0][1])

	# lr.runCVAndOptimize(sv, data[0][1])

	# test the logistic regression classifier and report its accuracy
	lr.accuracyTest(logReg, data[1][0], data[1][1])

	# build a decision tree classifier
	dt = dec_tree.decisionTree(5.)
	dt = dec_tree.trainDT(dt, sv, data[0][1])

	# dt.runCVAndOptimize(dt, data[0][1])

	dec_tree.accuracyTest(dt, data[1][0], data[1][1])

	# create the plot
	# Plot.setup(sv, linearSVM, rbfSVM, polynomialSVM, tup)

	print "\ntotal program execution = {t} seconds".format(t=(time.time()-start_time))
	print "exiting...\n"