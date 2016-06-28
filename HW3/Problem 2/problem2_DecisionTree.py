# Braden Katzman - bmk2137
# Columbia University
# Artificial Intelligence Summer 2016
# HW3 - Question 2
# Description:
#	Decision Tree classifier with param option max_depth

from sklearn import tree
from sklearn.cross_validation import cross_val_score
from sklearn.metrics import accuracy_score

# Builds and returns a decision tree classifier given parameter max_depth
def decisionTree(max_depth):
	print "\nbuilding decision tree classifier with max_depth={max_depth}".format(max_depth=max_depth)
	dt = tree.DecisionTreeClassifier(max_depth=max_depth)
	return dt

# Trains and returns a trained SVM given parameters SVM, support vector (training), and y (labels)
def trainDT(dt, sv, y):
	print "\ntraining Logistic Regression Classifier"
	# cross validate 5 times
	scores = cross_val_score(dt, sv, y, cv=5)
	print scores # NEED TO REPORT THIS IN THE WRITE UP

	# fit the data to the labels
	dt.fit(sv, y)
	return dt

# Tests a Decision Tree Classifier on testing data and returns the prediction labels given parameters dt and v (testing data vector)
def runDT(dt, v):
	print "\npredicting labels with Logistic Regression Classifier"
	predictions = dt.predict(v)
	return predictions

# runs cross validation and optimizes for different c
def runCVAndOptimize(sv, y, x_test, y_true):
	print "\nrunning cross validation and optimizing"
	max_depth = [1., 2., 3., 4., 5., 6., 7., 8., 9., 10.]

	# for each c value
	for i in range(10):
		print 'Decision Tree max_depth=' + repr(max_depth[i])
		dt = decisionTree(max_depth[i])
		trainDT(dt, sv, y)
		accuracyTest(dt, "Decision Tree", x_test, y_true)

# makes predictions and prints the accuracies for the various SVMs
def accuracyTest(dt, type_, x_test, y_true):
	print type_ + " accuracy: " + repr(accuracy_score(y_true, runDT(dt, x_test)))