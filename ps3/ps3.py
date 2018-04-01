# -*- coding: utf-8 -*-
# Problem Set 3: Simulating robots
# Name: Tuo Sun
# Collaborators (discussion): None
# Time: 4:30

import math
import random
import matplotlib
matplotlib.use("TkAgg")

import ps3_visualize
import pylab

from ps3_verify_movement3 import test_robot_movement


# === Provided class Position
class Position(object):
    """
    A Position represents a location in a two-dimensional room, where
    coordinates are given by floats (x, y).
    """
    def __init__(self, x, y):
        """
        Initializes a position with coordinates (x, y).
        """
        self.x = x
        self.y = y
        
    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y
    
    def get_new_position(self, angle, speed):
        """
        Computes and returns the new Position after a single clock-tick has
        passed, with this object as the current position, and with the
        specified angle and speed.

        Does NOT test whether the returned position fits inside the room.

        angle: float representing angle in degrees, 0 <= angle < 360
        speed: positive float representing speed

        Returns: a Position object representing the new position.
        """
        old_x, old_y = self.get_x(), self.get_y()
        
        # Compute the change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))
        
        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y
        
        return Position(new_x, new_y)

    def __str__(self):  
        return "Position: " + str(math.floor(self.x)) + ", " + str(math.floor(self.y))


# === Problem 1
class RectangularRoom(object):
    """
    A RectangularRoom represents a rectangular region containing clean or dirty
    tiles.

    A room has a width and a height and contains (width * height) tiles. Each tile
    has some fixed amount of dirt. The tile is considered clean only when the amount
    of dirt on this tile is 0.
    """
    def __init__(self, width, height, dirt_amount):
        """
        Initializes a rectangular room with the specified width, height, and 
        dirt_amount on each tile.

        width: an integer > 0
        height: an integer > 0
        dirt_amount: an integer >= 0
        """
        self.width = width
        self.height = height
        #  create a list of tiles
        self.tiles = [(x, y) for x in range(self.width) for y in range(self.height)]
        #  use the list to create a dictionary {tile: assigned dirt ammounts}
        self.tiles_dirt = {tile: dirt_amount for tile in self.tiles}
    
    def clean_tile_at_position(self, pos, capacity):
        """
        Mark the tile under the position pos as cleaned by capacity amount of dirt.

        Assumes that pos represents a valid position inside this room.

        pos: a Position object
        capacity: the amount of dirt to be cleaned in a single time-step
                  can be negative which would mean adding dirt to the tile

        Note: The amount of dirt on each tile should be NON-NEGATIVE.
              If the capacity exceeds the amount of dirt on the tile, mark it as 0.
        """
        # regularize the position into the tile and set a non-negative number to the dictionary
        tile_pos = (math.floor(pos.get_x()), math.floor(pos.get_y()))
        self.tiles_dirt[tile_pos] = max(self.tiles_dirt[tile_pos] - capacity,0)

    def is_tile_cleaned(self, m, n):
        """
        Return True if the tile (m, n) has been cleaned.

        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer
        
        Returns: True if the tile (m, n) is cleaned, False otherwise

        Note: The tile is considered clean only when the amount of dirt on this
              tile is 0.
        """
        return self.tiles_dirt[(m, n)] == 0

    def get_num_cleaned_tiles(self):
        """
        Returns: an integer; the total number of clean tiles in the room
        """
        #  return a length of list of cleaned tiles
        return len([x for x in list(self.tiles_dirt.keys()) if self.is_tile_cleaned(x[0], x[1])])
        
    def is_position_in_room(self, pos):
        """
        Determines if pos is inside the room.

        pos: a Position object.
        Returns: True if pos is in the room, False otherwise.
        """
        #  make sure the position is greater than 0 and less than the dimension of room
        return 0 <= pos.get_x() < self.width and 0 <= pos.get_y() < self.height
        
    def get_dirt_amount(self, m, n):
        """
        Return the amount of dirt on the tile (m, n)
        
        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer

        Returns: an integer
        """
        #  get the dirt of the tile, not need to use 'get' since we create them at first
        return int(self.tiles_dirt[(m, n)])
        
    def get_num_tiles(self):
        """
        Returns: an integer; the total number of tiles in the room
        """
        #  length of tiles is the total number of tiles
        return len(self.tiles) 

    def get_random_position(self):
        """
        Returns: a Position object; a random position inside the room
        """
        #  return a position object with 1 precision degree coordinate
        return Position(round(random.randrange(self.width),1), 
                        round(random.randrange(self.height),1)) 

class Robot(object):
    """
    Represents a robot cleaning a particular room.

    At all times, the robot has a particular position and direction in the room.
    The robot also has a fixed speed and a fixed cleaning capacity.

    Subclasses of Robot should provide movement strategies by implementing
    update_position_and_clean, which simulates a single time-step.
    """
    def __init__(self, room, speed, capacity):
        """
        Initializes a Robot with the given speed and given cleaning capacity in the 
        specified room. The robot initially has a random direction and a random 
        position in the room.

        room:  a RectangularRoom object.
        speed: a float (speed > 0)
        capacity: a positive interger; the amount of dirt cleaned by the robot 
                  in a single time-step
        """
        self.room = room
        self.speed = speed
        self.capacity = capacity
        self.pos = self.room.get_random_position()  # get a random position in the room
        self.direction = round(random.randrange(360),1)  # get d for 0.0 <= d < 360.0

    def get_robot_position(self):
        """
        Returns: a Position object giving the robot's position in the room.
        """
        return self.pos

    def get_robot_direction(self):
        """
        Returns: a float d giving the direction of the robot as an angle in
        degrees, 0.0 <= d < 360.0.
        """
        return self.direction

    def set_robot_position(self, position):
        """
        Set the position of the robot to position.

        position: a Position object.
        """
        self.pos = position

    def set_robot_direction(self, direction):
        """
        Set the direction of the robot to direction.

        direction: float representing an angle in degrees
        """
        self.direction = direction

    def update_position_and_clean(self):
        """
        Simulate the raise passage of a single time-step.

        Move the robot to a new position (if the new position is invalid, 
        rotate once to a random new direction, and stay stationary) and mark the tile it is on as having
        been cleaned by capacity amount. 
        """
        # do not change -- implement in subclasses
        raise NotImplementedError

# === Problem 2
class StandardRobot(Robot):
    """
    A StandardRobot is a Robot with the standard movement strategy.

    At each time-step, a StandardRobot attempts to move in its current
    direction; when it would hit a wall, it *instead*
    chooses a new direction randomly.
    """

    def update_position_and_clean(self):
        """
        Simulate the raise passage of a single time-step.

        Move the robot to a new position (if the new position is invalid, 
        rotate once to a random new direction, and stay stationary) and clean the dirt on the tile
        by its given capacity. 
        """
        # pre-caculate the next position
        new_pos = self.get_robot_position().get_new_position(self.direction, self.speed)
        # only execute cleaning without out of boundary violation
        if self.room.is_position_in_room(new_pos):
            self.room.clean_tile_at_position(new_pos, self.capacity)
            self.set_robot_position(new_pos)  # update the position for the next time-step
        else:  # otherwise, change the direction randomly
            self.set_robot_direction(round(random.randrange(360),1))
            

# Uncomment this line to see your implementation of StandardRobot in action!
# test_robot_movement(StandardRobot, RectangularRoom)

# === Problem 3
class RobotWithACat(Robot):
    """
    A RobotWithACat is a robot with a cat mounted on it. A RobotWithACat will 
    not clean the tile it moves to and pick a new, random direction for itself 
    with probability p rather than simply cleaning the tile it moves to.
    """
    p = 0.1337
    
    @staticmethod
    def set_cat_probability(prob):
        """
        Sets the probability of the cat messing with the controls equal to PROB.

        prob: a float (0 <= prob <= 1)
        """
        RobotWithACat.p = prob
    
    def gets_cat_interference(self):
        """
        Answers the question: Does the cat mess with this RobotWithACat's controls
        at this timestep?
        The cat messes with the RobotWithACat's controls with probability p.

        returns: True if the cat messes with RobotWithACat's controls, False otherwise.
        """
        return random.random() < RobotWithACat.p
    
    def update_position_and_clean(self):
        """
        Simulate the passage of a single time-step.
        
        Check if the cat messes with the controls. If the robot does get cat
        interference, do not clean the current tile and change its direction randomly.

        If the cat does not mess with the controls, the robot should behave like
        StandardRobot at this time-step (checking if it can move to a new position,
        move there if it can, pick a new direction and stay stationary if it can't)
        """
        # pre-caculate the next position
        new_pos = self.get_robot_position().get_new_position(self.direction, self.speed)
        # only execute cleaning without out of boundary violation or cat interference 
        if (not self.gets_cat_interference()) and self.room.is_position_in_room(new_pos):
                self.room.clean_tile_at_position(new_pos, self.capacity)
                self.set_robot_position(new_pos)  # update the position for the next time-step
        else:  # otherwise, change the direction randomly
            self.set_robot_direction(round(random.randrange(360),1))
    
# test_robot_movement(RobotWithACat, RectangularRoom)

# === Problem 4
class SuperRobot(Robot):
    """
    A SuperRobot is a robot that moves extra fast and cleans two tiles in one timestep.

    It moves in its current direction, cleans the tile it lands on, and continues 
    moving in that direction and cleans the second tile it lands on, all in one unit of time. 

    If the SuperRobot hits a wall when it attempts to move in its current direction,
    it may dirty the current tile by one unit because it moves very fast and can knock dust off of the wall.
    
    There are three possible cases:

    1. The robot tries to move. If it would hit the wall on the first move, it 
    does not move. Instead, it turns to face a random direction and stops for this timestep. 
    
    2. If it can move, it moves and cleans the tile it moves to. Then, it tries to move a second time. 
        

        b. If it does not hit the wall, it moves and cleans the tile it moves to. 

    """
    p = 0.15

    @staticmethod
    def set_dirty_probability(prob):
        """
        Sets the probability of getting the tile dirty equal to PROB.

        prob: a float (0 <= prob <= 1)
        """
        SuperRobot.p = prob
    
    def dirties_tile(self):
        """
        Answers the question: Does this SuperRobot dirty the tile if it hits the wall at full speed?
        A SuperRobot dirties a tile with probability p.

        returns: True if the SuperRobot dirties the tile, False otherwise.
        """
        return random.random() < SuperRobot.p
    
    def update_position_and_clean(self):
        """
        Simulate the passage of a single time-step.

        Check if the robot is going to hit a wall when it tries moving to the second tile. 
        If it is, clean the tile adjacent to the wall and then dirty it by 1 unit with probability p, 
        and rotate to a random direction.

        If the robot is not going to run into a wall when going to the second tile, the robot should 
        behave like StandardRobot, but move two tiles at a time (checking if it can move to both new 
        positions and move there if it can, or pick a new direction and stay stationary if it is adjacent 
        to a wall)
        """
        # pre-caculate the next 1st position
        new_pos = self.get_robot_position()  # get a original position
        i = 0
        while i < 2:  # create i represent (i+1)th move
            ori_pos = new_pos  # save the original position
            new_pos = new_pos.get_new_position(self.direction, self.speed)
            # only execute cleaning without out of boundary violation 
            if self.room.is_position_in_room(new_pos):
                self.room.clean_tile_at_position(new_pos, self.capacity)
                self.set_robot_position(new_pos)  # update the position for the next/second half of time-step
            else:  # if it hits the wall
                if i == 1 and self.dirties_tile():  # dirty the tile when it is the second time and with probability p
                    self.room.clean_tile_at_position(ori_pos, self.capacity-1)  # clean but dirty the tile by unit 1
                self.set_robot_direction(round(random.randrange(360),1))  # set a random direction and stop
                i = 2
                pass
            i += 1


# test_robot_movement(SuperRobot, RectangularRoom)
        
# === Problem 5
def run_simulation(num_robots, speed, capacity, width, height, dirt_amount, min_coverage, num_trials,
                  robot_type):
    """
    Runs num_trials trials of the simulation and returns the mean number of
    time-steps needed to clean the fraction min_coverage of the room. For example,
    if we want to test the amount of time it takes to clean 75% of the room, min_coverage
    would be 0.75.

    The simulation is run with num_robots robots of type robot_type, each       
    with the input speed and capacity in a room of dimensions width x height
    with the dirt dirt_amount on each tile.
    
    num_robots: an int (num_robots > 0)
    speed: a float (speed > 0)
    capacity: an int (capacity >0)
    width: an int (width > 0)
    height: an int (height > 0)
    dirt_amount: an int
    min_coverage: a float (0 <= min_coverage <= 1.0)
    num_trials: an int (num_trials > 0)
    robot_type: class of robot to be instantiated (e.g. StandardRobot or
                RobotWithACat)
    """
    record = []  #create a record list to store the time steps of each trial
    for x in range(num_trials):
        step = 0  # initialize time step, room and robots
        room = RectangularRoom(width, height, dirt_amount)
        robots = [robot_type(room, speed, capacity)]*num_robots
        #  keep running the updates until the safisfication of the coverage
        while room.get_num_cleaned_tiles()/room.get_num_tiles() < min_coverage:
            step += 1
            for robot in robots:
                robot.update_position_and_clean()
        record.append(step)  # add the result into record list
    return sum(record)/len(record)  # return the mean value of the record list


#print ('avg time steps: ' + str(run_simulation(1, 1.0, 1, 5, 5, 3, 1.0, 50, StandardRobot)))
#print ('avg time steps: ' + str(run_simulation(1, 1.0, 1, 10, 10, 3, 0.8, 50, StandardRobot)))
#print ('avg time steps: ' + str(run_simulation(1, 1.0, 1, 10, 10, 3, 0.9, 50, StandardRobot)))
#print ('avg time steps: ' + str(run_simulation(1, 1.0, 1, 20, 20, 3, 0.5, 50, StandardRobot)))
#print ('avg time steps: ' + str(run_simulation(3, 1.0, 1, 20, 20, 3, 0.5, 50, StandardRobot)))

# === Problem 6
#
# ANSWER THE FOLLOWING QUESTIONS:
#
# 1)How does the performance of the three robot types compare when cleaning 80%
#       of a 20x20 room?
#       RobotWithACat takes always longer than StandardRobot, 
#       but SuperRobot always performs much better
#
# 2) How does the performance of the three robot types compare when two of each
#       robot cleans 80% of rooms with dimensions 
#       10x30, 20x15, 25x12, and 50x6?
#       time_steps: RobotWithACat > StandardRobot > SuperRobot
#       a room with w-h ratio closed to 1:1 takes shorter time

def show_plot_compare_strategies(title, x_label, y_label):
    """
    Produces a plot comparing the three robot strategies in a 20x20 room with 80%
    minimum coverage.
    """
    num_robot_range = range(1, 11)
    times1 = []
    times2 = []
    times3 = []
    for num_robots in num_robot_range:
        print ("Plotting", num_robots, "robots...")
        times1.append(run_simulation(num_robots, 1.0, 1, 20, 20, 3, 0.8, 20, StandardRobot))
        times2.append(run_simulation(num_robots, 1.0, 1, 20, 20, 3, 0.8, 20, RobotWithACat))
        times3.append(run_simulation(num_robots, 1.0, 1, 20, 20, 3, 0.8, 20, SuperRobot))
    pylab.plot(num_robot_range, times1)
    pylab.plot(num_robot_range, times2)
    pylab.plot(num_robot_range, times3)
    pylab.title(title)
    pylab.legend(('StandardRobot', 'RobotWithACat', 'SuperRobot'))
    pylab.xlabel(x_label)
    pylab.ylabel(y_label)
    pylab.show()
    
def show_plot_room_shape(title, x_label, y_label):
    """
    Produces a plot showing dependence of cleaning time on room shape.
    """
    aspect_ratios = []
    times1 = []
    times2 = []
    times3 = []
    for width in [10, 20, 25, 50]:
        height = int(300/width)
        print ("Plotting cleaning time for a room of width:", width, "by height:", height)
        aspect_ratios.append(float(width) / height)
        times1.append(run_simulation(2, 1.0, 1, width, height, 3, 0.8, 200, StandardRobot))
        times2.append(run_simulation(2, 1.0, 1, width, height, 3, 0.8, 200, RobotWithACat))
        times3.append(run_simulation(2, 1.0, 1, width, height, 3, 0.8, 200, SuperRobot))
    pylab.plot(aspect_ratios, times1, 'o-')
    pylab.plot(aspect_ratios, times2, 'o-')
    pylab.plot(aspect_ratios, times3, 'o-')
    pylab.title(title)
    pylab.legend(('StandardRobot', 'RobotWithACat', 'SuperRobot'), fancybox=True, framealpha=0.5)
    pylab.xlabel(x_label)
    pylab.ylabel(y_label)
    pylab.show()


show_plot_compare_strategies('Time to clean 80% of a 20x20 room, for various numbers of robots','Number of robots','Time / steps')
show_plot_room_shape('Time to clean 80% of a 300-tile room for various room shapes','Aspect Ratio', 'Time / steps')
