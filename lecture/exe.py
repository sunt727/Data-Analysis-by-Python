# # bag1 = [1, 30,3,5,7]
# # bag2 = [0,23,4,3]
# #
# # def A(bag1, bag2):
# # 	yield(bag1,bag2)
# #
# # print(A(bag1, bag2))
#
import random
#
# def replacementSimulation(numTrials):
# 	'''
# 	Runs numTrials trials of a Monte Carlo simulation
# 	of drawing 4 balls out of a bucket containing
# 	3 red and 3 green balls. Balls are replaced once
# 	drawn. Returns a decimal - the fraction of times 4
# 	red balls are drawn.
# 	'''
# 	balls = ['r'] * 3 + ['g'] * 3
# 	results = [[random.choice(balls) for j in range(4)] for i in range(numTrials)]
# 	return len([result for result in results if result == ['r'] * 4])/numTrials
#
# # print(replacementSimulation(10))
# # results = [random.random() for i in range(5000)]
# # print(len([result for result in results if result == 0.1])/5000)
# # print(len([result for result in results if 0 < result < 0.1])/5000)
#

def coin1():
	if random.random() < 0.5:
		return 'heads'
	else:
		return 'tails'


def coin2():
	if random.random() < 0.25:
		return 'heads'
	else:
		return 'tails'


# Example: The
# following
# code:
# random.seed(1)
# print(getFracs(coin1, 1000))
# print(getFracs(coin2, 1000))
# should
# print
# something
# similar
# to:
# [0.473, 0.504, 0.485, 0.511, 0.517, 0.488, 0.481, 0.532, 0.517, 0.515]
# [0.254, 0.235, 0.258, 0.246, 0.251, 0.251, 0.258, 0.237, 0.241, 0.251]

def getFracs(coin, numFlips):
	"""
	coin is a function that takes no arguments and
	non-deterministically returns 'heads' or 'tails'

	Runs 10 trials of numFlips each, and returns a list
	containing the fraction of heads for the flips of each
	trial.
	"""
	results = []
	for i in range(10):
		result = []
		for flip in range(numFlips):
			result.append(coin())
		r = 0
		for c in result:
			if c == 'heads':
				r += 1
		results.append(r/numFlips)
	return results

# random.seed(1)
# print(getFracs(coin1, 1000))
# print(getFracs(coin2, 1000))

def get_std(X):
	mean = sum(X)/float(len(X))
	tot = 0.0
	for x in X:
		tot += (x - mean)**2
	std = (tot/len(X))**0.5
	return std

def testCoin(coin, getFracs, interval, initialNumFlips):
	"""
	coin is a function that takes no arguments and
	non-deterministically returns 'heads' or 'tails'

	getFracs satisfies the specification of the function
	in problem 1

	interval is a positive float

	initialNumFlips is an integer

	returns an estimate of the probability of coins
	returning 'heads'. Your estimate should have a .95
	probability of having a difference from the true
	probability of no more than interval.
	"""
	numFlips = initialNumFlips
	means = []
	while True:
		fracHeads = getFracs(coin, numFlips)
		mean = sum(fracHeads)/float(len(fracHeads))
		means.append(mean)
		sd = get_std(fracHeads)
		if 2 * 1.96 * sd <= interval:
			return mean # sum(means)/float(len(means))


# 0.5046875
print(testCoin(coin1, getFracs, 0.05, 32))