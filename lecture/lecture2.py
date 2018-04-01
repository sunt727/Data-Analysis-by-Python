# class Food(object):
#     def __init__(self, n, v, w):
#         self.name = n
#         self.value = v
#         self.calories = w
#     def getValue(self):
#         return self.value
#     def getCost(self):
#         return self.calories
#     def density(self):
#         return self.getValue()/self.getCost()
#     def __str__(self):
#         return self.name + ': <' + str(self.value)\
#                  + ', ' + str(self.calories) + '>'
#
# def buildMenu(names, values, calories):
#     menu = []
#     for i in range(len(values)):
#         menu.append(Food(names[i], values[i],
#                           calories[i]))
#     return menu
#
# def greedy(items, maxCost, keyFunction):
#     """Assumes items a list, maxCost >= 0,
#          keyFunction maps elements of Items to numbers"""
#     itemsCopy = sorted(items, key = keyFunction,
#                        reverse = True)
#     result = []
#     totalValue, totalCost = 0.0, 0.0
#     for i in range(len(itemsCopy)):
#         if (totalCost+itemsCopy[i].getCost()) <= maxCost:
#             result.append(itemsCopy[i])
#             totalCost += itemsCopy[i].getCost()
#             totalValue += itemsCopy[i].getValue()
#     return (result, totalValue)
#
# def testGreedy(items, constraint, keyFunction):
#     taken, val = greedy(items, constraint, keyFunction)
#     print('Total value of items taken =', val)
#     for item in taken:
#         print('   ', item)
#
# def testGreedys(foods, maxUnits):
#     print('Use greedy by value to allocate', maxUnits,
#           'calories')
#     testGreedy(foods, maxUnits, Food.getValue)
#     print('\nUse greedy by cost to allocate', maxUnits,
#           'calories')
#     testGreedy(foods, maxUnits,
#                lambda x: 1/Food.getCost(x))
#     print('\nUse greedy by density to allocate', maxUnits,
#           'calories')
#     testGreedy(foods, maxUnits, Food.density)
#
# def maxVal(toConsider, avail):
#     """Assumes toConsider a list of items,
#           avail a weight
#        Returns a tuple of the total value of a solution
#           to the 0/1 knapsack problem and the items of
#           that solution"""
#     if toConsider == [] or avail == 0:
#         result = (0, ())
#     elif toConsider[0].getCost() > avail:
#         #Explore right branch only
#         result = maxVal(toConsider[1:], avail)
#     else:
#         nextItem = toConsider[0]
#         #Explore left branch
#         withVal, withToTake = maxVal(toConsider[1:],
#                                      avail - nextItem.getCost())
#         withVal += nextItem.getValue()
#         #Explore right branch
#         withoutVal, withoutToTake = maxVal(toConsider[1:], avail)
#         #Choose better branch
#         if withVal > withoutVal:
#             result = (withVal, withToTake + (nextItem,))
#         else:
#             result = (withoutVal, withoutToTake)
#     return result
#
# def testMaxVal(foods, maxUnits, printItems = True):
#     print('Use search tree to allocate', maxUnits,
#           'calories')
#     val, taken = maxVal(foods, maxUnits)
#     print('Total value of items taken =', val)
#     if printItems:
#         for item in taken:
#             print('   ', item)
#
# # names = ['wine', 'beer', 'pizza', 'burger', 'fries',
# #         'cola', 'apple', 'donut', 'cake']
# # values = [89,90,95,100,90,79,50,10]
# # calories = [123,154,258,354,365,150,95,195]
# # foods = buildMenu(names, values, calories)
# #
# # testGreedys(foods, 1000)
# # print('')
# # # testMaxVal(foods, 1000)
# # #
# import random
#
# def buildLargeMenu(numItems, maxVal, maxCost):
#     items = []
#     for i in range(numItems):
#         items.append(Food(str(i),
#                           random.randint(1, maxVal),
#                           random.randint(1, maxCost)))
#     return items
#
# # for numItems in (5, 10, 15, 20, 25, 30, 35, 40, 45):
# #     print('Try a menu with', numItems, 'items')
# #     items = buildLargeMenu(numItems, 90, 250)
# #     testMaxVal(items, 750, False)
#
# def fib(n):
#     if n == 0 or n == 1:
#         return 1
#     else:
#         return fib(n - 1) + fib(n - 2)
#
# print(fib(30))
#
# # print(fib(120))
#
# def fastFib(n, memo):
#     """Assumes n is an int >= 0, memo used only by
#          recursive calls
#        Returns Fibonacci of n"""
#     if n == 0 or n == 1:
#         return 1
#     try:
#         return memo[n]
#     except KeyError:
#         result = fastFib(n-1, memo) + fastFib(n-2, memo)
#         memo[n] = result
#         return result
#
# for i in range(121):
#     print('fib(' + str(i) + ') =', fastFib(i, {}))
#
# def fastMaxVal(toConsider, avail, memo):
#     """Assumes toConsider a list of subjects, avail a weight
#          memo supplied by recursive calls
#        Returns a tuple of the total value of a solution to the
#          0/1 knapsack problem and the subjects of that solution"""
#     if (len(toConsider), avail) in memo:
#         result = memo[(len(toConsider), avail)]
#     elif toConsider == [] or avail == 0:
#         result = (0, ())
#     elif toConsider[0].getCost() > avail:
#         #Explore right branch only
#         result = fastMaxVal(toConsider[1:], avail, memo)
#     else:
#         nextItem = toConsider[0]
#         #Explore left branch
#         withVal, withToTake =\
#                  fastMaxVal(toConsider[1:],
#                             avail - nextItem.getCost(), memo)
#         withVal += nextItem.getValue()
#         #Explore right branch
#         withoutVal, withoutToTake = fastMaxVal(toConsider[1:],
#                                                 avail, memo)
#         #Choose better branch
#         if withVal > withoutVal:
#             result = (withVal, withToTake + (nextItem,))
#         else:
#             result = (withoutVal, withoutToTake)
#     memo[(len(toConsider), avail)] = result
#     return result
#
# def testMaxVal1(foods, maxUnits, printItems = True):
#     print('Menu contains', len(foods), 'items')
#     print('Use search tree to allocate', maxUnits,
#           'calories')
#     val, taken = fastMaxVal(foods, maxUnits, {})
#     if printItems:
#         print('Total value of items taken =', val)
#         for item in taken:
#             print('   ', item)
#
# #for numItems in (5, 10, 15, 20, 25, 30, 35, 40, 45, 50):
# #    items = buildLargeMenu(numItems, 90, 250)
# #    testMaxVal1(items, 750, True)
# testMaxVal1([3, 5, 8, 9], 64, True)
#
# def isPrime(x):
#     """Assumes x is an int > 2
#        Returns True if i is prime and false otherwise"""
#     for i in range(2, x):
#         if x%i == 0:
#             return False
#     return True
#
# def buildLargeMenu1(numItems, maxVal, maxCost):
#     items = []
#     for i in range(numItems):
#         items.append(Food(str(i),
#                           random.randint(1, maxVal),
#                           random.random()*maxCost))
#     return items
#
# #for numItems in (5, 10, 15, 20, 25, 30, 35, 40, 45, 50):
# #   items = buildLargeMenu1(numItems, 90, 250)
# #   testMaxVal1(items, 750, fastMaxVal, True)
# #
# ## e1 if c else e2
# ##
# ## x/y if y !=0 else None
# #
# #oldList = range(10)
# #test = lambda x: x%2 != 0
# #f = lambda x: x**2
# #
# #newList = []
# #for i in oldList:
# #   if test(i):
# #       newList.append(f(i))
# #
# #print(newList)
# #
# #new_List = [f(i) for i in oldList if test(i)]
# #print(newList)
#
# # L = [expression for item in L if conditional]
# #
# # L = []
# # for item in list:
# #    if conditional:
# #        L.append(expression)#L = [x*x for x in range(10)]
# # print(L)
#
# L = [2**i for i in range(21)]
# print(L)
#
# sentence = 'This is a sentence'.split(' ')
# L = [word[0] for word in sentence]
# print(L)
#
# noprimes = [j for i in range(2, 8) for j in range(i*2, 50, i)]
# primes = [x for x in range(2, 50) if x not in noprimes]
# print(noprimes)
# print(primes)
#
# noprimes = []
# for i in range(2,8):
#   for j in range(i*2, 50, i):
#     noprimes.append(j)
#
# primes=[]
# for x in range(2,50):
#  if x not in noprimes:
#    primes.append(x)
#
#
#
def findLengthOfLCIS(nums):
	maxlen = i = 0
	while i < len(nums):
		result = 1
		while i < len(nums)-1 and nums[i] < nums[i+1]:
			result += 1
			i += 1
		maxlen = max(maxlen, result)
		i += 1
	return maxlen

print(findLengthOfLCIS([1,3,5,4,7]))
print(findLengthOfLCIS([2,2,2,2,2]))
print(findLengthOfLCIS([1]))
print(findLengthOfLCIS([1,3,5,4,2,3,4,5]))
print(findLengthOfLCIS([2,1]))
print(findLengthOfLCIS([1,3,5,7]))

def twoSum(nums, target):
	"""
	:type nums: List[int]
	:type target: int
	:rtype: List[int]
	"""
	map = {}
	for i in range(len(nums)):
		if nums[i] not in map.keys():
			map[target - nums[i]] = i
		else:
			return [map[nums[i]], i]

print(twoSum([2, 7, 11, 15], 9))


