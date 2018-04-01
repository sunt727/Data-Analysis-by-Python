# 6.0002 Problem Set 2
# Graph Optimization
# Name: Tuo Sun
# Collaborators: None
# Time: 3:30

#
# Finding shortest paths through MIT buildings
#
import unittest
from graph import Digraph, Node, WeightedEdge

#
# Problem 2: Building up the Campus Map
#
# Problem 2a: Designing your graph
#
# What do the graph's nodes represent in this problem? What
# do the graph's edges represent? Where are the distances
# represented?

# Answer:
# Nodes represent buildings and edges represent the path from one building to another one.
# The distances represent the length of from one building to another one.


# Problem 2b: Implementing load_map
def load_map(map_filename):
	"""
	Parses the map file and constructs a directed graph

	Parameters:
		map_filename : name of the map file

	Assumes:
		Each entry in the map file consists of the following three positive
		integers, separated by a blank space:
			From To TotalDistance
		e.g.
			32 76 54
		This entry would become an edge from 32 to 76.

	Returns:
		a directed graph representing the map
	"""
	print("Loading map from file...")
	with open(map_filename) as m:
		# with open the map file and read the data from it
		read_data = m.read()
		# split data into lines and then split them by space to [start, end, length]
		rl = [rl.split(' ') for rl in read_data.split('\n') if rl is not '']
		# create a new graph
		g = Digraph()
		for path in rl:
			src, dest = Node(path[0]), Node(path[1])  # create new nodes (start, end)
			for n in (src, dest):  # try to add nodes, if they are exist, pass
				try:
					g.add_node(n)
				except ValueError:
					pass
			try:
				# try to add the edge, if they are exist, pass
				e = WeightedEdge(src, dest, path[2])
			except ValueError:
				pass
			g.add_edge(e)
		return g

# Problem 2c: Testing load_map
# Include the lines used to test load_map below, but comment them out

# Loading map from file...
# a->b (10)
# a->c (12)
# b->c (1)
#
# Problem 3: Finding the Shortest Path using Optimized Search Method
#
# Problem 3a: Objective function
#
# What is the objective function for this problem? What are the constraints?
#
# Answer: objective function is the shortest path function of series of nodes;
# the constraints are 1) we can never go to a node which passed before; 2) we can only follow
# the direction from source to destination of a path; 3) we have a start node and a end node
# 4) we can not pass too many large-numbered buildings.

# Problem 3b: Implement get_best_path
def get_best_path(digraph, start, end, path, max_sum_buildings, best_dist,
				  best_path):
	"""
	Finds the shortest path between buildings subject to constraints.

	Parameters:
		digraph: instance of Digraph or one of its subclasses
			The graph on which to carry out the search
		start: string
			Building number at which to start
		end: string
			Building number at which to end
		path: list composed of [[list of strings], int, int]
			Represents the current path of nodes being traversed. Contains
			a list of node names, total distance traveled, and total
			sum of building numbers.
		max_sum_buildings: int
			Maximum sum of building numbers a path can visit
		best_dist: int
			The smallest distance between the original start and end node
			for the initial problem that you are trying to solve
		best_path: list of strings
			The shortest path found so far between the original start
			and end node.

	Returns:
		A tuple of the form (best_dist, best_path).
		The first item is an integer, the length (distance traveled)
		of the best path.
		The second item is the shortest-path from start to end, represented by
		a list of building numbers (in strings).

		If there exists no path that satisfies max_total_dist and
		max_sum_buildings constraints, then return None.
	"""
	agenda = [path]  # use agenda as a stack for DFS
	solutions = []  # create an empty list for holding available solutions

	while agenda:  # while loop until no potential path in the agenda
		path_wl = agenda.pop(0)  # pop up the top one from the stack (agenda)
		this_path, this_dist, this_sum_bldg = path_wl  # get the this_path/this_dist/this_sum_bldg separately
		if this_sum_bldg <= max_sum_buildings:  # stop the loop when exceeding maximum sum of bldg
			if this_path[-1] == end:
				solutions += [path_wl]  # when reaching the goal, add the path into available solutions
				if this_dist < best_dist:  # if the new path is shorter than best one, revise the best
					best_path = this_path
					best_dist = this_dist
			else:
				for edge in digraph.get_edges_for_node(Node(this_path[-1])):  # get next edges/nodes
					dest = edge.get_destination().get_name()
					if dest not in this_path:  # avoid cycles
						path_copy = path_wl.copy()  # avoid mutate original path
						path_copy[0] = this_path + [dest]  # update the path/total distance/sum of bldg
						path_copy[1] += edge.get_total_distance()
						path_copy[2] += edge.get_destination().get_building_num()
						if path_copy[2] <= max_sum_buildings and path_copy[1] <= best_dist:
							agenda += [path_copy]  # add the path to agenda if there is no violation against our rules
				agenda = sorted(agenda, key=lambda x: (x[1], x[0]))

	solutions = sorted(solutions, key=lambda x: (x[1], x[0]))  # sorted the solution list by total distance
	if solutions:
		return solutions[0][1], solutions[0][0]  # return best path's total distance and this path
	else:
		return None, None  # return both total distance


def directed_dfs(digraph, start, end, max_total_dist, max_sum_buildings):
	"""
	Finds the shortest path from start to end using a directed depth-first
	search. The total distance traveled on the path must not
	exceed max_total_dist, and the sum of building numbers on this path must
	not exceed max_sum_buildings.

	Parameters:
		digraph: instance of Digraph or one of its subclasses
			The graph on which to carry out the search
		start: string
			Building number at which to start
		end: string
			Building number at which to end
		max_total_dist: int
			Maximum total distance on a path
		max_sum_buildings: int
			Maximum sum of building numbers a path can visit

	Returns:
		The shortest-path from start to end, represented by
		a list of building numbers (in strings).

		If there exists no path that satisfies max_total_dist and
		max_sum_buildings constraints, then raises a ValueError.
	"""
	best_dist = float('inf')  # initiate best distance as infinite
	best_path = None
	path = [[start], 0, Node(start).get_building_num()]  # initiate path with only start node and its building number
	best_dist, best_path = get_best_path(digraph, start, end, path, max_sum_buildings, max_total_dist, best_path)
	if best_path is None or best_dist > max_total_dist:  # check whether there is no solution or excessive solution
		raise ValueError("No path from {} to {}".format(start, end))
	return best_path


class Ps2Test(unittest.TestCase):
	LARGE_NUM_NODES = 99999

	def setUp(self):
		self.graph = load_map("mit_map.txt")

	def test_load_map_basic(self):
		self.assertTrue(isinstance(self.graph, Digraph))
		self.assertEqual(len(self.graph.nodes), 37)
		all_edges = []
		for _, edges in self.graph.edges.items():
			all_edges += edges  # edges must be dict of node -> list of edges
		all_edges = set(all_edges)
		self.assertEqual(len(all_edges), 133)

	def _print_path_description(self, start, end, total_dist, buildings_sum):
		constraint = ""
		if buildings_sum != Ps2Test.LARGE_NUM_NODES:
			constraint = "visiting buildings whose numbers add up to no more than {}".format(
				buildings_sum)
		if total_dist != Ps2Test.LARGE_NUM_NODES:
			if constraint:
				constraint += ' or {}m total'.format(total_dist)
			else:
				constraint = "without walking more than {}m total".format(
					total_dist)

		print("------------------------")
		print("Shortest path from Building {} to {} {}".format(
			start, end, constraint))

	def _test_path(self,
				   expectedPath,
				   total_dist=LARGE_NUM_NODES,
				   buildings_sum=LARGE_NUM_NODES):
		start, end = expectedPath[0], expectedPath[-1]
		self._print_path_description(start, end, total_dist, buildings_sum)
		dfsPath = directed_dfs(self.graph, start, end, total_dist, buildings_sum)
		print("Expected: ", expectedPath)
		print("DFS: ", dfsPath)
		self.assertEqual(expectedPath, dfsPath)

	def _test_impossible_path(self,
							  start,
							  end,
							  total_dist=LARGE_NUM_NODES,
							  buildings_sum=LARGE_NUM_NODES):
		self._print_path_description(start, end, total_dist, buildings_sum)
		try:
			path = directed_dfs(self.graph, start, end, total_dist, buildings_sum)
			print(path)
			self.fail()
		except:
			with self.assertRaises(ValueError):
				directed_dfs(self.graph, start, end, total_dist, buildings_sum)

	def test_path_one_step(self):
		self._test_path(expectedPath=['32', '56'])

	def test_path_unlimited_sum(self):
		self._test_path(
			expectedPath=['10','13', '9'], buildings_sum=Ps2Test.LARGE_NUM_NODES)

	def test_path_smaller_sum(self):
		self._test_path(
			expectedPath=['10','4', '9'], buildings_sum=23)

	def test_path_multi_step(self):
		self._test_path(expectedPath=['2', '3', '7', '9'])

	def test_with_no_limit_sum(self):
		self._test_path(
			expectedPath=['1', '3', '10', '13', '31', '37'],
			buildings_sum=Ps2Test.LARGE_NUM_NODES)

	def test_with_exact_sum(self):
		self._test_path(
			expectedPath=['1', '3', '10', '13', '31', '37'],
			buildings_sum=sum([1, 3,10, 13, 31, 37]))

	def test_with_exact_sum_minus_one(self):
		self._test_path(
			expectedPath=['1', '2', '10', '13', '31', '37'],
			buildings_sum=sum([1, 3,10, 13, 31, 37])-1)

	def test_with_start_end_sum(self):
		self._test_path(
			expectedPath=['32', '76'],
			buildings_sum=108)

	def test_without_start_end_sum(self):
		self._test_path(
			expectedPath=['32', '57', '76'],
			buildings_sum=Ps2Test.LARGE_NUM_NODES)

	def test_path_multi_step2(self):
		self._test_path(expectedPath=['1', '4', '8', '16', '56', '32'], buildings_sum=Ps2Test.LARGE_NUM_NODES  )

	def test_impossible_path1(self):
		self._test_impossible_path('2', '1', buildings_sum=2)

	def test_impossible_path2(self):
		self._test_impossible_path('31', '38', buildings_sum=39)

	def test_impossible_path3(self):
		self._test_impossible_path('37', '33', buildings_sum=69)

	def test_impossible_path4(self):
		self._test_impossible_path('1', '10', buildings_sum=11)



if __name__ == "__main__":
	unittest.main(verbosity=2)
	# suite = unittest.TestLoader().loadTestsFromTestCase(Ps2Test)
	# unittest.TextTestRunner(verbosity=2).run(suite)

# graph1 = load_map("test_load_map.txt")
# print(graph1)
# print(graph1.nodes)
# print(graph1.edges)
# graph2 = load_map("mit_map.txt")
# print(graph2)
# # print(graph2.nodes)
# # print(graph2.edges)
# print(directed_dfs(graph2, '1', '37', 9999, 999))