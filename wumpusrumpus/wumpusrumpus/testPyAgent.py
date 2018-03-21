import PyAgent as agent
import time

def test_KB():
  print()
  print("--------------- KB LOGIC  ----------------")

  print("TEST 16: Wumpus(1_1) does not mean Wumpus(2_2)")
  statements = []

  statement = "Stench(1_1)"
  statements.append(statement)

  statement = "-Wumpus(1_1)"
  statements.append(statement)

  question = "Wumpus(1_1)"
  expected = False
  run_KB_test(statements, question, expected)

  print("TEST 1: Breeze means breeze")
  statements = []

  statement = "Breeze(1_1)"
  statements.append(statement)

  question = "Breeze(1_1)"
  expected = True
  run_KB_test(statements, question, expected)

  print("TEST 1b: Find breeze")
  statements = []

  statement = "Breeze(1_1)"
  statements.append(statement)

  question = "exists x.(Breeze(x) -> ANSWER(x))"
  expected = ["1_1"]
  run_KB_test(statements, question, expected)

  print("TEST 1c: Breeze doesnt mean not breeze")
  statements = []

  statement = "Breeze(1_1)"
  statements.append(statement)

  question = "-Breeze(1_1)"
  expected = False
  run_KB_test(statements, question, expected)

  print("TEST 2: Pit means pit")
  statements = []

  statement = "Pit(1_1)"
  statements.append(statement)

  question = "Pit(1_1)"
  expected = True
  run_KB_test(statements, question, expected)

  print("TEST 3: Wumpus means wumpus")
  statements = []

  statement = "Wumpus(1_1)"
  statements.append(statement)

  question = "Wumpus(1_1)"
  expected = True
  run_KB_test(statements, question, expected)

  print("TEST 4: Stench means Stench")
  statements = []

  statement = "Stench(1_1)"
  statements.append(statement)

  question = "Stench(1_1)"
  expected = True
  run_KB_test(statements, question, expected)

  print("TEST 5: Wall means wall")
  statements = []

  statement = "Wall(1_1, 1_2)"
  statements.append(statement)

  question = "Wall(1_1, 1_2)"
  expected = True
  run_KB_test(statements, question, expected)

  print("TEST 5a: Wall means wall - flipped")
  statements = []

  statement = "Wall(1_1, 1_2)"
  statements.append(statement)

  question = "Wall(1_2, 1_1)"
  expected = True
  #run_KB_test(statements, question, expected)

  print("TEST 5b: Not wall means not wall")
  statements = []

  statement = "-Wall(1_1, 1_2)"
  statements.append(statement)

  question = "-Wall(1_1, 1_2)"
  expected = True
  run_KB_test(statements, question, expected)

  print("TEST 5c: Not wall doesn't mean wall")
  statements = []

  statement = "-Wall(1_1, 1_2)"
  statements.append(statement)

  statement = "-Wall(1_2, 1_1)"
  statements.append(statement)

  question = "Wall(1_1, 1_2)"
  expected = False
  run_KB_test(statements, question, expected)

  print("TEST 6: Adjacent means adjacent")
  statements = []

  statement = "Adjacent(1_1, 1_2)"
  statements.append(statement)

  question = "Adjacent(1_1, 1_2)"
  expected = True
  run_KB_test(statements, question, expected)

  print("TEST 7: Adjacent means adjacent - flipped")
  statements = []

  statement = "Adjacent(1_1, 1_2)"
  statements.append(statement)

  question = "Adjacent(1_2, 1_1)"
  expected = True
  #run_KB_test(statements, question, expected)

  print("TEST 8: Not breeze and adjacent means not pit")
  statements = []

  statement = "-Breeze(1_1)"
  statements.append(statement)

  statement = "Adjacent(1_1, 1_2)"
  statements.append(statement)

  question = "-Pit(1_2)"
  expected = True
  run_KB_test(statements, question, expected)

  print("TEST 9: Explored means Static Safe")

  statements = []
  statement = "Explored(1_1)"
  statements.append(statement)

  question = "StaticSafe(1_1)"

  expected = True
  run_KB_test(statements, question, expected)

  print("TEST 10: Static safe does not mean pit")

  statements = []

  statement = "StaticSafe(1_1)"
  statements.append(statement)
  question = "Pit(1_1)"
  expected = False

  run_KB_test(statements, question, expected)

  print("TEST 11: Not stench and adjacent means not wumpus")
  statements = []

  statement = "-Stench(1_1)"
  statements.append(statement)

  statement = "Adjacent(1_1, 1_2)"
  statements.append(statement)

  question = "-Wumpus(1_2)"
  expected = True
  run_KB_test(statements, question, expected)

  print("TEST 12: Not stench and not breeze and adjacent means static safe")
  statements = []

  statement = "-Stench(1_1)"
  statements.append(statement)

  statement = "-Breeze(1_1)"
  statements.append(statement)

  statement = "Adjacent(1_1, 1_2)"
  statements.append(statement)

  question = "-Wumpus(1_2)"
  expected = True
  run_KB_test(statements, question, expected)

  print("TEST 13: Explored means no wumpus")
  statements = []

  statement = "Explored(1_1)"
  statements.append(statement)

  question = "-Wumpus(1_1)"
  expected = True
  run_KB_test(statements, question, expected)

  print("TEST 14: Explored means no pit")
  statements = []

  statement = "Explored(1_1)"
  statements.append(statement)

  question = "-Pit(1_1)"
  expected = True
  run_KB_test(statements, question, expected)

  print("TEST 15: No pit and no wumpus means Static safe")
  statements = []

  statement = "-Pit(1_1)"
  statements.append(statement)

  statement = "-Wumpus(1_1)"
  statements.append(statement)

  question = "StaticSafe(1_1)"
  expected = True
  run_KB_test(statements, question, expected)

  print("TEST 16: Wumpus(1_1) does not mean Wumpus(2_2)")
  statements = []

  statement = "Wumpus(1_1)"
  statements.append(statement)

  question = "Wumpus(2_2)"
  expected = False
  run_KB_test(statements, question, expected)

def run_KB_test(statements, question, expected):
  agent.pyagent_initialize()
  start_time = round(time.clock(), 2)
  for statement in statements:
      agent.KB.tell(statement)
  actual = agent.KB.ask(question)
  end_time = round(time.clock(), 2)
  output_test_results(expected, actual, end_time - start_time)


def test_get_adjacent_cells():
  print()
  print("--------------- GET ADJACENT CELLS  ----------------")

  print("TEST 1:")
  cell = [1, 1]
  expected = [[1, 2], [2, 1]]
  run_get_adjacent_cells_test(cell, expected)

  print("TEST 2:")
  cell = [1, 2]
  expected = [[1, 1], [2, 2], [1, 3]]
  run_get_adjacent_cells_test(cell, expected)

  print("TEST 3:")
  cell = [3, 5]
  expected = [[2, 5], [4, 5], [3, 6], [3, 4]]
  run_get_adjacent_cells_test(cell, expected)

  print("TEST 4:")
  cell = [6, 2]
  expected = [[7, 2], [6, 1], [6, 3]]
  run_get_adjacent_cells_test(cell, expected)


def run_get_adjacent_cells_test(cell, expected):
  agent.pyagent_initialize()
  start_time = round(time.clock(), 2)
  agent.KB.tell("Wall(6_2, 5_2)")
  agent.KB.tell("Wall(5_2, 6_2)")
  actual = agent.get_adjacent_cells(cell)
  end_time = round(time.clock(), 2)
  output_test_results(expected, actual, end_time - start_time)


def test_find_subsequence():
  print()
  print("--------------- FIND SUBSEQUENCE  ----------------")

  print("TEST 1:")
  subseq = (1, 2, 3)
  seq = (0, 1, 2, 3, 4, 5)
  expected = 4
  run_find_subsequence_test(subseq, seq, expected)

  print("TEST 2:")
  subseq = ((1, 2), (3, 4))
  seq = ((0, 1), (1, 2), (3, 4), (5, 6))
  expected = 3
  run_find_subsequence_test(subseq, seq, expected)


  print("TEST 3:")
  subseq = [(0, 0), (0, 1), (0, 1), (0, 0), (1, 0)]
  seq = [
      (0, 0),
      (1, 0), (1, 0),
      (0, 0),
      (0, -1), (0, -1),
      (0, 0),
      (-1, 0), (-1, 0),
      (0, 0),
      (0, 1), (0, 1)
  ]
  expected = 2
  run_find_subsequence_test(subseq, seq, expected)

  print("TEST 4:")
  subseq = [(0, 0), (-1, 0), (-1, 0), (0, 0), (0, -1)]
  seq = [
      (0, 0),
      (1, 0), (1, 0),
      (0, 0),
      (0, -1), (0, -1),
      (0, 0),
      (-1, 0), (-1, 0),
      (0, 0),
      (0, 1), (0, 1)
  ]
  expected = 4
  run_find_subsequence_test(subseq, seq, expected)

  print("TEST 5:")
  subseq = [(0, 0), (1, 0), (1, 0), (0, 0), (0, 1)]
  seq = [
      (0, 0),
      (1, 0), (1, 0),
      (0, 0),
      (0, -1), (0, -1),
      (0, 0),
      (-1, 0), (-1, 0),
      (0, 0),
      (0, 1), (0, 1)
  ]
  expected = 10
  run_find_subsequence_test(subseq, seq, expected)



def run_find_subsequence_test(subseq, seq, expected):
  agent.pyagent_initialize()
  start_time = round(time.clock(), 2)
  actual = agent.find_subsequence(subseq, seq)
  end_time = round(time.clock(), 2)
  output_test_results(expected, actual, end_time - start_time)


def test_update_agent_direction():
  print()
  print("--------------- GET ADJACENT CELLS  ----------------")

  print("TEST 1:")
  curr_dir = "N"
  action = "left"
  expected = "W"
  run_update_agent_direction_test(curr_dir, action, expected)

  print("TEST 2:")
  curr_dir = "S"
  action = "left"
  expected = "E"
  run_update_agent_direction_test(curr_dir, action, expected)

  print("TEST 3:")
  curr_dir = "E"
  action = "left"
  expected = "N"
  run_update_agent_direction_test(curr_dir, action, expected)

  print("TEST 4:")
  curr_dir = "W"
  action = "left"
  expected = "S"
  run_update_agent_direction_test(curr_dir, action, expected)

  print("TEST 5:")
  curr_dir = "W"
  action = "right"
  expected = "N"
  run_update_agent_direction_test(curr_dir, action, expected)


def run_update_agent_direction_test(curr_dir, action, expected):
  agent.pyagent_initialize()
  start_time = round(time.clock(), 2)
  actual = agent.update_agent_direction(curr_dir, action)
  end_time = round(time.clock(), 2)
  output_test_results(expected, actual, end_time - start_time)


def test_string_to_coordinate():
  print()
  print("--------------- STRING TO COORDINATE  ----------------")

  print("TEST 1:")
  string = "0_0"
  expected = [0, 0]
  run_string_to_coordinate_test(string, expected)

  print("TEST 2:")
  string = "5_3"
  expected = [5, 3]
  run_string_to_coordinate_test(string, expected)

  print("TEST 3:")
  string = "2_3"
  expected = [2, 3]
  run_string_to_coordinate_test(string, expected)


def run_string_to_coordinate_test(string, expected):
  start_time = round(time.clock(), 2)
  actual = agent.string_to_coordinate(string)
  end_time = round(time.clock(), 2)
  output_test_results(expected, actual, end_time - start_time)


def test_coordinate_to_string():
  print()
  print("---------------  COORDINATE TO STRING  ----------------")

  print("TEST 1:")
  coordinate = (0, 0)
  expected = "0_0"
  run_coordinate_to_string_test(coordinate, expected)

  print("TEST 2:")
  coordinate = [2, 3]
  expected = "2_3"
  run_coordinate_to_string_test(coordinate, expected)

  print("TEST 2:")
  coordinate = [3, 3]
  expected = "3_3"
  run_coordinate_to_string_test(coordinate, expected)


def run_coordinate_to_string_test(coordinate, expected):
  start_time = round(time.clock(), 2)
  actual = agent.coordinate_to_string(coordinate)
  end_time = round(time.clock(), 2)
  output_test_results(expected, actual, end_time - start_time)


def output_test_results(expected, actual, execution_time, equality = True):
  if (equality):
    if (expected == actual):
      print("✔")
    else:
      print("✗")
      print("expected:", expected)
      print("actual:", actual)

  else:
    if (expected <= actual):
      print("✔")
    else:
      print("✗")
      print("expected:", expected)
      print("actual:", actual)

  if execution_time > 120:
    print("✗ TIMEOUT")

  print("time:", execution_time)
  print()


def main():
    # test_string_to_coordinate()
    # test_coordinate_to_string()
    # test_get_adjacent_cells()
    # test_update_agent_direction()
    # test_KB()
    test_find_subsequence()


if __name__ == "__main__":
  main()
