# Braden Katzman - bmk2137
# Columbia University
# Artificial Intelligence Summer 2016
# HW3 - Question 2
# Description: 
#	Fits a K Means model to an image given a k value

from sklearn.cluster import KMeans
import scipy as sp
import warnings

# builds a K Means clustering model with given k value
def buildKMeans(k):
	print "\nbuilding k means model with k={k}".format(k=k)

	kmeans = KMeans(n_clusters=k)

	return kmeans

# fits the image array to the model
def fitKMeans(kmeans, img_array):
	print "\nfitting image array to k means model"

	kmeans.fit(img_array)
	print "done fitting"

	return kmeans

# predicts the color indices on the full image
def predict(kmeans, img_array):
	print "\npredicting color indices on full image"

	warnings.filterwarnings("ignore") # ignore uint8 to float64 warning

	predictions = kmeans.predict(img_array)
	print "done predicting"

	return predictions