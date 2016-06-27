# Braden Katzman - bmk2137
# Columbia University
# Artificial Intelligence Summer 2016
# HW3 - Question 2
# Description: 
#	Used to render images


import matplotlib.pyplot as plt

def loadImagePlot(img, figure_num, axes, title):
	plt.figure(figure_num)
	plt.clf()
	ax = plt.axes(axes)
	plt.axis('off')
	plt.title(title)
	plt.imshow(img)

def showPlot():
	plt.show()