
# WUMPUS PROJECT

**CPE 480:** Artificial Intelligence \
**Professor:** Daniel Kauffman \
**Date:** Winter, 2018 \
_California Polytechnic State University, San Luis Obispo_


## Project Inspirations

The simulator for this project has been built off of the original 
[Wumpus World](https://github.com/erikphillips/wumpus_world)
with additions to make the worlds more interesting and challenging
for the agents competing within the world. The simulator was forked 
from the original at release version
[1.2](https://github.com/erikphillips/wumpus_world/tree/v1.2)


# Wumpus World Simulator
A driver for the wumpus world which allows for students to create their own 
Wumpus World agent to navigate the cave.


## Simulator Details

The simulator works by generating a new world and a new agent for each trial.
Before each try on this world, the agent's `Initialize()` method is called, which
you can use to perform any pre-game preparation. Then, the game starts.  The
agent's `Process()` method is called with the current *Percept*, and the agent
should return an action, which is performed in the simulator. This continues
until the game is over (agent dies or leaves cave) or the maximum number of
moves is exceeded. Scoring information is output at the end of the simulation.

Some important notes: A wumpus or pit will never be at the same location as 
the gold, and the gold will never be at the edge of the map. A wumpus will 
always circle the gold's location.

Please use the simulator with the `-manual` flag to experiment with how the
simulator works and how the entities within the world function.


## Agent Details
Your agent must include at least two methods: `Initialize` and `Process`. 
You may change any or all of these methods to implement your agent, but the
methods must return one of the expected output (applies to `Process` only). 
You may include additional methods as you see fit.


## Python Agent
You will make all your changes to the `PyAgent.py` file. You will see two
functions in the file: `pyagent_initialize` and `pyagent_process`. These 
two functions are called by their counterparts in the simulator. You can
see how this is done in the `Wumpsim.py` file, **BUT DO NOT MODIFY THIS
FILE**.  The only file you should change is `PyAgent.py`. Note that the
`pyagent_process` function takes the five separate percepts, rather than a
`Percept` class instance, and the `pyagent_process` function should return one of
the six actions defined in the `Action.py` file.

Once you've finished your `PyAgent.py` file, simply run the `python3 Wumpsim.py` program
to test your agent. The `PyAgent.py` file and the `Wumpsim.py` script must be
in the same directory. The `Wumpsim.py` program accepts all the simulator options
described below.

### Manual Agent
For testing purposes and for learning about the behavior of the cave, a manual agent has 
been created. `ManualPyAgent.py` is a script that allows for manually entering movements 
for the agent. To run the manual agent, the `ManualyPyAgent.py` script must be in the same 
directory as `Wumpsim.py`. Run the following command:

``` $ python3 Wumpsim.py -manual ```

### Agent Percepts
Percepts are passed to the PyAgent through the following:

```
pyagent_process(stench, breeze, glitter, bump, scream, compass):
    pyagent_process: called with new percepts after each action to return the next action
    :param int stench: 0 (no stench) or 1 (yes stench) representing if there is a stench at the current location
    :param int breeze: 0 (no breeze) or 1 (yes breeze) representing if there is a breeze at the current location
    :param int glitter: 0 (no glitter) or 1 (yes glitter) representing if there is a glitter at the current location
    :param int bump: 0 (no bump) or 1 (yes bump) representing if the agent encountered a bump on the last move
    :param int scream: 0 (no scream) or 1 (yes scream) representing if the agent heard a scream
    :param String compass: string in the format "[(x,y),...]" where x,y represents the all the wumpus current locations
    :return int action: return an action for the agent as described in Action.py
```

Some additional details to note:
- When the agent smells a stench, there is a wumpus in one of the adjacent tiles.
- When the agent feels a breeze, there is a pit in one of the adjacent tiles
- When the agent sees glitter, there is gold at the current location.
- When the agent feels a bump, the agent's move was not allowed due to a wall in it's path.
- When the agent hears a scream, all the wumpus within the world will change their rotation 
directions. Meaning that all agents that were rotation around the gold clockwise, will not 
rotate counter-clockwise and vis-a-versa.
- When the agent asks for the compass, the agent is given a string that will need to be parsed. 
The string represents an array of coordinates for all the wumpus locations. If the `-disable-compass` 
flag is used, then no compass is returned.
- The default maximum number of moves is set to the number of possible tiles in the world times 10 moves allowed per tile. This should allow all agents the ability to navigate the whole entire puzzle and return home.


### Simulator Options
The following options are allowed and provided to the simulator as arguments:

```
usage: Wumpsim.py [-h] [-max-moves MAX_MOVES] [-seed SEED] [-size SIZE]
                  [-world WORLD] [-manual] [-static-wumpus] [-disable-compass]
                  [-scream-probability SCREAM_PROBABILITY]

Optional Arguments:
  
  -seed SEED
    The seed to specify to the random number generator. Specifying a seed 
    allows for the simulator to run the same random worlds.
    Default is None which uses a random component from the system time.
    
  -manual
    If the flag is present, the manual agent will be used allowing for
    manual agent actions provided by the user.
    
  -static-wumpus
    If the flag is present, the wumpus will be static and it's location
    will be generated based off of a random location.
    Otherwise, if the flag is not present, the wumpus will circle the gold.
    
  -size SIZE
    Override the default world size of 4.
    
  -max-moves MAX_MOVES
    Override the maximum number of moves allowed for the agent in the world.
    
  -disable-compass
    Disable the compass percept from being returned.
    
  -scream-probability SCREAM_PROBABILITY
    Specify a custom scream probability between 0 and 1.
    
  -world WORLD
    The world file to as a pre-defined wumpus world. The file must follow a
    specified format (example in 'worlds/' directory). 
    The details of the file are specified below:
      
      size N              # the size of the world (where N is an integer representing the size)
      
      wumpus_count N      # the number of wumpus creatures in the world (where N is an integer)
      
      wumpus I X Y        # the wumpus starting location, where I in the ID and X,Y are the coordinates
      
      wumpus_rotation I D # the wumpus rotational key where I is the ID and D is the rotation direction
                          # D is an integer from the set {static = 0, clockwise = 1, counter-clockwise = 2}
                          
      gold I X Y          # the location of the gold, where I is the gold ID (matching the wumpus ID)
                          # and X,Y are the coordinates of the gold
                          
      pit X Y             # the location of the pit, where X,Y are the coordinates
      
      wall D X Y          # the wall spcification where X,Y are the tile and D is the direction 
                          # as an integer in the set {0 = RIGHT, 1 = UP, 2 = LEFT, 3 = DOWN}

```


## ASCII World Files

The ascii world files follow a strict format, outlined below. I have tried my best to provide error 
messages for issues that may arise, but cannot guarentee that unknown errors will not occur. To verify 
the world, please parse it, then run it in the simulator manually, using the command: 

```
$ python3 WumpusWorldParser.py worlds/ascii_world_template.txt worlds/ascii_world_template.out
$ python3 Wumpsim.py -manual -world=worlds/ascii_world_template.out
```

If an error occurs that the output file already exists, run the Parser with the `--force` flag.


### Header

```
size N              # represents the size of the world, where N >= 2
wumpus_rotation I D # represents the direction of the wumpus rotation, 
                    # where I is the index of the wumpus, and
                    # where D=[static|counter-clockwise|clockwise]
```
***Please note:*** The ordering is enforced and very important and all keys must be specified. 
Special attention should be paid to the `wumpus_rotation` field, as the index must start with 1, 
and increase incrementally from there. Finally, one (1) blank line seperates the header from the ascii world file.


### Tile Format

```
+-----+
|W G P|
|#    |  
+-----+

+ represents corners of a tile (required)
- represents top/bottom walls/borders
| represents left/rights side walls/borders

P represents the location of a pit
W represents the wumpus is at this location (starting location if not static)
G represents the gold's location
# represents the ID of the object (integer representing the index of the object, 1 indexed)
  The ID can take up the whole entire bottom row, and be placed anywhere within the row.
  The only objects that will need an ID are the Wumpus and the Gold.

(the following is for reference only - not included in ascii world file)
A represents the agent's current location (must be located at tile 1, 1 to start) (currently not implementedin ascii parsing)
D represents the agent's current direction/orientation ['>'|'v'|'<'|'^']  (currently not implemented in ascii parsing)
```

***Please note carefully:*** There should be five (5) spaces between the wall layouts for the tile. 
There should be exactly five (5) wall characters on the top/bottom and two (2) wall characters on the right/left sides. 
There is one (1) space seperating the different objects within the tile (one space between 'W' and 'G', etc.). 
There are no spaces between objects and the side walls. When two tiles are placed next to each other, they will share 
a '+' corner and any walls, if present. There should be one (1) blank line at the end of the world file.


## Example Usage
Parse an ascii world: \
``` $ python3 WumpusWorldParser.py worlds/ascii_world_template.txt worlds/ascii_world_template.out ```

Run an encoded world: \
``` $ python3 Wumpsim.py -world=worlds/ascii_world_template.out ```

Run using the manual agent: \
``` $ python3 Wumpsim.py -manual ```

Run using a static wumpus and seeded random generator with larger cave size: \
``` $ python3 Wumpsim.py -seed=1234 -size=6 -static-wumpus ```

Run using a different number of maximum moves: \
``` $ python3 Wumpsim.py -max-moves=10 ```


## Known Issues

- Issue: Processing the wumpus move and the order in which this occurs. Currently the wumpus will move 
after the agent has moved, and this allows for the wumpus to capture the agent without the agent being 
aware of the wumpus through the stench percept. However, by using the compass to detect the location of 
the wumpus, the agent can predict where the wumpus will be located and predict the wumpus movements.


## Acknowledgments
This project was based on the wumpus simulator by Larry Holder:

```
Wumpus Simulator v2.9 (released 09/15/2017)
Copyright (c) 2017. Washington State University.
Written by Larry Holder (holder@wsu.edu).
```

The Python version of this simulator project was written for the CPE 480 class in Artificial Intelligence 
at Cal Poly, San Luis Obispo, CA to replace the C++ implementation of the simulator above.
