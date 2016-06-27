# Braden Katzman - bmk2137
# Columbia University
# Artificial Intelligence Summer 2016
# HW3 - Question 2
# Description: 
#	Given K Means predictions, this module recreates the image

import numpy as np

def recreateImage(img_array, predictions, width, height, dimensions):
	print "\nrecreating image from k means clustering predictions"

	# create an array of zeros with the same shape as the original image
	img = np.zeros((width, height, dimensions))

	predictions_iterator = 0

	# iterate over the width of the image
	for i in range(width):

		# iterate over the height of the image
		for j in range(height):
			# set the image pixel value to the matching label predictions
			img[i][j] = img_array[predictions[predictions_iterator]]

			# increment the predictions counter
			predictions_iterator += 1

	print "done recreating"
	return img