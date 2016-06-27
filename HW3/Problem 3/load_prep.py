# Braden Katzman - bmk2137
# Columbia University
# Artificial Intelligence Summer 2016
# HW3 - Question 2
# Description: 
#	Loads an image and converts to a 2D numpy array


# MAIN SOURCE USED:  http://scikit-learn.org/stable/auto_examples/cluster/plot_color_quantization.html
# source: http://stackoverflow.com/questions/25528654/numpy-array-to-png-file-and-back

from skimage.io import imread, imsave
import numpy as np

def loadImage(filename):
	print "\nloading image '{filename}'".format(filename=filename)

	trees = imread(filename)

	return trees


# From main source:
# Convert to floats instead of the default 8 bits integer coding. Dividing by
# 255 is important so that plt.imshow behaves works well on float data (need to
# be in the range [0-1]
def convertImgToFloats(img):
	print "\nconverting image data to floats in range [0,1]"

	img = np.array(img, dtype=np.float64) / 255

	return img

# transform an image into a 2D numpy array
def transformTo2DArray(img):
	print "\ntransforming image into 2D numpy array"

	width, height, dimensions = orig = tuple(img.shape)

	# print str(width) + ", " + str(height) + ", " + str(dimensions)

	# error check and make sure the original dimensions of the image is 3
	assert dimensions == 3

	# convert to array
	img_as_array = np.reshape(img, (width * height, dimensions))

	return img_as_array, width, height, dimensions