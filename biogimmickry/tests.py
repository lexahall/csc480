import biogimmickry as bio
import time

def test_create_simple_program():
  print()
  print("---------------  CREATE SIMPLE PROGRAM  ----------------")

  print("TEST 1: simple 4")
  target = [0, 0, -2, 3]
  run_inversion_test(target)

  print("TEST 2: medium 4")
  target = [9, 21, -3, 6]
  run_inversion_test(target)

  print("TEST 3: hard 4")
  target = [1, 2, -32, 8]
  run_inversion_test(target)

  print("TEST 4: simple 5")
  target = [1, 0, -2, 0, 0]
  run_inversion_test(target)

  print("TEST 5: medium 5")
  target = [0, -2, 3, 0, 30]
  run_inversion_test(target)

  print("TEST 6: hard 5")
  target = [12, -2, -33, -9, 10]
  run_inversion_test(target)

  print("TEST 7: simple 6")
  target = [1, 0, -2, 3, 0, 0]
  run_inversion_test(target)

  print("TEST 8: medium 6")
  target = [0, 3, -2, 3, 0, 30]
  run_inversion_test(target)

  print("TEST 9: hard 6")
  target = [12, 34, -2, -19, -9, 10]
  run_inversion_test(target)

  print("TEST 10: easy 7")
  target = [0, 0, -2, 3, 0, 1, 0]
  run_inversion_test(target)

  print("TEST 11: medium 7")
  target = [-12, 20, -2, 3, 0, 0, 13]
  run_inversion_test(target)

  print("TEST 12: hard 7")
  target = [2, 0, -2, 3, 30, -23, 15]
  run_inversion_test(target)

  print("TEST 13: 8 -1's (equivalent of test 4)")
  target = [-1, -1, -1, -1, -1, -1, -1, -1]
  run_inversion_test(target)

  print("TEST 14: medium 8")
  target = [0, 0, -2, -9, -8, -9, -1, 1]
  run_inversion_test(target)

  print("TEST 15: 8 9's")
  target = [9, -9, -9, -9, 9, 9, 9, 9]
  run_inversion_test(target)


def run_inversion_test(target):
  interpreter = bio.interpret
  start_time = round(time.clock(), 2)
  program = bio.create_simple_program(target, interpreter)
  array = [0] * len(target)
  bio.interpret(program, array)
  end_time = round(time.clock(), 2)

  output_test_results(target, array, end_time - start_time)


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
  # DELIVERABLES:
  test_create_simple_program()

  # HELPER FUNCTIONS:

if __name__ == "__main__":
  main()
