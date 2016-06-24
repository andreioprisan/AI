# Braden Katzman - bmk2137
# Columbia University
# Artificial Intelligence Summer 2016
# HW3 - Question 2
# Description: 
#	Loads the raw data, transposes it, and splits into testing and training

import csv
import numpy as np
from sklearn.cross_validation import train_test_split

# global variables
class1 = []
class2 = []
labels = []

# split the raw data into 40% testing and 60% training
def testSplit(vectors, labels):
	print "\nsplitting data into 60% training and 40% testing"
	train1, test1, trainL, testL = train_test_split(vectors, labels, test_size=0.4, random_state=42)
	return [train1, trainL], [test1, testL]

# builds transposed vectors
def buildVectors():
	print "\ntransposing vectors"
	st = np.transpose([class1, class2])
	return st

# load the chessboard data into a data matrix and return as tuple
def load(filename):
	print "\nloading raw data from {filename}".format(filename=filename)
	with open(filename, 'rU') as csvfile:
		reader = csv.reader(csvfile, delimiter=',', )
		reader.next() # skip the header line
		for row in reader:
			class1.append(float(row[0]))
			class2.append(float(row[1]))
			labels.append(float(row[2]))

	return class1, class2, labels

def getClass1():
	return class1

def getClass2():
	return getClass2

def getLabels():
	return labels
