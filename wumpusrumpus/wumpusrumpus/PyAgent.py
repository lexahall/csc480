# Name:         Lexa Hall
# Course:       CSC 480
# Instructor:   Daniel Kauffman
# Assignment:   Wumpus Rumpus
# Term:         Winter 2018


import nltk.inference as inference
import nltk.sem.logic as logic
import random


KB = None


def pyagent_initialize():
    global KB
    axioms = [
        "all x. all y.(-Breeze(x) & Adjacent(x, y) -> -Pit(y))",
        "all x. all y.(-Stench(x) & Adjacent(x, y) -> -Wumpus(y))",
        "all x. all y.(-Stench(x) & -Breeze(x) & Adjacent(x, y) -> StaticSafe(y))",
        "all x.(Explored(x) -> -Wumpus(x) & -Pit(x))",
        "all x.(Explored(x) -> StaticSafe(x))",
        "all x.(-Pit(x) & -Wumpus(x) -> StaticSafe(x))",
        # "all x. Stench(x) -> exists y. Wumpus(y) & Adjacent(x, y)"
        # "all x. exists y.(Breeze(x) & Adjacent(x, y) -> Pit(y))",
        # "all x. exists y.(Stench(x) & Adjacent(x, y) -> Wumpus(y))",
        # "all x.(StaticSafe(x) -> -Wumpus(x) & -Pit(x))",
        # "all x. all y.(Wall(x, y) -> Wall(y, x))",
        # "all x. all y.(Adjacent(x, y) -> Adjacent(y, x))",
        # "all v. all w. all x. all y. all z.((Breeze(v) & Adjacent(v, z)) & \
        #                                    (Breeze(w) & Adjacent(w, z)) & \
        #                                    (Breeze(x) & Adjacent(x, z)) & \
        #                                    (Breeze(y) & Adjacent(y, z)) -> \
        #                                    Pit(z))",
        # "all v. all w. all x. all y. all z.((Stench(v) & Adjacent(v, z)) & \
        #                                    (Stench(w) & Adjacent(w, z)) & \
        #                                    (Stench(x) & Adjacent(x, z)) & \
        #                                    (Stench(y) & Adjacent(y, z)) -> \
        #                                    Wumpus(z))",
    ]
    KB = KnowledgeBase(axioms)


def pyagent_process(stench, breeze, glitter, bump, scream, compass):
    global KB

    print("pyagent_process:",
          ", ".join("{0}={1}".format(k, v) for k, v in locals().items()))

    actions = {"GOFORWARD": 0, "TURNLEFT": 1, "TURNRIGHT": 2, "GRAB": 3,
               "CLIMB": 5, "WAIT": 6, "COMPASS": 7}

    KB.num_moves += 1

    immediate_action = check_immediate_action(glitter, bump, compass, actions,
        scream)
    if immediate_action:
        return immediate_action

    update_KB(stench, breeze, scream)

    move = pick_best_move(["TURNLEFT", "TURNRIGHT", "GOFORWARD"])

    if move == "TURNLEFT" or move == "TURNRIGHT":
      update_agent_direction(move)
    else:
      update_agent_loc()

    return actions[move]


def check_immediate_action(glitter, bump, compass, actions, scream):
    handle_compass(compass, scream)

    if KB.wumpus_rotation == None:
        return actions["COMPASS"]

    update_wumpus_locations()

    if bump:
        return handle_bump(actions)

    if KB.agent_gold == KB.num_wumpuses and KB.agent_loc == (1, 1):
      return actions["CLIMB"]

    KB.tell("Explored({}_{})".format(KB.agent_loc[0], KB.agent_loc[1]))
    tell_adjacent_cells()

    if glitter == 1:
        # there is gold, pick it up
        KB.agent_gold += 1
        return actions["GRAB"]


def update_KB(stench, breeze, scream):
    if stench == 1:
        # there is a wumpus in one of the adjacent cells
        KB.tell("Stench({}_{})".format(KB.agent_loc[0], KB.agent_loc[1]))
    else:
        # there are no wumpuses in the adjacent cells
        KB.tell("all x.(Adjacent({}_{}, x) -> -Wumpus(x))".format(
            KB.agent_loc[0],
            KB.agent_loc[1]
        ))

    if breeze == 1:
        # there is a pit in one of the adjacent cells
        KB.tell("Breeze({}_{})".format(KB.agent_loc[0], KB.agent_loc[1]))
    else:
        # there is not a pit in any of the adjacent cells
        KB.tell("all x.(Adjacent({}_{}, x) -> -Pit(x))".format(
            KB.agent_loc[0],
            KB.agent_loc[1]
        ))


    if scream == 1:
        print()
        print("----------------------------------------------------------------")
        print("SCREAM")
        print()

        # Dynamic wumpuses are changing direction
        for i in range(len(KB.wumpus_delays)):
            if len(KB.wumpus_indecies) > i:
                previous_index = KB.wumpus_indecies[i] - KB.wumpus_rotation
                if len(KB.wumpus_moves) > previous_index:
                    previous_delta = KB.wumpus_moves[previous_index]
                    if previous_delta == (0, 0):
                        KB.wumpus_delays[i] = 1
                    else:
                        KB.wumpus_delays[i] = 2
        KB.wumpus_rotation *= -1


def handle_compass(compass, scream):
    if compass is not None: # parse compass string
        compass_array = [tuple(int(n) for n in sub.split(","))
                         for sub in compass[2:-2].split("),(")]

        KB.num_wumpuses = len(compass_array)
        new_wumpus_locations = []

        if scream:
            KB.restart_compass = True

        if not KB.restart_compass:
            index = 0
            for loc in compass_array:
                if loc != (0, 0):
                    new_wumpus_locations.append(loc)
                    if len(KB.wumpus_locations) > 0 and not scream:
                        delta_x = loc[0] - KB.wumpus_locations[index][0]
                        delta_y = loc[1] - KB.wumpus_locations[index][1]
                        KB.delta_locations[index].append((delta_x, delta_y))
                    index += 1
        else:
            KB.restart_compass = False

        KB.wumpus_locations = new_wumpus_locations
        initialize_dynamic_wumpus_data(scream)


def initialize_dynamic_wumpus_data(scream):
    if len(KB.wumpus_locations) == 0 and KB.num_moves > 2:
        KB.wumpus_rotation = 0
        return

    if len(KB.wumpus_delays) == 0:
        for i in range(len(KB.wumpus_locations)):
            KB.wumpus_delays.append(0)

    if len(KB.delta_locations) == 0 or scream:
        KB.delta_locations = [[] for i in range(len(KB.wumpus_locations))]
    elif len(KB.delta_locations[0]) >= 6:
        KB.predicted_wumpus_locations = [
            [] for i in range(len(KB.wumpus_locations))
        ]
        set_wumpus_indecies()


def set_wumpus_indecies():
    for deltas in KB.delta_locations:
        KB.wumpus_indecies.append(find_subsequence(deltas, KB.wumpus_moves))


def find_subsequence(subseq, seq):
    for k in range(len(seq)):
        sequence_found = True

        if subseq[0] == seq[k]:
            j = 0

            for i in range(len(subseq)):
                if j + k == len(seq):
                    j = 0
                    k = 0
                if subseq[i] != seq[j + k]:
                    sequence_found = False
                    break
                j += 1

            if sequence_found:
              KB.wumpus_rotation = 1
              return j + k - 1

    else:
        return find_reverse_subsequence(subseq, seq)


def find_reverse_subsequence(subseq, seq):
    for k in range(len(seq) - 1, -1, -1):
        sequence_found = True

        if subseq[0] == seq[k]:
            j = 0

            for i in range(len(subseq)):
                if j + k == -1:
                    j = 0
                    k = len(seq) - 1

                if subseq[i] != seq[j + k]:
                    sequence_found = False
                    break
                j -= 1

            if sequence_found:
              KB.wumpus_rotation = -1
              return j + k + 1

    else:
        return -1


def update_wumpus_locations():
    print("WUMPUS INDICIES:", KB.wumpus_indecies)
    print("PREVIOUS WUMPUS LOCATIONS:", KB.wumpus_locations)
    current_loc = 1
    next_loc = 2

    for i in range(len(KB.wumpus_locations)):
        if KB.wumpus_delays[i] == 0:
            KB.wumpus_locations[i] = calc_wumpus_loc(i)
            print("CURRENT WUMPUS LOCATIONS:", KB.wumpus_locations)
            KB.predicted_wumpus_locations[i] = calc_wumpus_loc(i)
        else:
            print("delaying the wumpus")
            KB.wumpus_delays[i] -= 1

    print("PREDICTED WUMPUS LOCATIONS:", KB.wumpus_locations)
    print()


def calc_wumpus_loc(index):
    print(KB.wumpus_indecies[index])
    print(KB.wumpus_rotation)
    wumpus_index = (
        (KB.wumpus_indecies[index] + KB.wumpus_rotation) %
        len(KB.wumpus_moves)
    )
    print("WUMPUS INDEX:", wumpus_index)
    KB.wumpus_indecies[index] = wumpus_index
    wumpus_move = KB.wumpus_moves[wumpus_index]
    print("WUMPUS MOVE:", wumpus_move)
    new_x = KB.wumpus_locations[index][0] + wumpus_move[0]
    new_y = KB.wumpus_locations[index][1] + wumpus_move[1]

    return (new_x, new_y)


def handle_bump(actions):
    attempted_loc = KB.agent_loc
    update_agent_loc(-1)
    tell_wall(KB.agent_loc, attempted_loc)

    move = pick_best_move(["TURNLEFT", "TURNRIGHT"])

    update_agent_direction(move)
    return actions[move]


def pick_best_move(moves):
    max_value = -100
    for move in moves:
        cell = get_cell_from_move(move)
        value = evaluate_cell(cell)
        if value >= max_value:
            max_value = value
            best_move = move

    if max_value < 0:
        return "TURNLEFT"

    if max_value == 1:
        if KB.agent_loc == (1, 1):
          return "GOFORWARD"
        else:
          return "TURNLEFT"

    return best_move


def get_cell_from_move(move):
    if move == "GOFORWARD":
        return get_next_cell(1, KB.agent_dir)

    dir_map = {
        'N': {'TURNLEFT' : 'W', 'TURNRIGHT' : 'E'},
        'E': {'TURNLEFT' : 'N', 'TURNRIGHT' : 'S'},
        'S': {'TURNLEFT' : 'E', 'TURNRIGHT' : 'W'},
        'W': {'TURNLEFT' : 'S', 'TURNRIGHT' : 'N'},
    }

    agent_dir = dir_map[KB.agent_dir][move]
    return get_next_cell(1, agent_dir)


def evaluate_cell(cell):
    #print()
    death_penalty = 100
    cell_value = 1

    if KB.agent_gold == KB.num_wumpuses:
        explored_penalty = -1
        if is_towards_home(cell):
          #print("towards home, +1")
          cell_value += 1
    else:
        explored_penalty = 0.04

    is_safe = KB.ask("StaticSafe({}_{})".format(cell[0], cell[1]))

    is_explored = KB.ask("Explored({}_{})".format(cell[0], cell[1]))

    is_pit = KB.ask("Pit({}_{})".format(cell[0], cell[1]))

    is_wumpus = check_for_wumpus(cell)

    is_wall = KB.ask("Wall({}_{}, {}_{})".format(
        KB.agent_loc[0],
        KB.agent_loc[1],
        cell[0],
        cell[1]
    ))

    if is_wumpus or is_pit or is_wall:
        cell_value -= death_penalty

    elif is_safe:
        #print("towards safe, +1")
        cell_value += 1

        if is_explored:
            cell_value -= explored_penalty

    #print("Current cell:", cell)
    #print("is_explored:", is_explored)
    #print("is_wumpus:", is_wumpus)
    #print("is_pit:", is_pit)
    #print("is_not_wumpus:", is_not_wumpus)
    #print("is_not_pit:", is_not_pit)
    #print("is_safe:", is_safe)
    #print("is_wall:", is_wall)

    return cell_value


def check_for_wumpus(cell):
    is_wumpus = KB.ask("Wumpus({}_{})".format(cell[0], cell[1]))
    if is_wumpus:
      return is_wumpus

    for loc in KB.predicted_wumpus_locations:
        if loc == cell:
            return True

    for loc in KB.wumpus_locations:
        if loc == cell:
            return True

    return False



def is_towards_home(cell):
    home = (1, 1)
    old_manhattan_dist = get_manhattan_dist(KB.agent_loc, home)
    new_manhattan_dist = get_manhattan_dist(cell, home)

    if new_manhattan_dist < old_manhattan_dist:
        return True

    return False


def get_manhattan_dist(cell, home):
    return abs(cell[0] - home[0]) + abs(cell[1] - home[1])


def get_next_cell(direction, agent_dir):
    dir_map = {
        'N': [0, 1],
        'S': [0, -1],
        'E': [1, 0],
        'W': [-1, 0],
    }

    next_x = KB.agent_loc[0] + direction * dir_map[agent_dir][0]
    next_y = KB.agent_loc[1] + direction * dir_map[agent_dir][1]

    return (next_x, next_y)


def update_agent_loc(direction = 1):
    next_cell = get_next_cell(direction, KB.agent_dir)
    KB.agent_loc = (next_cell[0], next_cell[1])


def update_agent_direction(action):
    dir_map = {
        'N': {'TURNLEFT' : 'W', 'TURNRIGHT' : 'E', 'GOFORWARD' : 'N'},
        'E': {'TURNLEFT' : 'N', 'TURNRIGHT' : 'S', 'GOFORWARD' : 'E'},
        'S': {'TURNLEFT' : 'E', 'TURNRIGHT' : 'W', 'GOFORWARD' : 'S'},
        'W': {'TURNLEFT' : 'S', 'TURNRIGHT' : 'N', 'GOFORWARD' : 'W'},
    }

    KB.agent_dir = dir_map[KB.agent_dir][action]


def tell_adjacent_cells():
    adjacent_cells = get_adjacent_cells()
    for cell in adjacent_cells:
        KB.tell("Adjacent({}_{}, {}_{})".format(
            KB.agent_loc[0],
            KB.agent_loc[1],
            cell[0],
            cell[1]
        ))
        KB.tell("Adjacent({}_{}, {}_{})".format(
            cell[0],
            cell[1],
            KB.agent_loc[0],
            KB.agent_loc[1]
        ))


def get_adjacent_cells():
    cells = []
    x = KB.agent_loc[0]
    y = KB.agent_loc[1]

    if (x > 1):
        cells.append([x - 1, y])
    else:
        tell_wall([x, y], [x - 1, y])

    if (y > 1):
        cells.append([x, y - 1])
    else:
        tell_wall([x, y], [x, y - 1])

    cells.append([x + 1, y])
    cells.append([x, y + 1])

    #for cell in cells:
    #    unreachable_cell = KB.ask("Wall({}_{}, {}_{})".format(
    #        KB.agent_loc[0],
    #        KB.agent_loc[1],
    #        cell[0],
    #        cell[1]
    #    ))
    #    if unreachable_cell:
    #        cells.remove(cell)

    return cells


def tell_wall(curr, attempted):
    KB.tell("Wall({}_{}, {}_{})".format(
        curr[0],
        curr[1],
        attempted[0],
        attempted[1]
    ))

    KB.tell("Wall({}_{}, {}_{})".format(
        attempted[0],
        attempted[1],
        curr[0],
        curr[1]
    ))


def coordinate_to_string(coordinate):
    return "{}_{}".format(coordinate[0], coordinate[1])


def string_to_coordinate(string):
    values = string.split("_")
    return [int(values[0]), int(values[1])]


class KnowledgeBase(object):

    def __init__(self, axioms = []):
        self.sentences = [logic.Expression.fromstring(a) for a in axioms]
        self.used_sentences = set()
        self.agent_gold = 0
        self.agent_loc = (1, 1)
        self.agent_dir = "E"
        self.num_moves = 0
        self.num_wumpuses = 0
        self.num_dynamic_wumpuses = 0
        self.wumpus_rotation = None
        self.restart_compass = True
        self.wumpus_delays = []
        self.delta_locations = []
        self.wumpus_indecies = []
        self.wumpus_locations = []
        self.predicted_wumpus_locations = []

        self.wumpus_moves = [
            (0, 0),
            (1, 0), (1, 0),
            (0, 0),
            (0, -1), (0, -1),
            (0, 0),
            (-1, 0), (-1, 0),
            (0, 0),
            (0, 1), (0, 1)
        ]


    def tell(self, sentence):
        if sentence not in self.used_sentences:
            self.used_sentences.add(sentence)
            self.sentences.append(logic.Expression.fromstring(sentence))

    def ask(self, sentence):
        sentence = logic.Expression.fromstring(sentence)
        prover = inference.Prover9()
        prover.config_prover9(".")
        return prover.prove(sentence, self.sentences)
