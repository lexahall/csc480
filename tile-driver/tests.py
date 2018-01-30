import tiledriver2 as driver
import time

def test_solve_puzzle():
   # test tile lists
   print("------------------- SOLVE_PUZZLE ----------------")
   # answer: 6
   print("TEST 1:")
   tiles = [3, 2, 1, 0]
   start_time = round(time.clock(), 2)
   soln = driver.solve_puzzle(tiles)
   end_time = round(time.clock(), 2)
   expected_cost = 6
   if (expected_cost <= len(soln)):
      print("✔")
   else:
      print("✗")
      print("expected cost:", expected_cost)
      print("actual cost:", len(soln))
      print("soln:", soln)
   print("execution time:", end_time - start_time)
   print()

   # answer: 20
   print("TEST 2:")
   tiles = [7, 1, 8, 6, 3, 4, 0, 5, 2]
   start_time = round(time.clock(), 2)
   soln = driver.solve_puzzle(tiles)
   end_time = round(time.clock(), 2)
   expected_cost = 20
   if (expected_cost <= len(soln)):
      print("✔")
   else:
      print("✗")
      print("expected cost:", expected_cost)
      print("actual cost:", len(soln))
      print("soln:", soln)
   print("execution time:", end_time - start_time)
   print()

   # answer: 28
   print("TEST 3:")
   tiles = [8, 5, 4, 7, 0, 6, 2, 1, 3]
   start_time = round(time.clock(), 2)
   soln = driver.solve_puzzle(tiles)
   end_time = round(time.clock(), 2)
   expected_cost = 28
   if (expected_cost <= len(soln)):
      print("✔")
   else:
      print("✗")
      print("expected cost:", expected_cost)
      print("actual cost:", len(soln))
      print("soln:", soln)
   print("execution time:", end_time - start_time)
   print()

   # answer: 31
   print("TEST 4:")
   tiles = [8, 0, 6, 5, 4, 7, 2, 3, 1]
   start_time = round(time.clock(), 2)
   soln = driver.solve_puzzle(tiles)
   end_time = round(time.clock(), 2)
   expected_cost = 31
   if (expected_cost <= len(soln)):
      print("✔")
   else:
      print("✗")
      print("expected cost:", expected_cost)
      print("actual cost:", len(soln))
      print("soln:", soln)
   print("execution time:", end_time - start_time)
   print()

   # answer: 36
   # print("TEST 5:")
   # tiles = [5, 1, 3, 7, 9, 6, 4, 11, 13, 8, 14, 2, 12, 10, 15, 0]
   # start_time = round(time.clock(), 2)
   # soln = driver.solve_puzzle(tiles)
   # end_time = round(time.clock(), 2)
   # expected_cost = 36
   # if (expected_cost <= len(soln)):
   #    print("✔")
   # else:
   #    print("✗")
   #    print("expected cost:", expected_cost)
   #    print("actual cost:", len(soln))
   #    print("soln:", soln)
   # print("execution time:", end_time - start_time)
   # print()

   # answer: 40
   # print("TEST 6:")
   # tiles = [2, 12, 3, 4, 9, 1, 0, 11, 7, 6, 5, 10, 17, 13, 14, 15, 16, 8, 24, 18, 20, 21, 19, 22, 23]
   # start_time = round(time.clock(), 2)
   # soln = driver.solve_puzzle(tiles)
   # end_time = round(time.clock(), 2)
   # expected_cost = 40
   # if (expected_cost <= len(soln)):
   #    print("✔")
   # else:
   #    print("✗")
   #    print("expected cost:", expected_cost)
   #    print("actual cost:", len(soln))
   #    print("soln:", soln)
   # print("execution time:", end_time - start_time)
   # print()


def test_conflict_tiles():
   print()
   print("------------------- CONFLICT TILES ----------------")
   print("TEST 1:")
   minimum_cost = 100
   width = 2
   start_time = round(time.clock(), 2)
   tiles = driver.conflict_tiles(width)
   end_time = round(time.clock(), 2)
   soln = driver.solve_puzzle(tiles)
   if (minimum_cost <= len(soln)):
      print("✔")
   else:
      print("✗")
      print("width:", width)
      print("tiles:", tiles)
      print("cost:", len(soln))
   print("execution time:", end_time - start_time)
   print()

   print("TEST 2:")
   minimum_cost = 28
   width = 3
   start_time = round(time.clock(), 2)
   tiles = driver.conflict_tiles(width)
   end_time = round(time.clock(), 2)
   soln = driver.solve_puzzle(tiles)
   if (minimum_cost <= len(soln)):
      print("✔")
   else:
      print("✗")
      print("width:", width)
      print("tiles:", tiles)
      print("cost:", len(soln))
   print("execution time:", end_time - start_time)
   print()

   print("TEST 3:")
   minimum_cost = 100
   width = 4
   start_time = round(time.clock(), 2)
   tiles = driver.conflict_tiles(width)
   end_time = round(time.clock(), 2)
   soln = driver.solve_puzzle(tiles)
   if (minimum_cost <= len(soln)):
      print("✔")
   else:
      print("✗")
      print("width:", width)
      print("tiles:", tiles)
      print("cost:", len(soln))
   print("execution time:", end_time - start_time)
   print()


def test_find_num_conflicts():
   print()
   print("------------------- NUM CONFLICTS ----------------")
   print("TEST 1:")
   width = 3
   expected_num_conflicts = 2
   tiles = [0, 7, 2, 3, 4, 5, 6, 1, 8]
   start_time = round(time.clock(), 2)
   num_conflicts = driver.find_num_conflicts(tiles, width)
   end_time = round(time.clock(), 2)
   if (expected_num_conflicts == num_conflicts):
      print("✔")
   else:
      print("✗")
      print("expected num conflicts:", expected_num_conflicts)
      print("actual num conflicts:", num_conflicts)

   print("execution time:", end_time - start_time)
   print()

   print("TEST 2:")
   width = 3
   expected_num_conflicts = 5
   tiles = [0, 7, 2, 5, 4, 3, 8, 1, 6]
   start_time = round(time.clock(), 2)
   num_conflicts = driver.find_num_conflicts(tiles, width)
   end_time = round(time.clock(), 2)
   if (expected_num_conflicts == num_conflicts):
      print("✔")
   else:
      print("✗")
      print("expected num conflicts:", expected_num_conflicts)
      print("actual num conflicts:", num_conflicts)

   print("execution time:", end_time - start_time)
   print()


def test_shuffle_tiles():
   print()
   print("------------------- SHUFFLE TILES ----------------")
   print("TEST 1:")
   minimum_cost = 100
   width = 2
   start_time = round(time.clock(), 2)
   tiles = driver.shuffle_tiles(width)
   end_time = round(time.clock(), 2)
   soln = driver.solve_puzzle(tiles)
   if (minimum_cost <= len(soln)):
      print("✔")
   else:
      print("✗")
      print("width:", width)
      print("tiles:", tiles)
      print("cost:", len(soln))
   print("execution time:", end_time - start_time)
   print()

   print("TEST 2:")
   minimum_cost = 28
   width = 3
   start_time = round(time.clock(), 2)
   tiles = driver.shuffle_tiles(width)
   end_time = round(time.clock(), 2)
   soln = driver.solve_puzzle(tiles)
   if (minimum_cost <= len(soln)):
      print("✔")
   else:
      print("✗")
      print("width:", width)
      print("tiles:", tiles)
      print("cost:", len(soln))
   print("execution time:", end_time - start_time)
   print()

   print("TEST 3:")
   minimum_cost = 100
   width = 4
   start_time = round(time.clock(), 2)
   tiles = driver.shuffle_tiles(width)
   end_time = round(time.clock(), 2)
   soln = driver.solve_puzzle(tiles)
   if (minimum_cost <= len(soln)):
      print("✔")
   else:
      print("✗")
      print("width:", width)
      print("tiles:", tiles)
      print("cost:", len(soln))
   print("execution time:", end_time - start_time)
   print()


def test_is_solvable():
   print()
   print("-------------------  IS SOLVABLE  ----------------")
   print("TEST 1:")
   tiles = [0, 1, 2, 3, 4, 5, 6, 7, 8]
   start_time = round(time.clock(), 2)
   solvable = driver.is_solvable(tiles)
   end_time = round(time.clock(), 2)
   expected = True
   if (expected == solvable):
      print("✔")
   else:
      print("✗")
      print("expected:", expected)
      print("actual:", solvable)
   print("execution time:", end_time - start_time)
   print()

   print("TEST 2:")
   tiles = [1, 0, 3, 2, 4, 5, 6, 7, 8]
   start_time = round(time.clock(), 2)
   solvable = driver.is_solvable(tiles)
   end_time = round(time.clock(), 2)
   expected = False
   if (expected == solvable):
      print("✔")
   else:
      print("✗")
      print("expected:", expected)
      print("actual:", solvable)
   print("execution time:", end_time - start_time)
   print()

   print("TEST 3:")
   tiles = [7, 0, 2, 8, 5, 3, 6, 4, 1]
   start_time = round(time.clock(), 2)
   solvable = driver.is_solvable(tiles)
   end_time = round(time.clock(), 2)
   expected = False
   if (expected == solvable):
      print("✔")
   else:
      print("✗")
      print("expected:", expected)
      print("actual:", solvable)
   print("execution time:", end_time - start_time)
   print()

   print("TEST 4:")
   tiles = [0, 7, 2, 3, 4, 5, 6, 1, 8]
   start_time = round(time.clock(), 2)
   solvable = driver.is_solvable(tiles)
   end_time = round(time.clock(), 2)
   expected = True
   if (expected == solvable):
      print("✔")
   else:
      print("✗")
      print("expected:", expected)
      print("actual:", solvable)
   print("execution time:", end_time - start_time)
   print()

   print("TEST 5:")
   tiles = [1, 2, 3, 4, 5, 6, 8, 7]
   start_time = round(time.clock(), 2)
   solvable = driver.is_solvable(tiles)
   end_time = round(time.clock(), 2)
   expected = False
   if (expected == solvable):
      print("✔")
   else:
      print("✗")
      print("expected:", expected)
      print("actual:", solvable)
   print("execution time:", end_time - start_time)
   print()

def test_count_inversions():
   print()
   print("-------------------  COUNT INVERSIONS  ----------------")
   print("TEST 1:")
   tiles = [0, 1, 2, 3, 4, 5, 6, 7, 8]
   start_time = round(time.clock(), 2)
   num_inversions = driver.count_inversions(tiles)
   end_time = round(time.clock(), 2)
   expected = 0
   if (expected == num_inversions):
      print("✔")
   else:
      print("✗")
      print("expected:", expected)
      print("actual:", num_inversions)
   print("execution time:", end_time - start_time)
   print()

   print("TEST 2:")
   tiles = [1, 0, 3, 2, 4, 5, 6, 7, 8]
   start_time = round(time.clock(), 2)
   num_inversions = driver.count_inversions(tiles)
   end_time = round(time.clock(), 2)
   expected = 1
   if (expected == num_inversions):
      print("✔")
   else:
      print("✗")
      print("expected:", expected)
      print("actual:", num_inversions)
   print("execution time:", end_time - start_time)
   print()

   print("TEST 3:")
   tiles = [7, 0, 2, 8, 5, 3, 6, 4, 1]
   start_time = round(time.clock(), 2)
   num_inversions = driver.count_inversions(tiles)
   end_time = round(time.clock(), 2)
   expected = 19
   if (expected == num_inversions):
      print("✔")
   else:
      print("✗")
      print("expected:", expected)
      print("actual:", num_inversions)
   print("execution time:", end_time - start_time)
   print()

   print("TEST 4:")
   tiles = [0, 7, 2, 3, 4, 5, 6, 1, 8]
   start_time = round(time.clock(), 2)
   num_inversions = driver.count_inversions(tiles)
   end_time = round(time.clock(), 2)
   expected = 7
   if (expected == num_inversions):
      print("✔")
   else:
      print("✗")
      print("expected:", expected)
      print("actual:", num_inversions)
   print("execution time:", end_time - start_time)
   print()

   print("TEST 5:")
   tiles = [0, 1, 2, 3, 4, 5, 6, 8, 7]
   start_time = round(time.clock(), 2)
   num_inversions = driver.count_inversions(tiles)
   end_time = round(time.clock(), 2)
   expected = 1
   if (expected == num_inversions):
      print("✔")
   else:
      print("✗")
      print("expected:", expected)
      print("actual:", num_inversions)
   print("execution time:", end_time - start_time)
   print()

def main():
   # DELIVERABLES:
   # test_solve_puzzle()
   test_conflict_tiles()
   test_shuffle_tiles()
   test_is_solvable()

   # HELPER FUNCTIONS:
   test_find_num_conflicts()
   test_count_inversions()

if __name__ == "__main__":
   main()
