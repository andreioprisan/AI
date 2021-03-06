# Braden Katzman - bmk2137
# Columbia University
# Artificial Intelligence Summer 2016
# HW3 - Question 2
# Description: 
#	Facilitates the processing of an image using k-means clustering

import time
import problem3_load_prep as load_prep
import problem3_KMeans as KMeans
import problem3_RecreateImage as RecreateImage
import problem3_Plot as Plot


if __name__ == '__main__':
	print "start"
	start_time = time.time()

	### PART 1

	# load the image
	trees = load_prep.loadImage('trees.png')

	# get 2D array representation of image
	tup = load_prep.transformToArray(trees)
	trees_array = tup[0]
	width = tup[1]
	height = tup[2]
	dimensions = tup[3]

	# build a kmeans model with k = 3
	kmeans = KMeans.buildKMeans(3)

	# fit the image to the model
	kmeans = KMeans.fitKMeans(kmeans, trees_array)

	# predict the color indices on the image
	predictions = KMeans.predict(kmeans, trees_array)

	# recreate the image
	new_img = RecreateImage.recreateImage(trees_array, predictions, width, height, dimensions)

	# set the images up on the plot
	Plot.loadImagePlot(trees, 1, [0, 0, 1, 1], "Original")
	Plot.loadImagePlot(new_img, 2, [0, 0, 1, 1], "K Means k=3")

	Plot.showPlot()

	print "\ntotal program execution = {t} seconds".format(t=(time.time()-start_time))
	print "exiting...\n"