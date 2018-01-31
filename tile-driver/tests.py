import tiledriver as driver
import time

def test_solve_puzzle():
   # test tile lists
   print("------------------- SOLVE_PUZZLE ----------------")
   # answer: 6
   print("TEST 1:")
   tiles = [3, 2, 1, 0]
   expected_cost = 6
   run_solve_puzzle(expected_cost, tiles)

   # answer: 20
   print("TEST 2:")
   tiles = [7, 1, 8, 6, 3, 4, 0, 5, 2]
   expected_cost = 20
   run_solve_puzzle(expected_cost, tiles)

   # answer: 28
   print("TEST 3:")
   tiles = [8, 5, 4, 7, 0, 6, 2, 1, 3]
   expected_cost = 28
   run_solve_puzzle(expected_cost, tiles)

   # answer: 31
   print("TEST 4:")
   tiles = [8, 0, 6, 5, 4, 7, 2, 3, 1]
   expected_cost = 31
   run_solve_puzzle(expected_cost, tiles)

   # answer: 36
   # print("TEST 5:")
   # tiles = [5, 1, 3, 7, 9, 6, 4, 11, 13, 8, 14, 2, 12, 10, 15, 0]
   # expected_cost = 36
   # run_solve_puzzle(expected_cost, tiles)

   # answer: 40
   # print("TEST 6:")
   # tiles = [2, 12, 3, 4, 9, 1, 0, 11, 7, 6, 5, 10, 17, 13, 14, 15, 16, 8, 24, 18, 20, 21, 19, 22, 23]
   # expected_cost = 40
   # run_solve_puzzle(expected_cost, tiles)


def run_solve_puzzle(expected, tiles):
   start_time = round(time.clock(), 2)
   soln = driver.solve_puzzle(tiles)
   end_time = round(time.clock(), 2)
   output_test_results(expected, len(soln), end_time - start_time, False)


def test_conflict_tiles():
   print()
   print("------------------- CONFLICT TILES ----------------")
   print("TEST 1:")
   minimum_cost = 100
   width = 2
   run_conflict_tiles(minimum_cost, width)

   print("TEST 2:")
   minimum_cost = 28
   width = 3
   run_conflict_tiles(minimum_cost, width)

   print("TEST 3:")
   minimum_cost = 100
   width = 4
   run_conflict_tiles(minimum_cost, width)


def run_conflict_tiles(expected, width):
   start_time = round(time.clock(), 2)
   tiles = driver.conflict_tiles(width)
   end_time = round(time.clock(), 2)
   soln = driver.solve_puzzle(tiles)
   output_test_results(expected, len(soln), end_time - start_time, False)


def test_find_num_conflicts():
   print()
   print("------------------- NUM CONFLICTS ----------------")
   print("TEST 1:")
   width = 3
   expected_num_conflicts = 2
   tiles = [0, 7, 2, 3, 4, 5, 6, 1, 8]
   run_num_conflicts(expected_num_conflicts, tiles, width)

   print("TEST 2:")
   width = 3
   expected_num_conflicts = 5
   tiles = [0, 7, 2, 5, 4, 3, 8, 1, 6]
   run_num_conflicts(expected_num_conflicts, tiles, width)


def run_num_conflicts(expected, tiles, width):
   start_time = round(time.clock(), 2)
   num_conflicts = driver.find_num_conflicts(tiles, width)
   end_time = round(time.clock(), 2)
   output_test_results(expected, num_conflicts, end_time - start_time)


def test_shuffle_tiles():
   print()
   print("------------------- SHUFFLE TILES ----------------")
   print("TEST 1:")
   minimum_cost = 100
   width = 2
   run_shuffle_tiles(minimum_cost, width)

   print("TEST 2:")
   minimum_cost = 28
   width = 3
   run_shuffle_tiles(minimum_cost, width)

   print("TEST 3:")
   minimum_cost = 100
   width = 4
   run_shuffle_tiles(minimum_cost, width)


def run_shuffle_tiles(expected, width):
   start_time = round(time.clock(), 2)
   tiles = driver.shuffle_tiles(width)
   end_time = round(time.clock(), 2)
   soln = driver.solve_puzzle(tiles)
   output_test_results(expected, len(soln), end_time - start_time, False)


def test_is_solvable():
   print()
   print("-------------------  IS SOLVABLE  ----------------")
   print("TEST 1:")
   tiles = [0, 1, 2, 3, 4, 5, 6, 7, 8]
   expected = True
   run_solvable_test(expected, tiles)

   print("TEST 2:")
   tiles = [1, 0, 3, 2, 4, 5, 6, 7, 8]
   expected = False
   run_solvable_test(expected, tiles)

   print("TEST 3:")
   tiles = [7, 0, 2, 8, 5, 3, 6, 4, 1]
   expected = False
   run_solvable_test(expected, tiles)

   print("TEST 4:")
   tiles = [0, 7, 2, 3, 4, 5, 6, 1, 8]
   expected = False
   run_solvable_test(expected, tiles)

   print("TEST 5:")
   tiles = [0, 1, 2, 3, 4, 5, 6, 8, 7]
   expected = False
   run_solvable_test(expected, tiles)


def run_solvable_test(expected, tiles):
   start_time = round(time.clock(), 2)
   solvable = driver.is_solvable(tiles)
   end_time = round(time.clock(), 2)
   output_test_results(expected, solvable, end_time - start_time)


def test_count_inversions():
   print()
   print("-------------------  COUNT INVERSIONS  ----------------")

   print("TEST 1:")
   expected = 0
   tiles = [0, 1, 2, 3, 4, 5, 6, 7, 8]
   run_inversion_test(expected, tiles)

   print("TEST 2:")
   tiles = [1, 0, 3, 2, 4, 5, 6, 7, 8]
   expected = 1
   run_inversion_test(expected, tiles)

   print("TEST 3:")
   tiles = [7, 0, 2, 8, 5, 3, 6, 4, 1]
   expected = 19
   run_inversion_test(expected, tiles)

   print("TEST 4:")
   tiles = [0, 7, 2, 3, 4, 5, 6, 1, 8]
   expected = 7
   run_inversion_test(expected, tiles)

   print("TEST 5:")
   tiles = [0, 1, 2, 3, 4, 5, 6, 8, 7]
   expected = 1
   run_inversion_test(expected, tiles)


def run_inversion_test(expected, tiles):
   start_time = round(time.clock(), 2)
   num_inversions = driver.count_inversions(tiles)
   end_time = round(time.clock(), 2)
   output_test_results(expected, num_inversions, end_time - start_time)


def output_test_results(expected, actual, execution_time, equality = True):
   if (equality):
      if (expected == actual):
         print("✔")
      else:
         print("✗")
         print("expected:", expected)
         print("actual:", actual)
      print("execution time:", execution_time)

   else:
      if (expected <= actual):
         print("✔")
      else:
         print("✗")
         print("expected:", expected)
         print("actual:", actual)
      print("execution time:", execution_time)

   print()


def main():
   # DELIVERABLES:
   test_solve_puzzle()
   test_conflict_tiles()
   test_shuffle_tiles()
   test_is_solvable()

   # HELPER FUNCTIONS:
   test_find_num_conflicts()
   test_count_inversions()

if __name__ == "__main__":
   main()
