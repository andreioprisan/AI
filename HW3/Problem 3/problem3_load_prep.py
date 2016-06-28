# Braden Katzman - bmk2137
# Columbia University
# Artificial Intelligence Summer 2016
# HW3 - Question 2
# Description: 
#	Loads an image and converts to a 2D numpy array


# MAIN SOURCE USED:  http://scikit-learn.org/stable/auto_examples/cluster/plot_color_quantization.html
# source: http://stackoverflow.com/questions/25528654/numpy-array-to-png-file-and-back

import scipy as sp
import numpy as np
import warnings

def loadImage(filename):
	print "\nloading image '{filename}'".format(filename=filename)

	warnings.filterwarnings("ignore") # ignore uint8 to float64 warning
	# load file as np array
	trees = sp.misc.imread(filename)

	return trees

# transform an image into a 2D numpy array
def transformToArray(img):
	print "\ntransforming image into numpy array"

	width, height, dimensions = orig = tuple(img.shape)

	# convert to array
	img_as_array = np.reshape(img, (width * height, dimensions))

	return img_as_array, width, height, dimensions