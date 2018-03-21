"""
Wumpsim.py a Python implementation of pywumpsim

Created by Erik Phillips - ephill07@calpoly.edu
Date: November 6th, 2017
Version 2: February 15th, 2018

CSC 480 - Artificial Intelligence
Professor Daniel Kauffman
Cal Poly, San Luis Obispo

https://github.com/erikphillips/wumpus_world
https://github.com/erikphillips/CPE480TA-wumpus-project

This version of the wumpus simulator can be currently found here:
https://github.com/erikphillips/CPE480TA-wumpus-project
"""


import PyAgent
import ManualPyAgent
import random
import queue
import sys


# The version of the wumpus simulator
WUMPSIM_VERSION = "v2.1"

# The size of the world, which will be a square
WORLD_SIZE = 4

# The probability that a pit will be at any given location
PIT_PROBABILITY = 0.2

# The probability that the wumpus will scream and reverse direction
SCREAM_PROBABILITY = 0.05

# Orientations: Defines orientations within the world """
RIGHT = 0
UP = 1
LEFT = 2
DOWN = 3

# Actions: Defines allowed actions within the world
GOFORWARD = 0
TURNLEFT = 1
TURNRIGHT = 2
GRAB = 3
CLIMB = 5
WAIT = 6
COMPASS = 7


class Percept(object):
    def __init__(self):
        """ __init__: create a new percept"""
        self.stench = False
        self.breeze = False
        self.glitter = False
        self.bump = False
        self.scream = False
        self.compass = None

    def initialize(self):
        """ initialize: reset the percepts to their default value at the start of a try """
        self.stench = False
        self.breeze = False
        self.glitter = False
        self.bump = False
        self.scream = False
        self.compass = None


class State(object):
    """ State: holds the information on the current state of the game """

    def __init__(self, file_information, static_wumpus):
        """ __init__: create a new state for the wumpus world, setting locations for wumpus, pits, and gold """

        # If there is file information, then use that, otherwise setup randomly
        if file_information is None:
            self.wumpus_count = random.randint(1, round((WORLD_SIZE + 1) / 2))
            self.gold_locations = self._get_gold_locations()

            if static_wumpus:
                self.wumpus_rotations = [0] * self.wumpus_count
                self.wumpus_locations = self._get_wumpus_locations()
            else:
                self.wumpus_rotations = self._get_wumpus_rotations()
                self.wumpus_locations = self._get_wumpus_locations()

            self.pit_locations = self._get_pit_locations()
            self.walls = self._get_walls()
            self.wumpus_movement_queues = self._get_wumpus_moves()
        else:
            self.wumpus_count = file_information.wumpus_count
            self.gold_locations = file_information.gold_locations
            self.wumpus_rotations = file_information.wumpus_rotations
            self.wumpus_locations = file_information.wumpus_locations
            self.pit_locations = file_information.pit_locations
            self.walls = file_information.walls
            self.wumpus_movement_queues = self._get_wumpus_moves()

        self.agent_location = Location(1, 1)
        self.agent_orientation = RIGHT
        self.agent_alive = True
        self.agent_in_cave = True

        self.wumpus_alive = []
        self.agent_has_gold = []
        for i in range(self.wumpus_count):
            self.wumpus_alive.append(True)
            self.agent_has_gold.append(False)

    def initialize(self):
        """ initialize: called at the start of a new try, to reset game aspects back to default """
        self.agent_location = Location(1, 1)
        self.agent_orientation = RIGHT
        self.agent_alive = True
        self.agent_has_gold = 0
        self.agent_in_cave = True

        self.wumpus_alive = []
        self.agent_has_gold = []
        for i in range(self.wumpus_count):
            self.wumpus_alive.append(True)
            self.agent_has_gold.append(False)

    def _get_gold_locations(self):
        """ _get_gold_location: return a random location not (1,1) for the gold's location """
        locations = []
        for i in range(self.wumpus_count):
            x, y = self._get_random_location(obj_type="GOLD")
            locations.append(Location(x, y))
        return locations

    def _get_wumpus_rotations(self):
        rotations = []
        for i in range(self.wumpus_count):
            rotations.append(random.choice([1, 2]))
        return rotations

    def _get_wumpus_locations(self):
        """
        _get_wumpus_location: return a random location, not (1,1) for the wumpus's location
        Note: the gold's location must be set for this function to complete.
        """

        locations = []
        for i in range(self.wumpus_count):
            if self.wumpus_rotations[i] == 0 or self.wumpus_rotations[i] == 3:  # if the rotation is static or path-follow
                x, y = self._get_random_location(obj_type="WUMPUS")
                locations.append(Location(x, y))
            else:  # otherwise, pick a random location based on the availability around the gold
                locations.append(random.choice(self._get_all_possible_wumpus_locations(index=i)))

        return locations

    def _get_random_location(self, obj_type=None):
        """ _get_random_location: return a random location that is not the (1,1) square """
        x = 1
        y = 1

        while self._location_rejected(x, y, obj_type):
            x = random.randint(1, WORLD_SIZE)
            y = random.randint(1, WORLD_SIZE)

        return x, y

    @staticmethod
    def _location_rejected(x, y, obj_type):
        if obj_type == "GOLD":
            return ((x == 2) and (y == 2)) or (x == 1) or (y == 1) or (x == WORLD_SIZE) or (y == WORLD_SIZE)
        elif obj_type == "PIT":
            return (x == 1) and (y == 1)
        elif obj_type == "WUMPUS":
            return ((x == 1) and (y == 1)) or ((x == 1) and (y == 2)) or ((x == 2) and (y == 1))
        else:
            return (x == 1) and (y == 1)

    def _get_pit_locations(self):
        """ _get_pit_locations: returns an array of pit locations, randomly selected based on a probability """
        locations = []
        for x in range(1, WORLD_SIZE + 1):
            for y in range(1, WORLD_SIZE + 1):
                location = Location(x, y)
                if (x != 1) or (y != 1):
                    # Using the PIT_PROBABILITY, randomly determine if a pit will be at this location
                    if (random.randint(0, 1000 - 1)) < (PIT_PROBABILITY * 1000):
                        add_pit = True
                        for i in range(self.wumpus_count):
                            if self.gold_locations[i] == location:
                                add_pit = False
                                break
                        if add_pit:
                            locations.append(location)
        return locations

    @staticmethod
    def _get_walls():
        walls = []
        for i in range(1, WORLD_SIZE + 1):
            idx = Wall.locate_wall(walls, i, 1)
            if idx >= 0:
                wall = walls[idx]
                wall.bottom = True
            else:
                wall = Wall(i, 1)
                wall.bottom = True
                walls.append(wall)

            idx = Wall.locate_wall(walls, i, WORLD_SIZE)
            if idx >= 0:
                wall = walls[idx]
                wall.top = True
            else:
                wall = Wall(i, WORLD_SIZE)
                wall.top = True
                walls.append(wall)

            idx = Wall.locate_wall(walls, 1, i)
            if idx >= 0:
                wall = walls[idx]
                wall.left = True
            else:
                wall = Wall(1, i)
                wall.left = True
                walls.append(wall)

            idx = Wall.locate_wall(walls, WORLD_SIZE, i)
            if idx >= 0:
                wall = walls[idx]
                wall.right = True
            else:
                wall = Wall(WORLD_SIZE, i)
                wall.right = True
                walls.append(wall)

        return walls

    def _get_all_possible_wumpus_locations(self, index):
        """
        _get_all_possible_wumpus_locations: return all possible wumpus locations
        Note: the gold's location must be set prior to execution of this function
        """

        locations = []
        for x in range(max(1, self.gold_locations[index].x - 1), min(WORLD_SIZE + 1, self.gold_locations[index].x + 1)):
            for y in range(max(1, self.gold_locations[index].y - 1), min(WORLD_SIZE + 1, self.gold_locations[index].y + 1)):
                if not (x == self.gold_locations[index].x and y == self.gold_locations[index].y):
                    locations.append(Location(x, y))
        return locations

    def _get_wumpus_moves(self):
        """
        _get_wumpus_moves: find the order to which the wumpus will move.
        :return Queue: returns a queue with the moves for the wumpus.
        """

        moves = []
        for i in range(self.wumpus_count):
            if self.wumpus_rotations[i] == 0 or self.wumpus_rotations[i] == 3:
                moves.append(queue.Queue())
                continue  # early return if the wumpus should not move in a pattern

            que = queue.Queue()

            x = self.gold_locations[i].x
            y = self.gold_locations[i].y

            # add the locations to the queue in clockwise order, repeating the corners (for direction changes)
            que.put(Location(x + 1, y + 1))  # upper right
            que.put(Location(x + 1, y + 1))  # upper right
            que.put(Location(x + 1, y))      # middle right
            que.put(Location(x + 1, y - 1))  # lower right
            que.put(Location(x + 1, y - 1))  # lower right
            que.put(Location(x, y - 1))      # lower middle
            que.put(Location(x - 1, y - 1))  # lower left
            que.put(Location(x - 1, y - 1))  # lower left
            que.put(Location(x - 1, y))      # middle left
            que.put(Location(x - 1, y + 1))  # upper left
            que.put(Location(x - 1, y + 1))  # upper left
            que.put(Location(x, y + 1))      # upper middle

            if self.wumpus_rotations[i] == 2:  # 2 == counter-clockwise, meaning the queue needs to be reversed
                aux_stack = []
                while not que.empty():
                    aux_stack.append(que.get())

                while len(aux_stack) > 0:
                    que.put(aux_stack.pop())

            while que.queue[0] != self.wumpus_locations[i]:
                que.put(que.get())  # cycle through the que until the first location is the wumpus location
            que.put(que.get())  # make the first move not the current location

            moves.append(que)

        return moves


class Wall(object):
    """ Wall: wall object that tracks a tile's wall attributes """
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.top = False
        self.right = False
        self.bottom = False
        self.left = False

    @staticmethod
    def locate_wall(walls, x, y):
        for idx in range(len(walls)):
            if walls[idx].x == x and walls[idx].y == y:
                return idx
        return -1


class Location(object):
    """ Location: location object that holds an x, y coordinate in the map """

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    @staticmethod
    def adjacent(location1, location2):
        """ adjacent: returns true if the two locations are next to each other """

        x1 = location1.x
        x2 = location2.x
        y1 = location1.y
        y2 = location2.y

        if (x1 == x2) and (y1 == (y2 - 1)) or \
           (x1 == x2) and (y1 == (y2 + 1)) or \
           (x1 == (x2 - 1)) and (y1 == y2) or \
           (x1 == (x2 + 1)) and (y1 == y2):
            return True

        return False


class WumpusWorld(object):
    def __init__(self, file_information=None, static_wumpus=False, disable_compass=False):
        """
        __init__: create a new wumpus world, randomly placing the wumpus and the gold, and multiple pits
        :param WumpusWorldFileInformation file_information: the file information for this world creation
        """

        self.num_actions = 0
        self.disable_compass = disable_compass

        # Update the current state
        self.current_state = State(file_information=file_information, static_wumpus=static_wumpus)

        # Update current percepts
        self.current_percept = Percept()

        for pit in self.current_state.pit_locations:
            if Location.adjacent(self.current_state.agent_location, pit):
                self.current_percept.breeze = True

        for i in range(self.current_state.wumpus_count):
            if self.current_state.gold_locations[i].x == 1 and self.current_state.gold_locations[i].y == 1:
                self.current_percept.glitter = True

            if Location.adjacent(self.current_state.agent_location, self.current_state.wumpus_locations[i]) or \
                    (self.current_state.agent_location == self.current_state.wumpus_locations[i]):
                self.current_percept.stench = True

    def initialize(self):
        """ initialize: called at the start of a new try, resets certain aspects to default """

        self.num_actions = 0
        self.current_state.initialize()
        self.current_percept.initialize()

        for pit in self.current_state.pit_locations:
            if Location.adjacent(self.current_state.agent_location, pit):
                self.current_percept.breeze = True

        for i in range(self.current_state.wumpus_count):
            if self.current_state.gold_locations[i].x == 1 and self.current_state.gold_locations[i].y == 1:
                self.current_percept.glitter = True

            if Location.adjacent(self.current_state.agent_location, self.current_state.wumpus_locations[i]) or \
                    (self.current_state.agent_location == self.current_state.wumpus_locations[i]):
                self.current_percept.stench = True

    def get_percept(self):
        """ get_percept: return the current percept for the agent's location """
        return self.current_percept

    def execute_action(self, action):
        """
        execute_action: execute the provided action, updating the agent's location and the percepts
        :param int action: the action that will be performed as defined in the actions
        """

        self.num_actions += 1
        self.current_percept.bump = False
        self.current_percept.scream = False
        self.current_percept.compass = None

        if action == GOFORWARD:
            idx = Wall.locate_wall(self.current_state.walls,
                                   self.current_state.agent_location.x,
                                   self.current_state.agent_location.y)
            wall = None  # if wall is none (ie idx = -1), then there is no obstructions at the current location
            if idx >= 0:
                wall = self.current_state.walls[idx]

            if self.current_state.agent_orientation == RIGHT:
                if self.current_state.agent_location.x < WORLD_SIZE:
                    if wall and wall.right:
                        self.current_percept.bump = True
                    else:
                        self.current_state.agent_location.x += 1
                else:
                    self.current_percept.bump = True
            elif self.current_state.agent_orientation == UP:
                if self.current_state.agent_location.y < WORLD_SIZE:
                    if wall and wall.top:
                        self.current_percept.bump = True
                    else:
                        self.current_state.agent_location.y += 1
                else:
                    self.current_percept.bump = True
            elif self.current_state.agent_orientation == LEFT:
                if self.current_state.agent_location.x > 1:
                    if wall and wall.left:
                        self.current_percept.bump = True
                    else:
                        self.current_state.agent_location.x -= 1
                else:
                    self.current_percept.bump = True
            elif self.current_state.agent_orientation == DOWN:
                if self.current_state.agent_location.y > 1:
                    if wall and wall.bottom:
                        self.current_percept.bump = True
                    else:
                        self.current_state.agent_location.y -= 1
                else:
                    self.current_percept.bump = True

            self.current_percept.glitter = False  # Update glitter percept
            self.current_percept.stench = False  # Update stench percept

            for i in range(self.current_state.wumpus_count):
                if (not self.current_state.agent_has_gold[i]) and \
                        (self.current_state.agent_location == self.current_state.gold_locations[i]):
                    self.current_percept.glitter = True

                if Location.adjacent(self.current_state.agent_location, self.current_state.wumpus_locations[i]) or \
                        (self.current_state.agent_location == self.current_state.wumpus_locations[i]):
                    self.current_percept.stench = True

                # check for death by wumpus
                if self.current_state.wumpus_alive[i] and \
                        (self.current_state.agent_location == self.current_state.wumpus_locations[i]):
                    self.current_state.agent_alive = False

            # Update breeze percept
            self.current_percept.breeze = False

            for pit in self.current_state.pit_locations:
                if Location.adjacent(self.current_state.agent_location, pit):
                    self.current_percept.breeze = True
                elif self.current_state.agent_location == pit:
                    self.current_state.agent_alive = False

        if action == TURNLEFT:
            if self.current_state.agent_orientation == RIGHT:
                self.current_state.agent_orientation = UP
            elif self.current_state.agent_orientation == UP:
                self.current_state.agent_orientation = LEFT
            elif self.current_state.agent_orientation == LEFT:
                self.current_state.agent_orientation = DOWN
            elif self.current_state.agent_orientation == DOWN:
                self.current_state.agent_orientation = RIGHT

        if action == TURNRIGHT:
            if self.current_state.agent_orientation == RIGHT:
                self.current_state.agent_orientation = DOWN
            elif self.current_state.agent_orientation == UP:
                self.current_state.agent_orientation = RIGHT
            elif self.current_state.agent_orientation == LEFT:
                self.current_state.agent_orientation = UP
            elif self.current_state.agent_orientation == DOWN:
                self.current_state.agent_orientation = LEFT

        if action == GRAB:
            self.current_percept.glitter = False
            for i in range(self.current_state.wumpus_count):
                if not self.current_state.agent_has_gold[i] and \
                        (self.current_state.agent_location == self.current_state.gold_locations[i]):
                    self.current_state.agent_has_gold[i] = True

                if not self.current_state.agent_has_gold[i] and \
                        self.current_state.agent_location == self.current_state.gold_locations[i]:
                    self.current_percept.glitter = True

        if action == CLIMB:
            if self.current_state.agent_location.x == 1 and self.current_state.agent_location.y == 1:
                self.current_state.agent_in_cave = False
                self.current_percept.stench = False
                self.current_percept.breeze = False
                self.current_percept.glitter = False

        # Based on a random probability, the wumpus will change rotation direction
        if (random.randint(0, 1000 - 1)) < (SCREAM_PROBABILITY * 1000):
            if 1 in self.current_state.wumpus_rotations or 2 in self.current_state.wumpus_rotations:
                self.current_percept.scream = True
                for i in range(self.current_state.wumpus_count):
                    self._reverse_wumpus_direction(index=i)

        # Process the wumpus move based on certain conditions:
        #  Only process a move if the agent hasn't died/is in the cave and the wumpus is alive
        for i in range(self.current_state.wumpus_count):
            if self.current_state.agent_alive and self.current_state.agent_in_cave and self.current_state.wumpus_alive[i]:
                self._process_wumpus_moves(index=i)  # process the wumpus movement only after the player has moved.

                # Now that the wumpus has moved, check for player safety
                if self.current_state.agent_location == self.current_state.wumpus_locations[i]:
                    self.current_state.agent_alive = False

        # The compass action is processed only after the wumpus has moved and if the compass is enabled
        if action == COMPASS and not self.disable_compass:
            self.current_percept.compass = "["
            for i in range(self.current_state.wumpus_count):
                if i > 0:
                    self.current_percept.compass += ","

                if self.current_state.wumpus_alive[i] and self.current_state.wumpus_rotations[i] != 0:
                    self.current_percept.compass += "({},{})".format(self.current_state.wumpus_locations[i].x,
                                                                     self.current_state.wumpus_locations[i].y)
                else:  # if there is no wumpus alive or the wumpus is static, write (0,0)
                    self.current_percept.compass += "(0,0)"

            self.current_percept.compass += "]"

    def _process_wumpus_moves(self, index):
        """ process_wumpus_move: process the wumpus move if there are moves available """

        if self.current_state.wumpus_movement_queues[index] is None or self.current_state.wumpus_movement_queues[index].empty():
            return  # Don't move the wumpus if there are no moves to make

        # Get the next location and recycle it
        next_location = self.current_state.wumpus_movement_queues[index].get()
        self.current_state.wumpus_movement_queues[index].put(next_location)

        # Set the wumpus's current location to the new location
        self.current_state.wumpus_locations[index] = next_location

    def _reverse_wumpus_direction(self, index):
        que = self.current_state.wumpus_movement_queues[index]
        aux_stack = []
        while not que.empty():
            aux_stack.append(que.get())

        while len(aux_stack) > 0:
            que.put(aux_stack.pop())

        self.current_state.wumpus_movement_queues[index] = que

    def game_over(self):
        """ game_over: return True if the game is over, False otherwise"""
        return not self.current_state.agent_in_cave or not self.current_state.agent_alive

    def get_score(self):
        """ get_score: return the score for the current state of the game """

        score = 0

        if not self.current_state.agent_alive:
            return 0.0  # return 0 if the agent died, agent does not get points for any gold found

        if not self.current_state.agent_in_cave:
            # the agent is not in the cave (climbed out) so count up the gold
            for i in range(len(self.current_state.agent_has_gold)):
                if self.current_state.agent_has_gold[i]:
                    score += 1  # +1 for leaving the cave with a gold

        return score / len(self.current_state.agent_has_gold)

    def print_world(self):
        """ print_world: print the current wumpus world"""

        print("World size = {}x{}".format(WORLD_SIZE, WORLD_SIZE))

        # print out the first horizontal line
        out = "+"
        for x in range(1, WORLD_SIZE + 1):
            idx = Wall.locate_wall(self.current_state.walls, x, WORLD_SIZE)
            if idx >= 0 and self.current_state.walls[idx].top:
                out += "-----+"
            else:
                out += "     +"

        print(out)

        for y in range(WORLD_SIZE, 0, -1):  # print starting from the 'bottom' up

            # print out the first row, containing pits + gold + wumpus
            idx = Wall.locate_wall(self.current_state.walls, 1, y)
            if idx >= 0 and self.current_state.walls[idx].left:
                out = "|"
            else:
                out = " "

            for x in range(1, WORLD_SIZE + 1):
                printed_wumpus = False
                for i in range(self.current_state.wumpus_count):
                    if self.current_state.wumpus_locations[i] == Location(x, y):
                        if self.current_state.wumpus_alive:
                            out += "W "
                            printed_wumpus = True
                            break  # removed check if wumpus is dead to the print 'x'
                if not printed_wumpus:
                    out += "  "

                printed_gold = False
                for i in range(self.current_state.wumpus_count):
                    if not self.current_state.agent_has_gold[i] and self.current_state.gold_locations[i] == Location(x, y):
                        out += "G"
                        printed_gold = True
                        break
                if not printed_gold:
                    out += " "

                _has_pit = False
                for pit in self.current_state.pit_locations:
                    if pit == Location(x, y):
                        _has_pit = True
                if _has_pit:
                    out += " P"
                else:
                    out += "  "

                idx = Wall.locate_wall(self.current_state.walls, x, y)
                if idx >= 0 and self.current_state.walls[idx].right:
                    out += "|"
                else:
                    out += " "

            print(out)

            # print out the second row, containing the agent
            idx = Wall.locate_wall(self.current_state.walls, 1, y)
            if idx >= 0 and self.current_state.walls[idx].left:
                out = "|"
            else:
                out = " "

            for x in range(1, WORLD_SIZE + 1):
                if self.current_state.agent_alive and self.current_state.agent_location == Location(x, y):
                    if self.current_state.agent_orientation == RIGHT:
                        out += "  A >"
                    elif self.current_state.agent_orientation == UP:
                        out += "  A ^"
                    elif self.current_state.agent_orientation == LEFT:
                        out += "  A <"
                    else:
                        out += "  A v"
                else:
                    out += "     "

                idx = Wall.locate_wall(self.current_state.walls, x, y)
                if idx >= 0 and self.current_state.walls[idx].right:
                    out += "|"
                else:
                    out += " "

            print(out)
            out = "+"

            # print out the final horizontal line
            for x in range(1, WORLD_SIZE + 1):
                idx = Wall.locate_wall(self.current_state.walls, x, y)
                if idx >= 0 and self.current_state.walls[idx].bottom:
                    out += "-----+"
                else:
                    out += "     +"

            print(out)

        # print the current percepts for the agent's location
        print("Current percept = [stench={},breeze={},glitter={},bump={},scream={},compass={}]".format(
            self.current_percept.stench,
            self.current_percept.breeze,
            self.current_percept.glitter,
            self.current_percept.bump,
            self.current_percept.scream,
            self.current_percept.compass))

        print("Agent has gold = {}".format(self.current_state.agent_has_gold))
        print("Current score = {}, Number of moves = {}".format(self.get_score(), self.num_actions))
        print()


class WumpusWorldFileInformation(object):
    def __init__(self, filename):
        self.world_size = WORLD_SIZE
        self.wumpus_count = 0
        self.wumpus_locations = []
        self.wumpus_rotations = []
        self.gold_locations = []
        self.pit_locations = []
        self.walls = []

        with open(filename, "r") as infile:
            lines = infile.readlines()

            self._process_size(lines[0])
            self._process_wumpus_count(lines[1])

            for _ in range(self.wumpus_count):
                self.wumpus_locations.append(None)
                self.wumpus_rotations.append(None)
                self.gold_locations.append(None)

            for idx in range(2, len(lines)):
                line = lines[idx]
                tokens = line.split(' ')
                if len(tokens) > 0:
                    if tokens[0] == "wumpus":
                        self._process_wumpus(line)
                    elif tokens[0] == "wumpus_rotation":
                        self._process_wumpus_rotation(line)
                    elif tokens[0] == "gold":
                        self._process_gold(line)
                    elif tokens[0] == "pit":
                        self._process_pits(line)
                    elif tokens[0] == "wall":
                        self._process_wall(line)
                    else:
                        print("Unknown token '{}' found in world file.".format(tokens[0]))
                        sys.exit(1)

    def _process_size(self, line):
        size_tokens = line.strip().split(" ")
        if len(size_tokens) != 2 or size_tokens[0] != "size":
            print("Incorrect token in world file '{}', expected 'size'".format(size_tokens[0]))
            sys.exit(1)

        self.world_size = int(size_tokens[1])
        if self.world_size < 2:
            print("Invalid world size, size < 2.")
            sys.exit(1)

        # if the size of the map is different than 4, then the world size will need updating.
        update_global_world_size(self.world_size)

    def _process_wumpus_count(self, line):
        tokens = line.strip().split(" ")
        if len(tokens) != 2 or tokens[0] != "wumpus_count":
            print("Incorrect token in world file '{}', expected 'wumpus_count'".format(tokens[0]))
            sys.exit(1)

        self.wumpus_count = int(tokens[1])

    def _process_wumpus(self, line):
        tokens = line.strip().split(" ")
        if len(tokens) != 4 or tokens[0] != "wumpus":
            print("Incorrect token in world file '{}', expected 'wumpus'".format(tokens[0]))
            sys.exit(1)

        idx = int(tokens[1]) - 1
        loc_x = int(tokens[2])
        loc_y = int(tokens[3])

        if (1 > loc_x > self.world_size) or (1 > loc_y > self.world_size) or (loc_x == 1 and loc_y == 1):
            print("Bad wumpus location in world file for location ({}, {}).".format(loc_x, loc_y))
            sys.exit(1)

        # Create a new location object and set it to the wumpus location
        self.wumpus_locations[idx] = Location(loc_x, loc_y)

    def _process_wumpus_rotation(self, line):
        tokens = line.strip().split(" ")
        if len(tokens) != 3 or tokens[0] != "wumpus_rotation":
            print("Incorrect token in world file '{}', expected 'wumpus_rotation'".format(tokens[0]))
            sys.exit(1)

        idx = int(tokens[1]) - 1
        rot = int(tokens[2])
        if rot < 0 or rot > 2:
            print("Invalid wumpus rotation code; 0 (static), 1 (clockwise), or 2 (counter-clockwise) only accepted.")
            sys.exit(1)

        self.wumpus_rotations[idx] = rot

    def _process_gold(self, line):
        tokens = line.strip().split(" ")
        if len(tokens) != 4 or tokens[0] != "gold":
            print("Incorrect token in world file '{}', expected 'gold'".format(tokens[0]))
            sys.exit(1)

        idx = int(tokens[1]) - 1
        loc_x = int(tokens[2])
        loc_y = int(tokens[3])

        if (1 > loc_x > self.world_size) or (1 > loc_y > self.world_size) or (loc_x == 1 and loc_y == 1):
            print("Bad gold location in world file for location ({}, {}).".format(loc_x, loc_y))
            sys.exit(1)

        # Create a new location object and set it to the gold location
        self.gold_locations[idx] = Location(loc_x, loc_y)

    def _process_pits(self, line):
        tokens = line.strip().split(" ")
        if len(tokens) != 3 or tokens[0] != "pit":
            print("Incorrect token in world file '{}', expected 'pit'".format(tokens[0]))
            sys.exit(1)

        loc_x = int(tokens[1])
        loc_y = int(tokens[2])

        if (1 > loc_x > self.world_size) or (1 > loc_y > self.world_size) or (loc_x == 1 and loc_y == 1):
            print("Bad pit location in world file for location ({}, {}).".format(loc_x, loc_y))
            sys.exit(1)

        # Create a new location object and append it to the pit locations
        self.pit_locations.append(Location(loc_x, loc_y))

    def _process_wall(self, line):
        tokens = line.strip().split(" ")
        if len(tokens) != 4 or tokens[0] != "wall":
            print("Incorrect token in world file '{}', expected 'wall' with arguments".format(tokens[0]))
            sys.exit(1)

        d = int(tokens[1])
        x = int(tokens[2])
        y = int(tokens[3])

        idx = Wall.locate_wall(self.walls, x, y)
        if idx >= 0:
            wall = self.walls[idx]
            if d == UP:
                wall.top = True
            elif d == LEFT:
                wall.left = True
            elif d == DOWN:
                wall.bottom = True
            elif d == RIGHT:
                wall.right = True
        else:
            wall = Wall(x, y)
            if d == UP:
                wall.top = True
            elif d == LEFT:
                wall.left = True
            elif d == DOWN:
                wall.bottom = True
            elif d == RIGHT:
                wall.right = True
            self.walls.append(wall)


class Agent(object):
    def __init__(self, manual=False):
        """ :param boolean manual: specify to true to utilize the manual agent """
        self.manual_agent = manual

    def initialize(self):
        """ initialize: call the agent's initialize method """
        if self.manual_agent:
            ManualPyAgent.pyagent_initialize()
        else:
            PyAgent.pyagent_initialize()

    def process(self, percept):
        """ process: call the agent's process method, passing to it the percepts """
        if self.manual_agent:
            return ManualPyAgent.pyagent_process(percept.stench, percept.breeze, percept.glitter, percept.bump, percept.scream, percept.compass)
        else:
            return PyAgent.pyagent_process(percept.stench, percept.breeze, percept.glitter, percept.bump, percept.scream, percept.compass)


def action_to_string(action):
    """ action_to_string: return a string from the given action """
    if action == GOFORWARD:
        return "GOFORWARD"
    if action == TURNRIGHT:
        return "TURNRIGHT"
    if action == TURNLEFT:
        return "TURNLEFT"
    if action == GRAB:
        return "GRAB"
    if action == CLIMB:
        return "CLIMB"
    if action == WAIT:
        return "WAIT"
    if action == COMPASS:
        return "COMPASS"
    return "UNKNOWN ACTION"


def update_global_world_size(size):
    """ update_global_world_size: update the global world size """
    global WORLD_SIZE
    WORLD_SIZE = size


def update_global_scream_probability(probability):
    """ update_global_scream_probability: update the global scream probability """
    global SCREAM_PROBABILITY
    SCREAM_PROBABILITY = probability


def main(args):
    """ main: the main driver for the wumpus simulator
              iterates over each trial, creating a new wumpus world
              then allows for the given number of tries for that world """

    print("Welcome to the Python Wumpus World Simulator {} by Erik Phillips. Happy Hunting!\n".format(WUMPSIM_VERSION))

    # Set random number generator seed
    # If no seed is given, args.seed is None, therefore the seed will be random
    random.seed(args.seed)

    # Update the global world size if specified in the args
    if args.size is not None:
        update_global_world_size(args.size)

    # update the global scream probability if specified in the args
    if args.scream_probability is not None:
        update_global_scream_probability(args.scream_probability)

    # Initialize the world, using the file information if provided
    file_information = None
    if args.world is not None:  # if there is a world file, process it
        file_information = WumpusWorldFileInformation(args.world)

    wumpus_world = WumpusWorld(file_information=file_information,
                               static_wumpus=args.static_wumpus,
                               disable_compass=args.disable_compass)  # new wumpus world

    # Initialize the simulator's agent object
    agent = Agent(args.manual)
    wumpus_world.initialize()  # call initialize on the wumpus world, resetting for the try
    agent.initialize()  # call the initialize method for the imported agent

    num_moves = 0
    max_moves = WORLD_SIZE * WORLD_SIZE * 10  # WORLD_SIZE ^ 2 * 10 (num tiles * 10 moves per tile)
    if args.max_moves is not None:
        max_moves = args.max_moves

    while (not wumpus_world.game_over()) and (num_moves < max_moves):
        wumpus_world.print_world()
        percept = wumpus_world.get_percept()  # get the percepts for the current location
        action = agent.process(percept)  # and pass the percepts to the imported agent, expecting an action

        print("Action = {}".format(action_to_string(action)))
        print()

        wumpus_world.execute_action(action)  # execute the action in the wumpus world
        num_moves += 1

    score = wumpus_world.get_score()  # get the final score for the world

    print()
    print("World completed, number of moves: {}, score: {:.2f}".format(num_moves, score))
    print("Thanks for playing!")
    print()

    # Return a tuple with the number of moves and the total score
    return num_moves, score


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser("Wumpsim.py")
    parser.add_argument('-max-moves', type=int,
                        help="override the default maximum number of moves")
    parser.add_argument('-seed', type=int,
                        help="set a random seed for world generation, used for pit, gold, and wumpus locations")
    parser.add_argument('-size', type=int, default=None,
                        help="override the default ({}) world size".format(WORLD_SIZE))
    parser.add_argument('-world', type=str,
                        help="specify a world file where the world file is encoded from the parser")
    parser.add_argument('-manual', action="store_true",
                        help="specify this flag to use the manual python agent")
    parser.add_argument('-static-wumpus', action="store_true",
                        help="specify flag to set the wumpus to a random static location")
    parser.add_argument('-disable-compass', action="store_true",
                        help="when specified, the agent cannot query the compass.")
    parser.add_argument('-scream-probability', type=float,
                        help="specify a custom scream probability.")

    args = parser.parse_args()

    if args.seed and args.seed <= 0:
        raise argparse.ArgumentTypeError("Seed must be a positive integer")

    if args.scream_probability is not None and (args.scream_probability < 0 or args.scream_probability > 1):
        raise argparse.ArgumentTypeError("Scream probability must be 0 <= p <= 1")

    main(args)
