# Braden Katzman - bmk2137
# Columbia University
# Artificial Intelligence Summer 2016
# HW3 - Question 2
# Description:
#	Logistic regression classifier with param options C and max_iter

from sklearn import linear_model

# Builds and returns a logistic regression classifier given parameters C and tol (tolerance)
def linearSVM(c, tol):
	print "\nbuilding logisitc regression classifier with C={c}, tol={tol}".format(c=c, tol=tol)
	logreg = linear_model.LogisticRegression(C=c, tol=tol)
	return logreg

# Trains and returns a trained SVM given parameters SVM, support vector (training), and y (labels)
def trainLogReg(lr, sv, y):
	print "\ntraining Logistic Regression Classifier"
	# cross validate 5 times
	scores = cross_val_score(lr, sv, y, cv=5)
	# print scores NEED TO REPORT THIS IN THE WRITE UP

	# fit the data to the labels
	lr.fit(sv, y)
	return svm

# Tests a Logistic Regression Classifier on testing data and returns the prediction labels given parameters lr and v (testing data vector)
def runSVM(lr, v):
	print "\npredicting labels with Logistic Regression Classifier"
	predictions = lr.predict(v)
	return predictions