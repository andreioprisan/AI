
# Braden Katzman - bmk2137
# Columbia University
# Artificial Intelligence Summer 2016
# HW3 - Question 2
# Description: 
#	Builds linear, polynomial, and Radial Basis Function Support Vector Machines
#	Trains SVMs on training data
#	Predicts using SVMS on testing data	
#
#	Features of SVM usage included:
#		- Cross Validation
#		- Metrics

from sklearn import svm
from sklearn.cross_validation import cross_val_score
from sklearn.metrics import accuracy_score

# Builds and returns a linear SVM given parameter C
def linearSVM(c):
	# print "\nbuilding linear SVM with C={c}".format(c=c)
	linSVM = svm.SVC(C=c, kernel='linear')
	return linSVM

# Builds and returns a polynomial SVM given parameters C and degrees
def polynomialSVM(c, deg):
	# print "\nbuilding polynomial SVM with C={c} and Degrees={d}".format(c=c, d=deg)
	polySVM = svm.SVC(C=c, kernel='poly', degree=deg)
	return polySVM

# Builds and returns a Radial Basis Function SVM given parameters C and gamma
def rbfSVM(c, gamma):
	# print "\nbuilding Radial Basis Function SVM with C={c} and Gamme={g}".format(c=c, g=gamma)
	rbfSVM = svm.SVC(C=c, kernel='rbf', gamma=gamma)
	return rbfSVM

# Trains and returns a trained SVM given parameters SVM, support vector (training), and y (labels)
def trainSVM(svm, sv, y):
	# print "\ntraining SVM"
	# cross validate 5 times
	scores = cross_val_score(svm, sv, y, cv=5)
	print scores

	# fit the data to the labels
	svm.fit(sv, y)
	return svm

# Tests a SVM on testing data and returns the prediction labels given parameters svm and v (testing data vector)
def runSVM(svm, v):
	# print "\npredicting labels with SVM"
	predictions = svm.predict(v)
	return predictions

# runs cross validation and optimizes for different c, gamma, and degrees values given parameters support vector (training) and y (labels)
def runCVAndOptimize(sv, y, x_test, y_true):
	print "\nrunning cross validation and optimizing"
	c = [1., 10., 100., 1000.]
	g = [0.001, 0.01, 0.1, 1, 10.]
	deg = [1, 2, 3, 4, 5]

	# for each c value
	for i in range(4):
		print "Linear C=" + repr(c[i])
		linear = linearSVM(c[i])
		trainSVM(linear, sv, y)
		singleAccuracyTest(linear, "linear", x_test, y_true)

		# for each degrees value
		for n in range(5):
			print "Poly C=" + repr(c[i]) + " Deg=" + repr(deg[n])
			poly = polynomialSVM(c[i], deg[n])
			trainSVM(poly, sv, y)
			singleAccuracyTest(poly, "polynomial", x_test, y_true)

			print "RBF C=" + repr(c[i]) + " Deg=" + repr(deg[n])
			rbf = rbfSVM(c[i], deg[n])
			trainSVM(rbf, sv, y)
			singleAccuracyTest(rbf, "RBF", x_test, y_true)

def singleAccuracyTest(svm, type_, x_test, y_true):
	print type_ + " accuracy: " + repr(accuracy_score(y_true, runSVM(svm, x_test)))

# makes predictions and prints the accuracies for the various SVMs
def accuracyTest(lin, poly, rbf, x_test, y_true):
	print "\nlinear accuracy: " + repr(accuracy_score(y_true, runSVM(lin, x_test)))
	print "polynomial accuracy: " + repr(accuracy_score(y_true, runSVM(poly, x_test)))
	print "rbf accuracy: " + repr(accuracy_score(y_true, runSVM(rbf, x_test)))


