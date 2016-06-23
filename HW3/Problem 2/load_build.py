# Braden Katzman - bmk2137
# Columbia University
# Artificial Intelligence Summer 2016
# HW3 - Question 2
# Description: 
#	Loads the raw data, transposes it, and splits into testing and training

import csv
import numpy as np

# global variables
class1 = []
class2 = []
labels = []

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
