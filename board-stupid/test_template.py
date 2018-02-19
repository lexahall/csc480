import boardstupid as game
import time

def test_search_tree():
  print()
  print("---------------  CREATE SIMPLE PROGRAM  ----------------")

  print("TEST 1:")
  board = [1, 2, 3, 4, 5, 6, 7, 8, 9]
  width = 3
  player = -1
  expected = 0
  run_search_tree_test(board, width, player, expected)

  print("TEST 2:")
  board = [1, 2, 3, 4, 5, 6, 7, 8, 9]
  width = 3
  player = 1
  expected = 0
  run_search_tree_test(board, width, player, expected)


  print("TEST 3:")
  board = ['X', 'O', 'X', 'O', 'X', 6, 'X', 'O', 9]
  width = 3
  player = -1
  expected = 0
  run_search_tree_test(board, width, player, expected)

  print("TEST 4:")
  board = ['X', 'O', 'X', 'O', 'X', 6, 'X', 'O', 9]
  width = 3
  player = 1
  expected = 0
  run_search_tree_test(board, width, player, expected)

  print("TEST 5:")
  board = ['X', 'O', 'X', 4, 5, 6, 7, 8, 9]
  width = 3
  player = -1
  expected = 10
  run_search_tree_test(board, width, player, expected)

  print("TEST 6:")
  board = ['X', 'O', 'X', 4, 5, 6, 7, 8, 9]
  width = 3
  player = 1
  expected = 10
  run_search_tree_test(board, width, player, expected)


def run_search_tree_test(board, width, player, expected):
  start_time = round(time.clock(), 2)
  actual = game.search_tree(board, width, player)
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
  test_search_tree()

if __name__ == "__main__":
  main()
