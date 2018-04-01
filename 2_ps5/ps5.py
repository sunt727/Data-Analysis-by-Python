# -*- coding: utf-8 -*-
# Problem Set 5: Experimental Analysis
# Name: Tuo Sun
# Collaborators (discussion): Sen Dai
# Time: 7:00

import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score
import re

# cities in our weather data
CITIES = [
	'BOSTON',
	'SEATTLE',
	'SAN DIEGO',
	'PHOENIX',
	'LAS VEGAS',
	'CHARLOTTE',
	'DALLAS',
	'BALTIMORE',
	'LOS ANGELES',
	'MIAMI',
	'NEW ORLEANS',
	'ALBUQUERQUE',
	'PORTLAND',
	'SAN FRANCISCO',
	'TAMPA',
	'NEW YORK',
	'DETROIT',
	'ST LOUIS',
	'CHICAGO'
]

TRAINING_INTERVAL = range(1961, 2011)
TESTING_INTERVAL = range(2011, 2017)

"""
Begin helper code
"""
class Temperature(object):
	"""
	The collection of temperature records loaded from given csv file
	"""
	def __init__(self, filename):
		"""
		Initialize a Temperature instance, which stores the temperature records
		loaded from a given csv file specified by filename.

		Args:
			filename: name of the csv file (str)
		"""
		self.rawdata = {}

		f = open(filename, 'r')
		header = f.readline().strip().split(',')
		for line in f:
			items = line.strip().split(',')

			date = re.match('(\d\d\d\d)(\d\d)(\d\d)', items[header.index('DATE')])
			year = int(date.group(1))
			month = int(date.group(2))
			day = int(date.group(3))

			city = items[header.index('CITY')]
			temperature = float(items[header.index('TEMP')])
			if city not in self.rawdata:
				self.rawdata[city] = {}
			if year not in self.rawdata[city]:
				self.rawdata[city][year] = {}
			if month not in self.rawdata[city][year]:
				self.rawdata[city][year][month] = {}
			self.rawdata[city][year][month][day] = temperature

		f.close()

	def get_yearly_temp(self, city, year):
		"""
		Get the daily temperatures for the given year and city.

		Args:
			city: city name (str)
			year: the year to get the data for (int)

		Returns:
			a 1-d numpy array of daily temperatures for the specified year and
			city
		"""
		temperatures = []
		assert city in self.rawdata, "provided city is not available"
		assert year in self.rawdata[city], "provided year is not available"
		for month in range(1, 13):
			for day in range(1, 32):
				if day in self.rawdata[city][year][month]:
					temperatures.append(self.rawdata[city][year][month][day])
		return np.array(temperatures)

	def get_daily_temp(self, city, month, day, year):
		"""
		Get the daily temperature for the given city and time (year + date).

		Args:
			city: city name (str)
			month: the month to get the data for (int, where January = 1,
				December = 12)
			day: the day to get the data for (int, where 1st day of month = 1)
			year: the year to get the data for (int)

		Returns:
			a float of the daily temperature for the specified time (year +
			date) and city
		"""
		assert city in self.rawdata, "provided city is not available"
		assert year in self.rawdata[city], "provided year {} is not available".format(year)
		assert month in self.rawdata[city][year], "provided month is not available"
		assert day in self.rawdata[city][year][month], "provided day is not available"
		return self.rawdata[city][year][month][day]

def se_over_slope(x, y, estimated, model):
	"""
	For a linear regression model, calculate the ratio of the standard error of
	this fitted curve's slope to the slope. The larger the absolute value of
	this ratio is, the more likely we have the upward/downward trend in this
	fitted curve by chance.

	Args:
		x: a 1-d numpy array with length N, representing the x-coordinates of
			the N sample points
		y: a 1-d numpy array with length N, representing the y-coordinates of
			the N sample points
		estimated: an 1-d numpy array of values estimated by a linear
			regression model
		model: a numpy array storing the coefficients of a linear regression
			model

	Returns:
		a float for the ratio of standard error of slope to slope
	"""
	assert len(y) == len(estimated)
	assert len(x) == len(estimated)
	EE = ((estimated - y)**2).sum()
	var_x = ((x - x.mean())**2).sum()
	SE = np.sqrt(EE/(len(x)-2)/var_x)
	return SE/model[0]

"""
End helper code
"""

def generate_models(x, y, degs):
	"""
	Generate regression models by fitting a polynomial for each degree in degs
	to points (x, y).

	Args:
		x: a 1-d numpy array of length N, representing the x-coordinates of
			the N sample points
		y: a 1-d numpy array of length N, representing the y-coordinates of
			the N sample points
		degs: a list of integers that correspond to the degree of each polynomial
			model that will be fit to the data

	Returns:
		a list of numpy arrays, where each array is a 1-d array of coefficients
		that minimizes the squared error of the fitting polynomial
	"""
	models = []  # create an empty model list
	for deg in degs:
		model = np.polyfit(x, y, deg)  # get the array of coefficients that best fits
		models.append(model)
	return models

def evaluate_models_on_training(x, y, models):
	"""
	For each regression model, compute the R-squared value for this model with the
	standard error over slope of a linear regression line (only if the model is
	linear), and plot the data along with the best fit curve.

	For the plots, you should plot data points (x,y) as blue dots and your best
	fit curve (aka model) as a red solid line. You should also label the axes
	of this figure appropriately and have a title reporting the following
	information:
		degree of your regression model,
		R-square of your model evaluated on the given data points,
		and SE/slope (if degree of this model is 1 -- see se_over_slope).

	Args:
		x: a 1-d numpy array with length N, representing the x-coordinates of
			the N sample points
		y: a 1-d numpy array with length N, representing the y-coordinates of
			the N sample points
		models: a list containing the regression models you want to apply to
			your data. Each model is a numpy array storing the coefficients of
			a polynomial.

	Returns:
		None
	"""
	for i in range(len(models)):  # iterate each model
		plt.figure()  # create a new plot
		estyvals = np.polyval(models[i], x)  # get the array of estimated y values
		plt.plot(x, y, 'bo', label='Data Points')  # plot points that show original points
		plt.plot(x, estyvals, 'r-', label='Regression Curve')  # plot the regression curve
		plt.xlabel('Years')
		plt.ylabel('Temperature (degrees Celsius)')
		deg = len(models[i]) - 1  # get the degree by the number of coefficients in a model
		r2 = r2_score(y, estyvals)  # get R2 value
		if deg > 1:
			plt.title('#{0} Model \nwhen R2 value is {1:.6f} and degree is {2}'.format(i+1, r2, deg))
		else:  # se_over_slope(x, y, estimated, model)
			plt.title('#{0} Model \nwhen R2 value is {1:.6f} and degree is {2} \nand the ratio of the standard error is {3:.6f}'.format(
				i+1, r2, deg, se_over_slope(x, y, estyvals, models[i])))
		plt.legend()
		plt.show()


def gen_cities_avg(temp, multi_cities, years):
	"""
	Compute the average annual temperature over multiple cities.

	Args:
		temp: instance of Temperature
		multi_cities: the names of cities we want to average over (list of str)
		years: the range of years of the yearly averaged temperature (list of
			int)

	Returns:
		a numpy 1-d array of floats with length = len(years). Each element in
		this array corresponds to the average annual temperature over the given
		cities for a given year.
	"""
	temps = []
	for year in years:
		# get the average annual temperature of all cities in this year
		temp_thisyr = sum(temp.get_yearly_temp(city, year).mean() for city in multi_cities)/len(multi_cities)
		temps.append(temp_thisyr)
	return np.array(temps, np.float64)  # convert the list to an array

def find_interval(x, y, length, has_positive_slope):
	"""
	Args:
		x: a 1-d numpy array with length N, representing the x-coordinates of
			the N sample points
		y: a 1-d numpy array with length N, representing the y-coordinates of
			the N sample points
		length: the length of the interval
		has_positive_slope: a boolean whose value specifies whether to look for
			an interval with the most extreme positive slope (True) or the most
			extreme negative slope (False)

	Returns:
		a tuple of the form (i, j) such that the application of linear (deg=1)
		regression to the data in x[i:j], y[i:j] produces the most extreme
		slope and j-i = length.

		In the case of a tie, it returns the most recent interval. For example,
		if the intervals (2,5) and (8,11) both have the same slope, (8,11) should
		be returned.

		If such an interval does not exist, returns None
	"""
	k_max, k_min = float('-inf'), float('inf')  # make INF and -INF for the for loop
	for i in range(len(x)-length+1):
		j = i + length
		model = np.polyfit(x[i:j], y[i:j], 1)[0]  # get the slope of the regression

		if has_positive_slope:
			if abs(model - k_max) <= 1e-8 or model > k_max:  # if tie or greater than the k_max, update i
				k_max = model
				best_i = i
		else:
			if abs(model - k_min) <= 1e-8 or model < k_min:  # if tie or less than the k_min, update i
				k_min = model
				best_i = i

	if has_positive_slope:  # if want positive, return if k_max is positive
		if k_max > 0:
			return best_i, best_i + length
	else:
		if k_min < 0:  # if want negative, return if k_min is negative
			return best_i, best_i + length


def rmse(y, estimated):
	"""
	Calculate the root mean square error term.

	Args:
		y: a 1-d numpy array with length N, representing the y-coordinates of
			the N sample points
		estimated: an 1-d numpy array of values estimated by the regression
			model

	Returns:
		a float for the root mean square error term
	"""
	return pow(((y-estimated)**2).sum()/len(y), 0.5)


def evaluate_models_on_testing(x, y, models):
	"""
	For each regression model, compute the RMSE for this model and plot the
	test data along with the models estimation.

	For the plots, you should plot data points (x,y) as blue dots and your best
	fit curve (aka model) as a red solid line. You should also label the axes
	of this figure appropriately and have a title reporting the following
	information:
		degree of your regression model,
		RMSE of your model evaluated on the given data points.

	Args:
		x: a 1-d numpy array with length N, representing the x-coordinates of
			the N sample points
		y: a 1-d numpy array with length N, representing the y-coordinates of
			the N sample points
		models: a list containing the regression models you want to apply to
			your data. Each model is a numpy array storing the coefficients of
			a polynomial.

	Returns:
		None
	"""
	for i in range(len(models)):  # iterate each model
		plt.figure()  # create a new plot
		estyvals = np.polyval(models[i], x)  # get the array of estimated y values
		plt.plot(x, y, 'bo', label='Data Points')  # plot points that show original points
		plt.plot(x, estyvals, 'r-', label='Regression Curve')  # plot the regression curve
		plt.xlabel('Years')
		plt.ylabel('Temperature (degrees Celsius)')
		deg = len(models[i]) - 1  # get the degree by the number of coefficients in a model
		r = rmse(y, estyvals)  # get the RSME
		plt.title('#{0} Model \nwhen RMSE is {1:.6f} and degree is {2}'.format(i+1, r, deg))
		plt.legend()
		plt.show()

if __name__ == '__main__':

	pass

	# Problem 3A
	# temp = Temperature('data.csv')  # import the temperature
	# x = np.array([x for x in range(1961, 2015)], np.int32)  # get the array of years from 1961 to 2016
	# y = np.array([temp.get_daily_temp('BOSTON', 2, 14, year) for year in x], np.float64)  # the 2/14 temp of Boston
	# models = generate_models(x, y, [1])
	# evaluate_models_on_training(x, y, models)
	# Problem 3B
	# temp = Temperature('data.csv')  # import the temperature
	# x = np.array([x for x in range(1961, 2017)], np.int32)  # get the array of years from 1961 to 2016
	# y = gen_cities_avg(temp, ['BOSTON'], x)  # the annual temperature of Boston
	# models = generate_models(x, y, [1])
	# evaluate_modelFs_on_training(x, y, models)
	# Problem 4B
	## SAN DIEGO
	# temp = Temperature('data.csv')  # import the temperature
	# x = np.array([x for x in range(1961, 2017)], np.int32)  # get the array of years from 1961 to 2016
	# y = gen_cities_avg(temp, ['SAN DIEGO'], x)
	# # i, j = find_interval(x, y, 30, True)  # increasing
	# i, j = find_interval(x, y, 30, False)  # decreasing
	# models = generate_models(x[i:j], y[i:j], [1])
	# print(models[0][0])
	# evaluate_models_on_training(x[i:j], y[i:j], models)
	## CITIES
	# temp = Temperature('data.csv')  # import the temperature
	# x = np.array([x for x in range(1961, 2017)], np.int32)  # get the array of years from 1961 to 2016
	# y = gen_cities_avg(temp, CITIES, x)
	# ijs = [find_interval(x, y, length, False) for length in range(1, 2017-1961)]  # decreasing
	# ijs = [ij for ij in ijs if ij is not None]  # delete Nonetype results from the list
	# i, j = max(ijs, key=lambda yr: yr[1] - yr[0])  # get the longest interval by comparing the difference
	# models = generate_models(x, y, [1])
	#models = generate_models(x[i:j], y[i:j], [1])
	# print(models[0][0])
	# evaluate_models_on_training(x, y, models)

	# Problem 5B
	# temp = Temperature('data.csv')  # import the temperature
	# x = np.array([x for x in TRAINING_INTERVAL], np.int32)  # get the array of years of TRAINING_INTERVAL
	# y = gen_cities_avg(temp, CITIES, x)
	# models = generate_models(x, y, [1, 2, 20])
	# # evaluate_models_on_training(x, y, models)
	#
	# x_test = np.array([x for x in TESTING_INTERVAL], np.int32)  # get the array of years of TRAINING_INTERVAL
	# y_test = gen_cities_avg(temp, CITIES, x_test)
	# evaluate_models_on_testing(x_test, y_test, models)