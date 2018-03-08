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
        # Kartik's
        "all x. Stench(x) -> exists y. Wumpus(y) & Adjacent(x, y)"
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

    immediate_action = check_immediate_action(glitter, bump, compass, actions)
    if immediate_action:
        return immediate_action

    update_KB(stench, breeze, scream)

    #action = determine_best_action(actions)
    move = pick_best_move(["TURNLEFT", "TURNRIGHT", "GOFORWARD"])

    return actions[move]


def check_immediate_action(glitter, bump, compass, actions):
    compass_threshold = 3

    handle_compass(compass)

    if KB.num_moves <= compass_threshold:
        return actions["COMPASS"]

    update_wupmus_loc()

    if bump:
        return handle_bump(actions)

    print("AGENT_LOCATION:", KB.agent_loc)
    print("AGENT_DIR:", KB.agent_dir)
    print("WUMPUS LOCATIONS:", KB.wumpus_locations)
    #print("SENTENCES:")
    #for sentence in KB.sentences:
    #    print(sentence)

    KB.tell("Explored({}_{})".format(KB.agent_loc[0], KB.agent_loc[1]))
    tell_adjacent_cells()

    if glitter == 1:
        # there is gold, pick it up
        return actions["GRAB"]


def update_KB(stench, breeze, scream):
    if stench == 1:
        # there is a wumpus in one of the adjacent cells
        KB.tell("Stench({})".format(KB.agent_loc[0], KB.agent_loc[1]))
    else:
        # there are no wumpuses in the adjacent cells
        KB.tell("all x.(Adjacent({}, x) -> -Wumpus(x))".format(
            KB.agent_loc[0],
            KB.agent_loc[1]
        ))

    if breeze == 1:
        # there is a pit in one of the adjacent cells
        KB.tell("Breeze({})".format(KB.agent_loc[0], KB.agent_loc[1]))
    else:
        # there is not a pit in any of the adjacent cells
        KB.tell("all x.(Adjacent({}, x) -> -Pit(x))".format(
            KB.agent_loc[0],
            KB.agent_loc[1]
        ))

    if scream == 1:
       # Dynamic wumpuses are changing direction
       KB.wumpus_direction *= -1



def handle_compass(compass):
    if compass is not None: # parse compass string
        compass_array = [tuple(int(n) for n in sub.split(","))
                         for sub in compass[2:-2].split("),(")]

        KB.num_wumpuses = len(compass_array)

        new_wumpus_locations = []

        for i in range(len(compass_array)):
            loc = compass_array[i]
            if loc != (0, 0):
                new_wumpus_locations.append(loc)
                if len(KB.wumpus_locations) > 0:
                    delta_x = loc[0] - KB.wumpus_locations[i][0]
                    delta_y = loc[1] - KB.wumpus_locations[i][1]
                    if len(KB.delta_locations) == 0:
                        KB.delta_locations.append((delta_x, delta_y))
                    else:
                        KB.delta_locations[i].append((delta_x, delta_y))

        KB.wumpus_locations = new_wumpus_locations

        if len(KB.delta_locations) > 0:
            set_wumpus_indecies()


def set_wumpus_indecies():
    wumpus_moves = [
        (1, 0), (1, 0),
        (0, -1), (0, -1),
        (-1, 0), (-1, 0),
        (0, 1), (0, 1)
    ]

    for deltas in KB.delta_locations:
        print(deltas)
        if deltas[0] == deltas[1]:
            delta = deltas[0]
            is_second_occurance = false
        else:
            delta = deltas[1]
            is_second_occurance = true

        for i in range(len(wumpus_moves)):
            if delta == wumpus_moves[i]:
                print(delta, wumpus_moves[i])
                index = i
                if is_second_occurance:
                    index += 1

                print(index)
                KB.wumpus_indecies.append(index)


def update_wupmus_loc():
    wumpus_moves = [(1, 0), (0, -1), (-1, 0), (0, 1)]
    print("WUMPUS INDECIES:", KB.wumpus_indecies)
    print("WUMPUS LOCATIONS:", KB.wumpus_locations)

    for i in range(len(KB.wumpus_locations)):
        wumpus_index = (KB.wumpus_indecies[i] + KB.wumpus_direction) % 4
        KB.wumpus_indecies[i] = wumpus_index
        print("WUMPUS INDEX:", wumpus_index)
        wumpus_move = wumpus_moves[wumpus_index]
        new_x = KB.wumpus_locations[i][0] + wumpus_move[0]
        new_y = KB.wumpus_locations[i][1] + wumpus_move[1]
        KB.wumpus_locations[i] = (new_x, new_y)


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
        if value > max_value:
            max_value = value
            best_move = move

    if max_value < 0:
        return "WAIT"

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
    cell_value = 1

    is_safe = KB.ask("StaticSafe({}_{})".format(cell[0], cell[1]))
    is_explored = KB.ask("Explored({}_{})".format(cell[0], cell[1]))
    is_wumpus = KB.ask("Wumpus({}_{})".format(cell[0], cell[1]))
    is_pit = KB.ask("Pit({}_{})".format(cell[0], cell[1]))
    is_wall = KB.ask("Wall({}_{}, {}_{})".format(
        KB.agent_loc[0],
        KB.agent_loc[1],
        cell[0],
        cell[1]
    ))

    if is_wumpus or is_pit or is_wall:
        cell_value -= 100

    elif is_safe:
        cell_value += 1

        if is_explored:
            cell_value -= 0.04

    return cell_value


def determine_best_action(actions):
    next_cell = get_next_cell(1, KB.agent_dir)
    if KB.ask("StaticSafe({}_{})".format(next_cell[0], next_cell[1])):
        update_agent_loc()
        return actions["GOFORWARD"]
    else:
        random_chance = random.random()
        if random_chance < 0.4:
            update_agent_direction("TURNLEFT")
            return actions["TURNLEFT"]
        elif 0.4 < random_chance < 0.8:
            update_agent_direction("TURNRIGHT")
            return actions["TURNRIGHT"]
        else:
            update_agent_loc()
            return actions["GOFORWARD"]


def get_next_cell(direction, agent_dir):
    dir_map = {
        'N': [0, 1],
        'S': [0, -1],
        'E': [1, 0],
        'W': [-1, 0],
    }

    next_x = KB.agent_loc[0] + direction * dir_map[agent_dir][0]
    next_y = KB.agent_loc[1] + direction * dir_map[agent_dir][1]

    return [next_x, next_y]


def update_agent_loc(direction = 1):
    next_cell = get_next_cell(direction, KB.agent_dir)
    KB.agent_loc = [next_cell[0], next_cell[1]]


def update_agent_direction(action):
    dir_map = {
        'N': {'TURNLEFT' : 'W', 'TURNRIGHT' : 'E'},
        'E': {'TURNLEFT' : 'N', 'TURNRIGHT' : 'S'},
        'S': {'TURNLEFT' : 'E', 'TURNRIGHT' : 'W'},
        'W': {'TURNLEFT' : 'S', 'TURNRIGHT' : 'N'},
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
        self.agent_loc = [1, 1]
        self.agent_dir = "E"
        self.num_moves = 0
        self.num_wumpuses = 0
        self.wumpus_direction = 1
        self.delta_locations = []
        self.wumpus_indecies = []
        self.wumpus_locations = []

    def tell(self, sentence):
        if sentence not in self.used_sentences:
            self.used_sentences.add(sentence)
            self.sentences.append(logic.Expression.fromstring(sentence))

    def ask(self, sentence):
        sentence = logic.Expression.fromstring(sentence)
        if "ANSWER" in str(sentence):
            prover = inference.ResolutionProverCommand(None, self.sentences)
            prover.add_assumptions([sentence])
            return [list(e.constants())[0].name for e in prover.find_answers()
                    if type(e) is logic.ConstantExpression]
        else:
            return inference.ResolutionProver().prove(sentence, self.sentences)
