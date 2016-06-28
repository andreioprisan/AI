# Braden Katzman - bmk2137
# Columbia University
# Artificial Intelligence Summer 2016
# HW3 - Question 2
# Description: 
#	Uses spectral clustering to segment an image

import time
import scipy as sp
import numpy as np
import matplotlib.pyplot as plt

from sklearn.feature_extraction import image
from sklearn.cluster import spectral_clustering
from sklearn.utils.testing import SkipTest
from sklearn.utils.fixes import sp_version

def run(img_array):
	print img_array.shape
	# img_array = sp.misc.imresize(img_array, 0.10) / 255.

	graph = image.img_to_graph(img_array)

	beta = 5
	eps = 1e-6
	graph.data = np.exp(-beta * graph.data / graph.data.std()) + eps

	N_REGIONS = 3

	for assign_labels in ('kmeans', 'discretize'):
		print assign_labels
		t0 = time.time()
		labels = spectral_clustering(graph, n_clusters=N_REGIONS, assign_labels=assign_labels, random_state=1)
		print "past"
		t1 = time.time()
		labels = labels.reshape(img_array.shape)

		plt.figure(figsize=(5, 5))
		plt.imshow(img_array, cmap=plt.cm.gray)

		for l in range(N_REGIONS):
			print l
			plt.contour(labels == l, contours=1, colors=[plt.cm.spectral(l / float(N_REGIONS))])


		plt.xticks(())
		plt.yticks(())
		title = 'Spectral clustering: %s, %.2fs' % (assign_labels, (t1 - t0))
		print(title)
		plt.title(title)
	plt.show()

def run2():
	lena = sp.misc.lena()
	# Downsample the image by a factor of 4
	lena = lena[::2, ::2] + lena[1::2, ::2] + lena[::2, 1::2] + lena[1::2, 1::2]
	lena = lena[::2, ::2] + lena[1::2, ::2] + lena[::2, 1::2] + lena[1::2, 1::2]

	# Convert the image into a graph with the value of the gradient on the
	# edges.
	graph = image.img_to_graph(lena)

	# Take a decreasing function of the gradient: an exponential
	# The smaller beta is, the more independent the segmentation is of the
	# actual image. For beta=1, the segmentation is close to a voronoi
	beta = 5
	eps = 1e-6
	graph.data = np.exp(-beta * graph.data / lena.std()) + eps

	# Apply spectral clustering (this step goes much faster if you have pyamg
	# installed)
	N_REGIONS = 11

	###############################################################################
	# Visualize the resulting regions

	for assign_labels in ('kmeans', 'discretize'):
	    t0 = time.time()
	    labels = spectral_clustering(graph, n_clusters=N_REGIONS,
	                                 assign_labels=assign_labels,
	                                 random_state=1)
	    t1 = time.time()
	    labels = labels.reshape(lena.shape)

	    plt.figure(figsize=(5, 5))
	    plt.imshow(lena,   cmap=plt.cm.gray)
	    for l in range(N_REGIONS):
	        plt.contour(labels == l, contours=1,
	                    colors=[plt.cm.spectral(l / float(N_REGIONS)), ])
	    plt.xticks(())
	    plt.yticks(())
	    plt.title('Spectral clustering: %s, %.2fs' % (assign_labels, (t1 - t0)))

	plt.show()