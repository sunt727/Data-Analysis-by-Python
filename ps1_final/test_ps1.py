from ps1_partition import get_partitions

import copy
import unittest
import ps1


def plan_generator(cows, limit, max_trips):
    """
    Finds all allocations of cows that result in the number of trips
    made being less than or equal to max_trips.

    Parameters:
    cows - a dictionary of name (string), weight (float) pairs
    limit - weight limit of the spaceship
    max_trips - maximum number of trips

    yields: set of frozensets where each frozenset of cow names
    represents a trip.
    """
    for plan in get_partitions(cows.keys()):
        # If all the trips in the plan are valid, and the plan has
        # fewer trips than max_trips, yield it.
        if all(sum(cows[cow] for cow in trip) <= limit for trip in plan):
            if len(plan) <= max_trips:
                yield set(frozenset(trip) for trip in plan)


class TestPS1(unittest.TestCase):

    def test_1_load_cows(self):

        cows = ps1.load_cows('ps1_cow_data.txt')
        real_cows = {'Maggie': 3, 'Moo Moo': 3, 'Herman': 7, 'Betsy': 9, 'Henrietta': 9,
                    'Oreo': 6, 'Milkshake': 2, 'Lola': 2, 'Florence': 2, 'Millie': 5}

        self.assertIsInstance(cows, dict, 'load_cows did not return a dictionary, but instead returned an instance of %s.' % type(cows))
        self.assertEqual(len(cows), 10, 'The dictionary returned by load_cows does not have the correct number of keys. Expected %s, got %s.' % (6, len(cows)))
        self.assertTrue(all(isinstance(w, str) for w in cows), 'A key in the dictionary returned by load_cows is not an integer. The dictionary you returned is: %s' % cows)
        self.assertTrue(all(isinstance(cs, int) for cs in cows.values()),'A value in the dictionary returned by load_cows is not a list. The dictionary you returned is: %s' % cows)
        self.assertDictEqual(cows, real_cows, 'The dictionary returned by load_cows does not match the expected dictionary. \nExpected: %s \nGot: %s ' % (real_cows, cows))

    def test_2_greedy_cow_transport(self):

        cows = {
            'John' : 85,
            'Ana' : 75,
            'Carlos' : 10,
            'Katy' : 15,
            'Aasavari' : 50,
            'Matt' : 65,
            'Bethany' : 45,
            'Laura' : 5,
            'Orhan' : 60,
            'Kaitlin' : 20
        }

        limit = 100

        # Check that greedy_cow_transport does not mutate the cows dictionary.
        cows_copy = copy.deepcopy(cows)
        greedy_plan = ps1.greedy_cow_transport(cows, limit)
        self.assertEqual(cows, cows_copy, 'greedy_cow_transport mutated the cows dictionary. Hint: the standard copying methods may fail, try googling copy.deepcopy')

        # The greedy process searches for the heaviest cow that fits in the
        # current trip.
        greedy_sol = [['John', 'Katy'],
                      ['Ana', 'Kaitlin', 'Laura'],
                      ['Matt', 'Carlos'],
                      ['Orhan'],
                      ['Aasavari', 'Bethany']]

        # Check that greedy_cow_transport returns a list of trips where each
        # trip is a list of cow names.
        self.assertEqual(type(greedy_plan), list, 'greedy_cow_transport did not return a list, and instead returned a %s.' % type(greedy_plan))
        self.assertTrue(all(type(trip) == list for trip in greedy_plan),
                        'greedy_cow_transport did not return a list of lists. Your code returned %s' % greedy_plan)
        self.assertTrue(all(all(type(cow) == str for cow in trip) for trip in greedy_plan),
                        'greedy_cow_transport did not return a list of lists of strings. Your code returned %s' % greedy_plan)

        # Check that all the trips in the plan that greedy_cow_transport returns
        # do not exceed the weight limit.
        self.assertTrue(all((sum(cows[cow] for cow in trip) <= limit) for trip in greedy_plan),
                        'greedy_cow_transport returned a trip that exceeds the weight limit %s. The plan you returned is: %s' % (limit, greedy_plan))

        # Check that the number of trips made is correct.
        actual_length = len(greedy_plan)
        exp_length = len(greedy_sol)
        self.assertEqual(actual_length, exp_length, 'greedy_cow_transport returned a plan that does have the correct number of trips. Expected %s, got %s' % (exp_length, actual_length))

        # Check that the plan returned by greedy_cow_transport matches one of
        # the correct plans.
        # Note: the problem set states that the order of the trips and the
        # order of cow names in the trips does not matter.
        greedy_plan_set = set(frozenset(trip) for trip in greedy_plan)
        sol_plan_set = set(frozenset(trip) for trip in greedy_sol)

        plan_matches_sol = greedy_plan_set == sol_plan_set
        self.assertTrue(plan_matches_sol, 'greedy_cow_transport returned a plan that does not match any of the expected plans.')

    def test_3_brute_force_cow_transport(self):
        cows = {
            'John' : 85,
            'Ana' : 75,
            'Carlos' : 10,
            'Katy' : 15,
            'Aasavari' : 50,
            'Matt' : 65,
            'Bethany' : 45,
            'Laura' : 5,
            'Orhan' : 60,
            'Kaitlin' : 20
        }

        limit = 100

        # Check that brute_force_cow_transport does not mutate the cows dictionary.
        cows_copy = copy.deepcopy(cows)
        brute_force_plan = ps1.brute_force_cow_transport(cows, limit)
        self.assertEqual(cows, cows_copy, 'brute_force_cow_transport mutated the cows dictionary. Hint: the standard copying methods may fail, try googling copy.deepcopy')

        real_plan = [['Carlos', 'John', 'Laura'],
                     ['Katy', 'Orhan', 'Kaitlin'],
                     ['Ana'],
                     ['Bethany', 'Aasavari'],
                     ['Matt']]

        # Check that brute_force_cow_transport returns a list of trips where
        # each trip is a list of cow names.
        self.assertEqual(type(brute_force_plan), list, 'brute_force_cow_transport did not return a list. Instead, it returned a %s' % type(brute_force_plan))
        self.assertTrue(all(type(trip) == list for trip in brute_force_plan),
                        'brute_force_cow_transport did not return a list of lists.')

        self.assertTrue(all(all(type(cow) == str for cow in trip) for trip in brute_force_plan),
                        'brute_force_cow_transport did not return a list of lists of strings. Your code returned: %s' % brute_force_plan)

        # Check that all the trips in the plan that bruteForceTransport
        # returns do not exceed the weight limit.
        self.assertTrue(all((sum(cows[cow] for cow in trip) <= limit) for trip in brute_force_plan),
                        'brute_force_cow_transport returned a trip that exceeds the weight limit %s. Your code returned: %s' % (limit, brute_force_plan))

        # Check that the number of trips made is correct.
        exp_length = len(real_plan)
        actual_length = len(brute_force_plan)
        self.assertEqual(actual_length, exp_length, 'brute_force_cow_transport returned a plan that does not match the expected plan in number of trips. Expected length %s, got %s' % (exp_length, actual_length))

        # Check that the plan returned by bruteForceTransport is a correct plan.
        # Note: the problem set states that the order of the trips and the
        # order of cow names in the trips does not matter.
        brute_force_plan_set = set(frozenset(trip) for trip in brute_force_plan)
        self.assertTrue(any(brute_force_plan_set == real_plan_set for real_plan_set in plan_generator(cows, limit, len(real_plan))),
                        'brute_force_cow_transport returned a plan that does not match any expected correct plan. Your code returned: %s' % brute_force_plan)


    def test_4_make_weight_sample(self):
        weights = (3, 5, 8, 9)
        n = 64
        answer = ps1.dp_make_weight(weights, n)
        self.assertIsInstance(answer, int, "dp_make_weight should return an integer, but instead returned a %s" % type(answer))
        self.assertEqual(answer, 20, 'Expected dp_make_make_weight to return %s with target weight %s and cow weights %s, but got %s' % (20, n, weights, answer))

    def test_5_make_weight_not_possible(self):
        weights = (2, 4, 8, 12)
        n = 63
        answer = ps1.dp_make_weight(weights, n)
        self.assertEqual(answer, None, 'Expected dp_make_make_weight to return %s with target weight %s and cow weights %s, but got %s' % (None, n, weights, answer))

    def test_6_very_large_input(self):
        weights = (3, 5, 8, 9, 15, 19, 22, 27, 28, 32, 36, 40, 51, 52, 53, 54, 60, 69, 73, 88, 91, 93, 102, 105)
        n = 1000
        answer = ps1.dp_make_weight(weights, n)
        self.assertEqual(answer, 332, 'Expected dp_make_make_weight to return %s with target weight %s and cow weights %s, but got %s' % (332, n, weights, answer))


if __name__ == '__main__':

    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestPS1))
    result = unittest.TextTestRunner(verbosity=2).run(suite)
