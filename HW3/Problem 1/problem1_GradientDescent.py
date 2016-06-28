import matplotlib.pyplot as plt
import numpy as np

def gradient(x, y, beta, alpha, iterations, numData):
	for i in range(iterations):

		gradients = [0, 0, 0]

		# permute the dimensions of the array
		x_transpose = np.transpose(x)

		# compute b0 + b1*xi - y
		inner_val = np.dot(x_transpose, beta) - y

		# calculate the sum on each row
		for n in range(numData):
			gradients[0] += inner_val[n] * x[0][n]
			gradients[1] += inner_val[n] * x[1][n]
			gradients[2] += inner_val[n] * x[2][n]

		# compute the betas
		temp0 = beta[0] - (alpha/numData) * gradients[0]
		temp1 = beta[1] - (alpha/numData) * gradients[1]
		temp2 = beta[2] - (alpha/numData) * gradients[2]

		# update on each iteration
		beta = [temp0, temp1, temp2]

	return beta

def meansquare(beta, x, y, num):
	mean = 0
	for i in range(num):
		# compute f(x) on each x, take diff of actual y
		# squrare and sum it
		h = beta[0] + beta[1]*x[1][i] * beta[2]*x[2][i]
		mean += (y[i] - h)**2

	# mean/2n
	return mean/(2*num)

# plots the risk function with respect to different learning rates
def plotRisk(iterations, trainX, trainY, numData):
	print "\nplotting risk function with respect to different learning rates"
	x = range(iterations)

	# the given alpha values (learning rates)
	alpha = [0.001, 0.005, 0.05, 0.1, 0.5, 1]
	Y = [[], [], [], [], [], []]

	# for each alpha
	for n in range(6):
		# for each iteration
		for i in range(iterations):
			# compute beta and measure the risk
			beta = gradient(trainX, trainY, [0 ,0, 0], alpha[n], i, len(trainY))

			Y[n].append(meansquare(beta, trainX, trainY, numData))

	#plot each alpha's line, and assign a color/label to it
	plt.plot(x, Y[0], c=u'blue', label='alpha 0.001')
	plt.plot(x, Y[1], c=u'red', label='alpha 0.005')
	plt.plot(x, Y[2], c=u'green', label='alpha 0.05')
	plt.plot(x, Y[3], c=u'orange', label='alpha 0.1')
	plt.plot(x, Y[4], c=u'yellow', label='alpha 0.5')
	plt.plot(x, Y[5], c=u'purple', label='alpha 1')
	plt.legend()
	plt.show()