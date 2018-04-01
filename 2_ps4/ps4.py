# Problem Set 4: Simulating the Spread of Disease and Bacteria Population Dynamics
# Name: Tuo Sun
# Collaborators (Discussion): None
# Time: 4:30
# Difficult Sections:

import math
import numpy as np
import pylab as pl
import random


##########################
# End helper code
##########################

class NoChildException(Exception):
	"""
	NoChildException is raised by the reproduce() method in the SimpleBacteria
	and ResistantBacteria classes to indicate that a bacteria cell does not
	reproduce. You should use NoChildException as is; you do not need to
	modify it or add any code.
	"""

##########################
# PROBLEM 1
##########################

class SimpleBacteria(object):
	"""A simple bacteria cell with no antibiotic resistance"""

	def __init__(self, birth_prob, death_prob):
		"""
		Args:
			birth_prob (float in [0, 1]): Maximum possible reproduction
				probability
			death_prob (float in [0, 1]): Maximum death probability
		"""
		self.birth_prob = birth_prob
		self.death_prob = death_prob

	def is_killed(self):
		"""
		Stochastically determines whether this bacteria cell is killed in
		the patient's body at a time step, i.e. the bacteria cell dies with
		some probability equal to the death probability each time step.

		Returns:
			bool: True with probability self.death_prob, False otherwise.
		"""
		return random.random() < self.death_prob  # make a random number from 0 to 1 to see whether it should be killed

	def reproduce(self, pop_density):
		"""
		Stochastically determines whether this bacteria cell reproduces at a
		time step. Called by the update() method in the Patient and
		TreatedPatient classes.

		The bacteria cell reproduces with probability
		birth_prob * (1 - population density).

		If this bacteria cell reproduces, then reproduce() creates and returns
		the instance of the offspring SimpleBacteria (which has the same
		birth_prob and death_prob values as its parent).

		Args:
			pop_density (float): The population density, defined as the
				current bacteria population divided by the maximum population

		Returns:
			SimpleBacteria: A new instance representing the offspring of
				this bacteria cell (if the bacteria reproduces). The child
				should have the same birth_prob and death_prob values as
				this bacteria.

		Raises:
			NoChildException if this bacteria cell does not reproduce.
		"""
		if random.random() < self.birth_prob * (1 - pop_density):  # judge whether this bacteria cell reproduces
			return SimpleBacteria(self.birth_prob, self.death_prob)  # generate a new bacteria object
		else:
			raise NoChildException


class Patient(object):
	"""
	Representation of a simplified patient. The patient does not take any
	antibiotics and his/her bacteria populations have no antibiotic resistance.
	"""
	def __init__(self, bacteria, max_pop):
		"""
		Args:
			bacteria (list of SimpleBacteria): The bacteria in the population
			max_pop (int): Maximum possible bacteria population size for
				this patient
		"""
		self.bacteria = bacteria
		self.max_pop = max_pop
		# default population density by dividing the surviving bacteria population by the maximum population
		self.pop_density = len(self.bacteria) / self.max_pop

	def get_total_pop(self):
		"""
		Gets the size of the current total bacteria population.

		Returns:
			int: The total bacteria population
		"""
		return len(self.bacteria)  # return the length of the bacteria list as the population

	def update(self):
		"""
		Update the state of the bacteria population in this patient for a
		single time step. update() should execute the following steps in
		this order:

		1. Determine whether each bacteria cell dies (according to the
		   is_killed method) and create a new list of surviving bacteria cells.

		2. Calculate the current population density by dividing the surviving
		   bacteria population by the maximum population. This population
		   density value is used for the following steps until the next call
		   to update()

		3. Based on the population density, determine whether each surviving
		   bacteria cell should reproduce and add offspring bacteria cells to
		   a list of bacteria in this patient. New offspring do not reproduce.

		4. Reassign the patient's bacteria list to be the list of surviving
		   bacteria and new offspring bacteria

		Returns:
			int: The total bacteria population at the end of the update
		"""
		survivings = [b for b in self.bacteria if not b.is_killed()]  # create a surviving list
		self.pop_density = len(survivings) / self.max_pop  # update the current population density
		offsprings = []
		for b in survivings:
			try:
				offsprings.append(b.reproduce(self.pop_density))  # add offsprings into a new list
			except NoChildException:  # pass when no bacteria reproduces
				pass
		self.bacteria = survivings + offsprings  # add offsprings list into a original list
		return self.get_total_pop()  # return the total bacteria population

##########################
# PROBLEM 2
##########################

def calc_pop_avg(populations, n):
	"""
	Finds the average bacteria population size across trials at time step n

	Args:
		populations (list of lists or 2D array): populations[i][j] is the
			number of bacteria in trial i at time step j
		n (int): time step
	Returns:
		float: The average bacteria population size at time step n
	"""
	ns = [trial[n] for trial in populations]  # list of nth time step in each trial
	return sum(ns)/len(ns)  # return the average value of the list


def simulation_without_antibiotic(num_bacteria,
								  max_pop,
								  birth_prob,
								  death_prob,
								  num_trials):
	"""
	Run the simulation. No antibiotics
	are used, and bacteria do not have any antibiotic resistance.

	For each of num_trials trials:
		* instantiate a list of SimpleBacteria
		* instantiate a Patient using the list of SimpleBacteria
		* simulate changes to the bacteria population for 300 timesteps,
		  recording the bacteria population after each time step. Note
		  that the first time step should contain the starting number of
		  bacteria in the patient

	Args:
		num_bacteria (int): number of SimpleBacteria to create for patient
		max_pop (int): maximum bacteria population for patient
		birth_prob (float in [0, 1]): maximum reproduction
			probability
		death_prob (float in [0, 1]): maximum death probability
		num_trials (int): number of simulation runs to execute

	Returns:
		populations (list of lists or 2D array): populations[i][j] is the
			number of bacteria in trial i at time step j
	"""
	pops = []  # create a populations list
	for trial in range(num_trials):  # for each trial
		bacterias = [SimpleBacteria(birth_prob, death_prob)] * num_bacteria  # instantiate a list of SimpleBacteria
		patient = Patient(bacterias, max_pop)  # instantiate a Patient using the list of SimpleBacteria
		record = [num_bacteria]  # the first time step should contain the starting number of bacteria in the patient
		for timestep in range(300):  # run 300 time steps
			patient.update()
			record.append(patient.get_total_pop())  # get the population of bacterias
		pops.append(record)
	return pops




# When you are ready to run the simulation, uncomment the next line
# populations = simulation_without_antibiotic(100, 1000, 0.1, 0.025, 50)
# print(populations)

##########################
# PROBLEM 3
##########################

def calc_pop_std(populations, t):
	"""
	Finds the standard deviation of populations across different trials
	at time step t by:
		* calculating the average population at time step t
		* compute average squared distance of the data points from the average
		  and take its square root

	You may not use third-party functions that calculate standard deviation,
	such as numpy.std. Other built-in or third-party functions that do not
	calculate standard deviation may be used.

	Args:
		populations (list of lists or 2D array): populations[i][j] is the
			number of bacteria present in trial i at time step j
		t (int): time step

	Returns:
		float: the standard deviation of populations across different trials at
			 a specific time step
	"""
	avg = calc_pop_avg(populations, t)  # get the average population at time step t
	# compute average squared distance of the data points from the average and take its square root
	return pow(sum([pow(timesteps[t] - avg, 2) for timesteps in populations])/len(populations), 0.5)

# print(calc_pop_std(populations, 3))

def calc_95_ci(populations, t):
	"""
	Finds a 95% confidence interval around the average bacteria population
	at time t by:
		* computing the mean and standard deviation of the sample
		* using the standard deviation of the sample to estimate the
		  standard error of the mean (SEM)
		* using the SEM to construct confidence intervals around the
		  sample mean

	Args:
		populations (list of lists or 2D array): populations[i][j] is the
			number of bacteria present in trial i at time step j
		t (int): time step

	Returns:
		mean (float): the sample mean
		width (float): 1.96 * SEM

		I.e., you should return a tuple containing (mean, width)
	"""
	#  mean is the average number; SEM is equal to standard deviation divided by numbers of sample
	return calc_pop_avg(populations, t), 1.96 * calc_pop_std(populations, t) / pow(len(populations), 0.5)

def plot_simulation_without_antibiotic(populations):
	"""
	Makes a plot of the bacteria population with error bars representing the
	95% confidence interval around the average bacteria population.
	Axis and plot title should be present. Use the code at the bottom of this
	document to test your implementation.

	Args:
		populations (list of lists or 2D array): populations[i][j] is the
			number of bacteria in trial i at time step j
	"""

	x = [x for x in range(len(populations[0]))]
	y = [calc_95_ci(populations, t)[0] for t in x]  # get the average resistant populations
	err = [calc_95_ci(populations, t)[1] for t in x]  # get the interval
	pl.errorbar(x, y, yerr=err)
	pl.title('Simulation Without Antibiotic')
	pl.xlabel('Time Step')
	pl.ylabel('Number of Bacteria')
	pl.show()

##########################
# PROBLEM 4
##########################

class ResistantBacteria(SimpleBacteria):
	"""A bacteria cell that can have antibiotic resistance."""

	def __init__(self, birth_prob, death_prob, resistant, mut_prob):
		"""
		Args:
			birth_prob (float in [0, 1]): reproduction probability
			death_prob (float in [0, 1]): death probability
			resistant (bool): whether this bacteria has antibiotic resistance
			mut_prob (float): mutation probability for this
				bacteria cell. This is the maximum probability of the
				offspring acquiring antibiotic resistance
		"""
		self.birth_prob = birth_prob
		self.death_prob = death_prob
		self.resistant = resistant
		self.mut_prob = mut_prob

	def get_resistant(self):
		"""Returns whether the bacteria has antibiotic resistance"""
		return self.resistant

	def is_killed(self):
		"""Stochastically determines whether this bacteria cell is killed in
		the patient's body at a given time step.

		Checks whether the bacteria has antibiotic resistance. If resistant,
		the bacteria dies with the regular death probability / 4. If not resistant,
		the bacteria dies with the regular death probability, making the
		probability of death higher.

		Returns:
			bool: True if the bacteria dies with the appropriate probability
				and False otherwise.
		"""

		if self.get_resistant():
			return random.random() < self.death_prob / 4
		else:
			return random.random() < self.death_prob

	def reproduce(self, pop_density):
		"""
		Stochastically determines whether this bacteria cell reproduces at a
		time step. Called by the update() method in the TreatedPatient class.

		A surviving bacteria cell will reproduce with probability:
		self.birth_prob * (1 - pop_density).

		If the bacteria cell reproduces, then reproduce() creates and returns
		an instance of the offspring ResistantBacteria, which will have the
		same birth_prob, death_prob, and mut_prob values as its parent.

		If the bacteria has antibiotic resistance, the offspring will also be
		resistant. If the bacteria does not have antibiotic resistance, its
		offspring have a probability of self.mut_prob * (1-pop_density) of
		developing that resistance trait. That is, bacteria in less densely
		populated environments have a greater chance of mutating to have
		antibiotic resistance.

		Args:
			pop_density (float): the population density

		Returns:
			ResistantBacteria: an instance representing the offspring of
			this bacteria cell (if the bacteria reproduces). The child should
			have the same birth_prob, death_prob values and mut_prob
			as this bacteria. Otherwise, raises a NoChildException if this
			bacteria cell does not reproduce.
		"""
		if random.random() < self.birth_prob * (1 - pop_density):  # judge whether this bacteria cell reproduces
			# if the bacteria has resistance, the offspring will be resistant; else check the probability
			oresisitant = True if self.get_resistant() else (random.random() < self.mut_prob * (1-pop_density))
			# generate a new bacteria object
			return ResistantBacteria(self.birth_prob, self.death_prob, oresisitant, self.mut_prob)
		else:
			raise NoChildException


class TreatedPatient(Patient):
	"""
	Representation of a treated patient. The patient is able to take an
	antibiotic and his/her bacteria population can acquire antibiotic
	resistance. The patient cannot go off an antibiotic once on it.
	"""
	def __init__(self, bacteria, max_pop):
		"""
		Args:
			bacteria: The list representing the bacteria population (a list of
					  bacteria instances)
			max_pop: The maximum bacteria population for this patient (int)

		This function should initialize self.on_antibiotic, which represents
		whether a patient has been given an antibiotic. Initially, the
		patient has not been given an antibiotic.

		Don't forget to call Patient's __init__ method at the start of this
		method.
		"""
		self.bacteria = bacteria
		self.max_pop = max_pop
		# default population density by dividing the surviving bacteria population by the maximum population
		self.pop_density = len(self.bacteria) / self.max_pop
		self.on_antibiotic = False  # Initially, the patient has not been given an antibiotic

	def set_on_antibiotic(self):
		"""
		Administer an antibiotic to this patient. The antibiotic acts on the
		bacteria population for all subsequent time steps.
		"""
		self.on_antibiotic = True

	def get_resistant_pop(self):
		"""
		Get the population size of bacteria cells with antibiotic resistance

		Returns:
			int: the number of bacteria with antibiotic resistance
		"""
		return len([b for b in self.bacteria if b.get_resistant()])  # return length of the resistant list

	def update(self):
		"""
		Update the state of the bacteria population in this patient for a
		single time step. update() should execute these actions in order:

		1. Determine whether each bacteria cell dies (according to the
		   is_killed method) and create a new list of surviving bacteria cells.

		2. If the patient is on antibiotics, the surviving bacteria cells from
		   (1) only survive further if they are resistant. If the patient is
		   not on the antibiotic, keep all surviving bacteria cells from (1)

		3. Calculate the current population density. This value is used until
		   the next call to update(). Use the same calculation as in Patient

		4. Based on this value of population density, determine whether each
		   surviving bacteria cell should reproduce and add offspring bacteria
		   cells to the list of bacteria in this patient.

		5. Reassign the patient's bacteria list to be the list of survived
		   bacteria and new offspring bacteria

		Returns:
			int: The total bacteria population at the end of the update
		"""
		survivings = [b for b in self.bacteria if not b.is_killed()]  # create a surviving list
		if self.on_antibiotic:
			survivings = [b for b in survivings if b.get_resistant()]  # only survive further if they are resistant
		self.pop_density = len(survivings) / self.max_pop  # update the current population density
		offsprings = []
		for b in self.bacteria:
			try:
				offsprings.append(b.reproduce(self.pop_density))  # add offsprings into a new list
			except NoChildException:  # pass when no bacteria reproduces
				pass
		self.bacteria = survivings + offsprings  # add offsprings list into a original list
		return len(self.bacteria)  # return the total bacteria population


##########################
# PROBLEM 5
##########################

def simulation_with_antibiotic(num_bacteria,
							   max_pop,
							   birth_prob,
							   death_prob,
							   resistant,
							   mut_prob,
							   num_trials):
	"""
	Runs simulations and plots graphs for problem 4.

	For each of num_trials trials:
		* instantiate a list of ResistantBacteria
		* instantiate a patient
		* run a simulation for 150 timesteps, add the antibiotic, and run the
		  simulation for an additional 250 timesteps, recording the total
		  bacteria population and the resistance bacteria population after
		  each time step

	Plot the average bacteria population size for both the total bacteria
	population and the antibiotic-resistant bacteria population (y-axis) as a
	function of elapsed time steps (x-axis) on the same plot. You might find
	the helper function make_two_curve_plot helpful

	Args:
		num_bacteria (int): number of ResistantBacteria to create for
			the patient
		max_pop (int): maximum bacteria population for patient
		birth_prob (float int [0-1]): reproduction probability
		death_prob (float in [0, 1]): probability of a bacteria cell dying
		resistant (bool): whether the bacteria initially have
			antibiotic resistance
		mut_prob (float in [0, 1]): mutation probability for the
			ResistantBacteria cells
		num_trials (int): number of simulation runs to execute

	Returns: a tuple of two lists of lists, or two 2D arrays
		populations (list of lists or 2D array): the total number of bacteria
			at each time step for each trial; total_population[i][j] is the
			total population for trial i at time step j
		resistant_pop (list of lists or 2D array): the total number of
			resistant bacteria at each time step for each trial;
			resistant_pop[i][j] is the number of resistant bacteria for
			trial i at time step j
	"""
	pops = []  # create a populations list
	repops = []  # create a resistant populations list
	for trial in range(num_trials):  # for each trial
		# instantiate a list of ResistantBacteria with initializing without resistant
		bacterias = [ResistantBacteria(birth_prob, death_prob, resistant, mut_prob)] * num_bacteria
		patient = TreatedPatient(bacterias, max_pop)  # instantiate a Patient using the list of SimpleBacteria
		record = [num_bacteria]  # the first time step should contain the starting number of bacteria in the patient
		rrecord = [0]
		for timestep in range(150):  # run 150 time steps without antibiotic
			patient.update()
			record.append(patient.get_total_pop())  # get the population of bacterias
			rrecord.append(patient.get_resistant_pop())  # get the resistant population of bacterias
		patient.set_on_antibiotic()
		for timestep in range(250):  # run 250 time steps with antibiotic
			patient.update()
			record.append(patient.get_total_pop())  # get the population of bacterias
			rrecord.append(patient.get_resistant_pop())  # get the resistant population of bacterias
		pops.append(record)
		repops.append(rrecord)
	return pops, repops

def plot_simulation_with_antibiotic(populations, resistant_pop):
	"""
	Makes a plot with two curves on it. One curve depicts the bacteria
	population and the second curve depicts the resistant population.
	Both curves should include error bars representing the 95% confidence
	interval around the average populations. Include a title, labels, and
	a legend.

	Args:
		populations (list of lists or 2D array): the total number of bacteria
			at each time step for each trial; total_population[i][j] is the
			total population for trial i at time step j
		resistant_pop (list of lists or 2D array): the total number of
			resistant bacteria at each time step for each trial;
			resistant_pop[i][j] is the number of resistant bacteria for
			trial i at time step j
	"""
	x = [x for x in range(len(populations[0]))]
	y1 = [calc_95_ci(populations, t)[0] for t in x]  # get the average populations
	y2 = [calc_95_ci(resistant_pop, t)[0] for t in x]  # get the interval
	err1 = [calc_95_ci(populations, t)[1] for t in x]  # get the average resistant populations
	err2 = [calc_95_ci(resistant_pop, t)[1] for t in x]  # get the interval
	pl.errorbar(x, y1, yerr=err1, label='Total bacteria')
	pl.errorbar(x, y2, yerr=err2, label='Resistant bacteria')
	pl.legend(loc='lower right')
	pl.title('Simulation With Antibiotic')
	pl.xlabel('Time Step')
	pl.ylabel('Bacteria Population')
	pl.show()

if __name__ == '__main__':
	pass
	# When you are ready to run the simulations, uncomment the next lines one
	# at a time

	############################
	# Problem 3
	############################

	# populations = simulation_without_antibiotic(num_bacteria=100,
	#                                             max_pop=1000,
	#                                             birth_prob=0.5,
	#                                             death_prob=0.3,
	#                                             num_trials=50)
	# plot_simulation_without_antibiotic(populations)
	############################
	# Problem 5
	############################
	## EX1
	# total_pop, resistant_pop = simulation_with_antibiotic(num_bacteria=100,
	#                                                       max_pop=800,
	#                                                       birth_prob=0.25,
	#                                                       death_prob=0.15,
	#                                                       resistant=False,
	#                                                       mut_prob=0.1,
	#                                                       num_trials=50)
	# plot_simulation_with_antibiotic(total_pop, resistant_pop)

	## EX2
	# total_pop, resistant_pop = simulation_with_antibiotic(num_bacteria=100,
	#                                                       max_pop=800,
	#                                                       birth_prob=0.08,
	#                                                       death_prob=0.2,
	#                                                       resistant=False,
	#                                                       mut_prob=0.8,
	#                                                       num_trials=50)
	# plot_simulation_with_antibiotic(total_pop, resistant_pop)
