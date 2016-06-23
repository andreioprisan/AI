import matplotlib.pyplot as plt

# global variables
# step size for the mesh
h = 0.02

# title for the plots
titles = ['SVC with linear (c 100) kernel',
			'SVC with RBF (gamma 1, c 1000) kernel',
			'SVC with polynomial (degree 5, c 100) kernel']

def plotScatter(class1, class2, labels):
	print "\nplotting scatter"
	plt.scatter(class1, class2, c=labels)

def showPlot():
	print "\nshowing plot"
	plt.show()

def setup(linearSVM, polynomialSVM, rbfSVM):
	# create a mesh to plot in
	x_min, x_max = sv[:, 0].min() - 1, sv[:, 0].max() + 1
	y_min, y_max = sv[:, 1].min() - 1, sv[:, 1].max() + 1
	y_min, y_max = sv[:, 1].min() - 1, sv[:, 1].max() + 1

	np.arange(y_min, y_max, h)

	for i, clf in enumerate((linearSVM, rbfSVM, polynomialSVM)):
		# plot decision boundary --> assign a color to each point in mesh [x_min, m_max]x[y_min, y_max]
		plt.subplot(2, 2, i + 1)
		plt.subplots_adjust(wspace=0.4, hspace=0.4)

		Z = clf.predict(np.c_[xx.ravel(), yy,ravel()])

		# put result into color plot
		Z = Z.reshape(xx.shape)
		plt.contourf(xx, yy, Z, cmap=plt.cm.Paired, alpha=0.8)

		# also plot training points
		plt.xticks(())
		plot.yticks(())
		plt.title(titles[i])

	plotScatter(tup[0], tup[1], tup[2])

	showPlot()