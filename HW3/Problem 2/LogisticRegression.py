# Braden Katzman - bmk2137
# Columbia University
# Artificial Intelligence Summer 2016
# HW3 - Question 2
# Description:
#	Logistic regression classifier with param option C 

from sklearn import linear_model
from sklearn.cross_validation import cross_val_score
from sklearn.metrics import accuracy_score

# Builds and returns a logistic regression classifier given parameters C and tol (tolerance)
def logReg(c):
	print "\nbuilding logisitc regression classifier with C={c}".format(c=c)
	logreg = linear_model.LogisticRegression(C=c)
	return logreg

# Trains and returns a trained SVM given parameters SVM, support vector (training), and y (labels)
def trainLogReg(lr, sv, y):
	print "\ntraining Logistic Regression Classifier"
	# cross validate 5 times
	scores = cross_val_score(lr, sv, y, cv=5)
	print scores # NEED TO REPORT THIS IN THE WRITE UP

	# fit the data to the labels
	lr.fit(sv, y)
	return lr

# Tests a Logistic Regression Classifier on testing data and returns the prediction labels given parameters lr and v (testing data vector)
def runLR(lr, v):
	print "\npredicting labels with Logistic Regression Classifier"
	predictions = lr.predict(v)
	return predictions

# runs cross validation and optimizes for different c
def runCVAndOptimize(sv, y):
	print "\nrunning cross validation and optimizing"
	c = [1., 10., 100., 1000.]

	# for each c value
	for i in range(4):
		print 'Log Reg C=' + repr(c[i])
		logreg = logReg(c[i])
		trainLogReg(logreg, sv, y)

# makes predictions and prints the accuracies for the various SVMs
def accuracyTest(logReg, x_test, y_true):
	print "\nLogistic Regression Accuracy: " + repr(accuracy_score(y_true, runLR(logReg, x_test)))