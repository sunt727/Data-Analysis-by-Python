#!/usr/bin/env python

from ps2 import *


class InternalPs2Test(unittest.TestCase):
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

    # ------------------------------------------------ holdout tests

    def test_start_end_same(self):
        self._test_path(expectedPath=['5'])

    def test_impossible_because_nonpositive_max_dist(self):
        self._test_impossible_path('32', '56', total_dist=0)
        self._test_impossible_path('32', '56', total_dist=-1)


if __name__ == "__main__":
    unittest.main()
