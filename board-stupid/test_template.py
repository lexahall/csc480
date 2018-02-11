import biogimmickry as bio
import time

def test_create_simple_program():
  print()
  print("---------------  CREATE SIMPLE PROGRAM  ----------------")

  print("TEST 1:")
  target = [0, 0, -2, 3]
  run_inversion_test(target)


def run_inversion_test(target):
  arrary = [0] * len(target)
  start_time = round(time.clock(), 2)
  program = bio.create_simple_program(target, interpreter)

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

  # HELPER FUNCTIONS:

if __name__ == "__main__":
  main()
