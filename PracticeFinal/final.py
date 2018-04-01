import numpy as np

def find_combination(choices, total):
	"""
	choices: a non-empty list of ints
	total: a positive int

	Returns result, a numpy.array of length len(choices)
	such that
		* each element of result is 0 or 1
		* sum(result*choices) == total
		* sum(result) is as small as possible
	In case of ties, returns any result that works.
	If there is no result that gives the exact total,
	pick the one that gives sum(result*choices) closest
	to total without going over.
	"""
	# # if memo is None:
	# # 	memo = {n: 0 for n in range(len(choices))}
	# memo = {}
	# # if result is None:
	# choices_copy = choices[:]
	# total_copy = total
	#
	# while sum(choices) > 0:
	# 	result = np.array([0] * len(choices))
	# 	result_copy = result
	# 	while total > 0 and sum(choices) > 0:
	# 		for j in range(len(choices)):
	# 			if choices[j] > total:
	# 				choices[j] = 0
	# 		if total > max(choices):
	# 			total -= max(choices)
	# 			i = choices.index(max(choices))
	# 			choices[i] = 0
	# 			result[i] = 1
	# 		else:
	# 			result[choices.index(total)] = 1
	# 			memo[sum(result)] = result
	# 			break
	# 	prev_sum = sum(memo.get(sum(result), result_copy)*choices_copy)
	# 	prev_len = sum(memo.get(sum(result), result_copy))
	#
	#
	# 	if total_copy >= sum(result):
	# 		if total_copy - sum(result*choices_copy) < total_copy - prev_sum:
	# 			memo[sum(result)] = result
	# 		elif sum(result*choices_copy) == prev_sum:
	# 			if prev_len == 0 or sum(result) < prev_len:
	# 				memo[sum(result)] = result
	#
	# 	choices = choices_copy
	# 	i = choices.index(max(choices))
	# 	choices[i] = 0
	# return memo  # [min(memo.keys(), key=lambda x: total_copy - sum(memo[x]*choices_copy))]  # if total_copy >= sum(memo[x]*choices_copy) else total_copy)]

	result = np.array([0] * len(choices))
	counter = 1
	while len(bin(counter)[2:]) <= len(choices):
		a = np.array(list(map(int, bin(counter)[2:].zfill(len(choices)))))

		if sum(a*choices) <= total:
			if sum(a*choices) > sum(result*choices):
				result = a
			elif sum(a*choices) == sum(result*choices):
				if sum(a) < sum(result):
					result = a
		counter += 1
	return result


print(find_combination([1,2,2,3], 4))
print(find_combination([1,1,3,5,3], 5))
print(find_combination([1,1,1,9], 4))
print(find_combination([3, 10, 2, 1, 5], 12))  # array([0, 1, 1, 0, 0])
print(find_combination([10, 100, 1000, 3, 8, 12, 38], 1171))  # array([1, 1, 1, 1, 1, 1, 1])
print(find_combination([21, 15, 100, 19, 12], 12))  #array([0, 0, 0, 0, 1])
print(find_combination([10, 10, 11, 11, 11], 20))  # array([1, 1, 0, 0, 0])
print(find_combination([4, 6, 3, 5, 2], 10))  # array([1, 1, 0, 0, 0])
print(find_combination([1, 3, 4, 2, 5], 16))  # array([1, 1, 1, 1, 1])
print(find_combination([105, 10, 9, 6, 4], 120))  # array([1, 0, 1, 1, 0])
print(find_combination([4, 10, 3, 5, 8], 1))  # array([0, 0, 0, 0, 0])
print(find_combination([1, 81, 3, 102, 450, 10], 9))  # array([1, 0, 1, 0, 0, 0])
print(find_combination([1], 10))  # array([1])

import random
# def same3infirst3draw():
# 	balls = ['r'] * 4 + ['g'] * 4
# 	drawn = []
# 	for i in range(3):
# 		drawn.append(balls.pop(random.randint(0, len(balls)-1)))
# 	return drawn == ['r'] * 3 or drawn == ['g'] * 3
#
# def drawing_without_replacement_sim(numTrials):
# 	'''
# 	Runs numTrials trials of a Monte Carlo simulation
# 	of drawing 3 balls out of a bucket containing
# 	4 red and 4 green balls. Balls are not replaced once
# 	drawn. Returns a float - the fraction of times 3
# 	balls of the same color were drawn in the first 3 draws.
# 	'''
# 	match = 0
# 	for n in range(numTrials):
# 		if same3infirst3draw():
# 			match += 1
# 	return match/numTrials

# print(drawing_without_replacement_sim(10000))

def greedySum(L, s):
	""" input: s, positive integer, what the sum should add up to
			   L, list of unique positive integers sorted in descending order
		Use the greedy approach where you find the largest multiplier for
		the largest value in L then for the second largest, and so on to
		solve the equation s = L[0]*m_0 + L[1]*m_1 + ... + L[n-1]*m_(n-1)
		return: the sum of the multipliers or "no solution" if greedy approach does
				not yield a set of multipliers such that the equation sums to 's'
	"""
	result = [0] * len(L)
	j = 0
	while j <= len(L) - 1:
		result[j] += (s // L[j])
		if s % L[j] == 0:
			return sum(result)
		else:
			s = s % L[j]
			j += 1
	return "no solution"

print()

# import random
# def same3infirst3draw1():
# 	L = [i for i in range(10)]
# 	drawn = []
# 	for i in range(4):
# 		drawn.append(random.choices(L))
# 	return drawn == sorted(drawn)
#
# def drawing_without_replacement_sim1(numTrials):
# 	'''
# 	Runs numTrials trials of a Monte Carlo simulation
# 	of drawing 3 balls out of a bucket containing
# 	4 red and 4 green balls. Balls are not replaced once
# 	drawn. Returns a float - the fraction of times 3
# 	balls of the same color were drawn in the first 3 draws.
# 	'''
# 	match = 0
# 	for n in range(numTrials):
# 		if same3infirst3draw1():
# 			match += 1
# 	return match/numTrials
#
# print(drawing_without_replacement_sim1(10000))