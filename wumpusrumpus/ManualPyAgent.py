"""
ManualPyAgent.py contains the logic for providing manual navigation through the world.
The simulator will generate worlds and based on the world, the simulator will call the methods as described below
to allow the manual agent to interact with the world.
"""

# Actions: Defines allowed actions within the world
GOFORWARD = 0
TURNLEFT = 1
TURNRIGHT = 2
GRAB = 3
CLIMB = 5
WAIT = 6
COMPASS = 7


def pyagent_initialize():
    """
    pyagent_initialize: called at the start of a new try
    """

    print("pyagent_initialize")


def pyagent_process(stench, breeze, glitter, bump, scream, compass):
    """
    pyagent_process: called with new percepts after each action to return the next action
    :param int stench: 0 (no stench) or 1 (yes stench) representing if there is a stench at the current location
    :param int breeze: 0 (no breeze) or 1 (yes breeze) representing if there is a breeze at the current location
    :param int glitter: 0 (no glitter) or 1 (yes glitter) representing if there is a glitter at the current location
    :param int bump: 0 (no bump) or 1 (yes bump) representing if the agent encountered a bump on the last move
    :param int scream: 0 (no scream) or 1 (yes scream) representing if the agent heard a scream
    :param String compass: string in the format "[(x,y),...]" where x,y represents the all the wumpus current locations
    :return int action: return an action for the agent as described in py
    """

    percept_str = ""
    if stench == 1:
        percept_str += "Stench=True,"
    else:
        percept_str += "Stench=False,"
    if breeze == 1:
        percept_str += "Breeze=True,"
    else:
        percept_str += "Breeze=False,"
    if glitter == 1:
        percept_str += "Glitter=True,"
    else:
        percept_str += "Glitter=False,"
    if bump == 1:
        percept_str += "Bump=True,"
    else:
        percept_str += "Bump=False,"
    if scream == 1:
        percept_str += "Scream=True,"
    else:
        percept_str += "Scream=False,"

    print("COMPASS:", compass)

    percept_str += "Compass={}".format(compass)

    print("pyagent_process: " + percept_str)

    while True:
        raw_input = input("Enter action [F]orward | [L]eft | [R]ight | [G]rab | [C]ompass | [E]xit/Climb | [W]ait: ")
        raw_input = raw_input.upper()

        if raw_input == "F":
            return GOFORWARD
        elif raw_input == "L":
            return TURNLEFT
        elif raw_input == "R":
            return TURNRIGHT
        elif raw_input == "G":
            return GRAB
        elif raw_input == "C":
            return COMPASS
        elif raw_input == "E":
            return CLIMB
        elif raw_input == "W":
            return WAIT
        else:
            # Continue looping until valid input is recognized, exit with ctrl+d
            print("Unrecognized input, please try again.")
