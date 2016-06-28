# Braden Katzman - bmk2137
# DataPrepAndNormalization.py
# 	- This file loads the age, height and weight features
#	- The above features are then scaled by their stdevs and means set to 0
#	For each feature (a column in the data matrix), the following scaling formula is used:
#		x_scaled = x - mean(x) / stdev(x)

__author__ = "Braden Katzman bmk2137"
import csv
import numpy as np

# load the data into a matrix
def load(filename):
	print "\nloading data into matrix"
	x = [[], [], []] # features - intercept, age, weight (kg)
	y = [] # labels - height (m)

	# open a csv file reader and add the content to the data matrix
	with open(filename, 'rb') as csvfile:
		reader = csv.reader(csvfile, delimiter=',', )
		for row in reader:
			# append the values to the lists, parsing to float
			x[0].append(1) # add the vector 1 (intercept) ahead of row data 
			x[1].append(float(row[0])) # feature - age
			x[2].append(float(row[1])) # feature - weight
			y.append(float(row[2])) # label - height

	# return as tuple of features and labels
	return x, y

def mean_stdev(matrix):
    mean_age = np.mean(matrix[1])
    mean_weight = np.mean(matrix[2])
    stdev_age = np.std(matrix[1])
    stdev_weight = np.std(matrix[2])
    return [mean_age, stdev_age], [mean_weight, stdev_weight]

def printFeatureStats(tup):
	print "\nThe mean age is " + repr(tup[0][0]) + " and the std deviation is " + repr(tup[0][1])
	print "The mean weight is " + repr(tup[1][0]) + " and the std deviation is " + repr(tup[1][1])

# scales the data by the formula listed at top of file x_scaled
def scale(x, tup):
	print "\nscaling each feature by standard deviation and mean"
	# iterate over the columns in the raw data
	for i in range(1, len(x)):
		# iterate over all rows in each column
		for n in range(len(x[1])):
			# scale the value in the row
			x[i][n] = x_scaled(x[i][n], tup[i-1][0], tup[i-1][1])

	# return the scaled data
	return x


# helper function for computing x_scaled
def x_scaled(x, mean_x, stdev_x):
	return (x - mean_x) / stdev_x



