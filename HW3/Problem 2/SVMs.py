
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
from sklearn.cross_validation import train_test_split
from sklearn.cross_validation import cross_val_score
from sklearn.metrics import accuracy_score

# split the raw data into 40% testing and 60% training
def testSplit(vectors, labels):
	train1, test1, trainL, testL = train_test_split(vectors, labels, test_size=0.4, random_state=42)
	return [train1, trainL], [test1, testL]

# Builds and returns a linear SVM given parameter C
def linearSVM(c):
	linSVM = svm.SVC(C=c, kernel='linear')
	return linSVM

# Builds and returns a polynomial SVM given parameters C and degrees
def polynomialSVM(c, deg):
	polySVM = svm.SVC(C=c, kernel='poly', degree=deg)
	return polySVM

# Builds and returns a Radial Basis Function SVM given parameters C and gamma
def rbfSVM(c, gamma):
	rbfSVM = smv.SVC(C=c, kernel='rbf', gamma=gamma)
	return rbfSVM

# Trains and returns a trained SVM given parameters SVM, support vector (training), and y (labels)
def trainSVM(svm, sv, y):
	# cross validate 5 times
	scores = cross_val_score(svm, sv, y, cv=5)

	# fit the data to the labels
	svm.fit(sv, y)
	return svm

# Tests a SVM on testing data and returns the prediction labels given parameters svm and v (testing data vector)
def runSVM(svm, v):
	predictions = svm.predict(v)
	return predictions

# runs cross validation and optimizes for different c, gamma, and degrees values given parameters support vector (training) and y (labels)
def runCVAndOptimize(sv, y):
	c = [1., 10., 100., 1000.]
	g = [0.001, 0.01, 0.1, 1, 10.]
	deg = [1, 2, 3, 4, 5]

	# for each c value
	for i in range(4):


		# for each degrees value
		for n in range(5):
			print 'Poly C=' + repr(c[i]) + 'Deg=' + repr(deg[n])
			poly = polynomialSVM(c[i], deg[n])
			trainSVM(poly, sv, y)




