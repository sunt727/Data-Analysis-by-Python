###########################
# 6.0002 Problem Set 1: Space Cows
# Name: Tuo Sun
# Collaborators: None
# Time: 2:30
# Difficult sections / topics: Problem #2

from ps1_partition import get_partitions
import time
import copy


# ================================
# Part A: Transporting Space Cows
# ================================

# Problem 1
def load_cows(filename):
	"""
	Read the contents of the given file.  Assumes the file contents contain
	data in the form of comma-separated cow weight, name pairs, and return a
	dictionary containing cow names as keys and corresponding weights as values.

	Parameters:
	filename : the name of the data file as a string

	Returns:
	a dictionary containing cow names (string) as keys, and the corresponding
	weight (int) as the value
	for ex: {'Matt': 3, 'Kaitlin': 3, 'Katy': 5}
	"""
	with open(filename) as f:
		# with open the file and read the data from it
		read_data = f.read()
		# split data into lines and then split them by comma
		rl = [rl.split(',') for rl in read_data.split('\n') if rl is not '']
		# return a dictionary that uses second item in the previous list as keys and first item as values
		return {i[1]: int(i[0]) for i in rl}


# Problem 2
def greedy_cow_transport(cows, limit=10):
	"""
	Uses a greedy heuristic to determine an allocation of cows that attempts to
	minimize the number of spaceship trips needed to transport all the cows. The
	returned allocation of cows may or may not be optimal.
	The greedy heuristic should follow the following method:

	1. As long as the current trip can fit another cow, add the largest cow that will fit
		to the trip
	2. Once the trip is full, begin a new trip to transport the remaining cows

	Does not mutate the given dictionary of cows.

	Parameters:
	cows : a dictionary of names (string), weights (int)
	limit : weight limit of the spaceship (an int)

	Returns:
	A list of lists, with each inner list containing the names of cows
	transported on a particular trip and the overall list containing all the
	trips
	"""
	# create empty overall trip list and copy the cows dictionary to avoid mutate it
	overall = []
	remain_cows = cows.copy()
	# start a while loop to iterate until no cow is in the list
	while list(remain_cows.keys()):
		# set start status of current trip list and current quota left
		quota = limit
		trip = []
		# start a while loop to iterate every trip until the quota is not enough to add more cows
		while list(remain_cows.values()) and quota >= min(list(remain_cows.values())):
			# pick up the cow with maximum weight in the list and put it into the trip list
			maxcow = max(list(remain_cows.keys()), key=lambda x: remain_cows[x] if remain_cows[x] <= quota else 0)
			trip.append(maxcow)
			# get the remain quota and delete the picked-up cow from the cows' list
			quota -= cows[maxcow]
			del remain_cows[maxcow]
		# once a trip loop end, add the trip into overall list and iterate
		# from reset the current trip list and current quota left
		overall.append(trip)
	# return the A list of lists, with each inner list containing the names of cows
	# transported on a particular trip and the overall list containing all the trips
	return overall


# Problem 3
def brute_force_cow_transport(cows, limit=10):
	"""
	Finds the allocation of cows that minimizes the number of spaceship trips
	via brute force.  The brute force algorithm should follow the following method:

	1. Enumerate all possible ways that the cows can be divided into separate trips
		Use the given get_partitions function in ps1_partition.py to help you!
	2. Select the allocation that minimizes the number of trips without making any trip
		that does not obey the weight limitation

	Does not mutate the given dictionary of cows.

	Parameters:
	cows : a dictionary of names (string), and weights (int)
	limit : weight limit of the spaceship (an int)

	Returns:
	A list of lists, with each inner list containing the names of cows
	transported on a particular trip and the overall list containing all the
	trips
	"""
	# get partitions from cows name list
	# iterate the sorted list with sublist's length, which means overall list with minimum trips iterates first
	for overall in sorted(get_partitions(list(cows.keys())), key=len):
		# if all trip lists in a overall list can satisfy the limit requirement, then return this overall list
		if all(sum(cows[cow] for cow in trip) <= limit for trip in overall):
			return overall


# Problem 4
def compare_cow_transport_algorithms():
	"""
	Using the data from ps1_cow_data.txt and the specified weight limit, run your
	greedy_cow_transport and brute_force_cow_transport functions here. Use the
	default weight limits of 10 for both greedy_cow_transport and
	brute_force_cow_transport.

	Print out the number of trips returned by each method, and how long each
	method takes to run in seconds.

	Returns:
	Does not return anything.
	"""
	# load cows dictionary with their weights
	cow_weights = load_cows('ps1_cow_data.txt')
	# start the greedy_cow_transport test with start time and end time, using default limit times
	start = time.time()
	greedy = len(greedy_cow_transport(cow_weights))
	elapsed = time.time()
	print("greedy_cow_transport uses %d times to transport all cows and costs %6f sec" % (greedy, elapsed - start))
	# start the brute_force_cow_transport test with start time and end time, using default limit times
	start = time.time()
	greedy = len(brute_force_cow_transport(cow_weights))
	elapsed = time.time()
	print("brute_force_cow_transport uses %d times to transport all cows and costs %6f sec" % (greedy, elapsed - start))


# Problem 5
def dp_make_weight(cow_weights, target_weight, memo=None):
	"""
	Find largest number of cows that can be brought back. Assumes there is
	an infinite supply of cows of each weight in cow_weights.

	Parameters:
	cow_weights   : tuple of ints, available cow weights sorted from smallest to
					largest value (d1 < d2 < ... < dk)
	target_weight : int, amount of weight the spaceship can carry
	memo          : dictionary, OPTIONAL parameter for memoization (you may not
					need to use this parameter depending on your implementation,
					dont delete though!)

	Returns:
	int, largest number of cows that can be brought back whose weight
	equals target_weight.
	None, if no combinations of weights equal target_weight
	"""
	# # iterate the number from small weight because it can result in larger output number of cows
	# for cow_weight in cow_weights:
	# 	# store the round division of target weight to this cow weight as current max number
	# 	max_num = target_weight//cow_weight
	# 	# return max number in case that this cow weight can fit the target weights
	# 	if target_weight % cow_weight == 0:
	# 		return int(max_num)
	# 	# if remaining target number cannot be dividable by all remain cow weights than max number minus one
	# 	while all((target_weight - (max_num * cow_weight)) % x != 0 for x in cow_weights) and (max_num >= 1):
	# 		max_num -= 1
	# 	# if any available number can satisfy the requirement, find it can return the revised max number
	# 	for x in cow_weights:
	# 		if (target_weight - (max_num * cow_weight)) % x == 0:
	# 			return int(max_num + ((target_weight - (max_num * cow_weight))/x))
	# 	# automatically return None if none thing returns
	# cw = list(cow_weights)
	# cw.reverse()
	#cw = list(cow_weights)
	# solution = [i for x in cw for i in range((target_weight//x)+1)]
	solutions = {}
	def alg(N):
		if solutions.get(N, 0) > 0:
			return solutions.get(N, 0)
		else:
			for weight in cow_weights:
				if N > weight:
					if alg(N-weight) is not None:
						for i in list(solutions.keys()):
							if N % i == 0:
								solutions[N] = max(solutions.get(N, 0), alg(i) * int(N/i))
						solutions[N] = max(solutions.get(N, 0), alg(N-weight) + 1)
				elif N == weight:
					solutions[N] = max(solutions.get(N, 0), 1)
					return solutions[N]

	# def matrix(a=[]):
	# 	l = []
	# 	x = a.pop(0)
	# 	if a:
	# 		for i in range((target_weight // x) + 1):
	# 			l += [i] + matrix(a)
	#
	# 	else:
	# 		for i in range((target_weight // x) + 1):
	# 			return [i]
	# 	return l
	# print(matrix(a=cw))

	# def findfit(dict, i):
	# 	s = cw[i]
	# 	for j in range(target_weight // cw[i]):
	# 		if sum(x * dict[x] for x in cw) == target_weight:
	# 			memo.append(list(dict.values()))
	# 		else:
	# 			if i != len(cw)-1:
	# 				findfit(dict, i + 1)
	# 				# n = cw[i + 1]
	# 				# dict[n] = target_weight // n
	# 			else:
	# 				dict[s] = dict[s] - 1


	# while sum(x * solution[x] for x in cw) != target_weight:
	# for i in range(len(cow_weights)):
	#sl = solution.copy()
	# 	findfit(sl, i)
	# findfit(solution, 0)
	alg(target_weight)
	return solutions[target_weight]
	#return sum(max(memo, key=sum)) if memo else None


# EXAMPLE TESTING CODE, feel free to add more if you'd like
if __name__ == '__main__':
	# # Problem 1
	# 	cow_weights = load_cows('ps1_cow_data.txt')
	# 	print(cow_weights)
	# # Problem 2
	# 	print(greedy_cow_transport(cow_weights))
	# # Problem 3
	# 	print(brute_force_cow_transport(cow_weights))
	# # Problem 4
	# 	compare_cow_transport_algorithms()
	# Problem 5
	cow_weights = (3, 5, 8, 9)
	# cow_weights = (13, 14, 15)
	n = 64
	print("Cow weights = (3, 5, 8, 9)")
	print("n = 64")
	print("Expected ouput: 20 (3 * 18 + 2 * 5 = 64)")
	start = time.time()
	print("Actual output:", dp_make_weight(cow_weights, n))
	elapsed = time.time()
	print("Actual output:", dp_make_weight(cow_weights, n))
	print("It costs %6f sec" % (elapsed - start))
	pass
