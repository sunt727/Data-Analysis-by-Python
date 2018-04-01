###########################
# 6.0002 Problem Set 1: Space Cows
# Name: Tuo Sun
# Collaborators: None
# Time: 3:00
# Difficult sections / topics: Problem #5

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
def dp_make_weight(cow_weights, target_weight=0, memo=None):
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
	:param cow_weights:
	:param target_weight:
	:return:
	"""
	# Create a memo list with 0 ~ target number of 0
	if memo is None:
		memo = [0] * (target_weight + 1)
	INF = float('inf')  # Create infinite
	# Create a function to avoid mutate memo and return -INF to final result
	def maxN(N):
		maxCows = -INF  # make a maxCows as -INF
		if memo[N] > 0:  # if memo[N] is not 0, return the same memo[N] since it has already tested
			return memo[N]
		elif memo[N] < 0:
			return -INF
		else:  # if memo[N] is 0, it means not tested yet
			for weight in cow_weights:
				if N == weight:
					if memo[N] == 0:
						memo[N] = 1  # if it is the last round, return 1 or its original value tested before
					return memo[N]
				elif N < weight:
					memo[N] = -INF
				else:
					if memo[N - weight] >= 0:  # if next round is tested, return its value to save time
						cow = maxN(N - weight)+1  # A(N) + 1 times
						if cow > maxCows:
							maxCows = cow
							memo[N] = maxCows  # max to maxCows
			return maxCows  # avoid return Nonetype
	# Run the function here
	maxN(target_weight)
	m = memo[target_weight]
	# return result if it is either not tested yet (0) or no result (-INF), otherwise return None
	return m if m > 0 else None

if __name__ == '__main__':
	# Problem 1
	cow_weights = load_cows('ps1_cow_data.txt')
	print(cow_weights)
	# Problem 2
	print(greedy_cow_transport(cow_weights))
	# Problem 3
	print(brute_force_cow_transport(cow_weights))
	# Problem 4
	compare_cow_transport_algorithms()
	# Problem 5
	cow_weights1 = (3, 5, 8, 9)
	cow_weights2 = (13, 14, 15)
	cow_weights3 = (2, 4, 8)
	cow_weights4 = (3, 5, 8, 9, 15, 19, 22, 27, 28, 32, 36, 40, 51, 52, 53, 54, 60, 69, 73, 88, 91, 93, 102, 105)
	n = 63

	print("Cow weights = (3, 5, 8, 9)")
	print("n = 64")
	print("Expected ouput: 20 (3 * 18 + 2 * 5 = 64)")
	start = time.time()
	print("Actual output:", dp_make_weight(cow_weights1, 64))
	elapsed = time.time()
	print("It costs %6f sec" % (elapsed - start))
	# start = time.time()
	# print("Actual output:", dp_make_weight(cow_weights2, 28))
	# elapsed = time.time()
	# print("It costs %6f sec" % (elapsed - start))
	# start = time.time()
	# print("Actual output:", dp_make_weight(cow_weights4, 1000))
	# elapsed = time.time()
	# print("It costs %6f sec" % (elapsed - start))
	# start = time.time()
	# print("Actual output:", dp_make_weight(cow_weights3, 63))
	# elapsed = time.time()
	# print("It costs %6f sec" % (elapsed - start))
	pass
