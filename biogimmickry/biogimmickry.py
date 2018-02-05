# Name:        Lexa Hall
# Course:      CSC 480
# Instructor:  Daniel Kauffman
# Assignment:  Biogimmickry
# Term:        Winter 2018


# ----------------  INTERPRET -------------------------------------------------
def interpret(program, array):
  program = clean_program(list(program))
  bracket_map = build_bracket_map(program)

  pc = 0
  mem_ptr = 0

  while pc < len(program):
    command = program[pc]

    if command == ">":
      mem_ptr += 1
      if mem_ptr == len(array):
         mem_ptr = 0 # wrap back around to the front of the list
         #mem_ptr = len(array) - 1 #don't wrap around

    if command == "<":
      mem_ptr = 0 if mem_ptr <= 0 else mem_ptr - 1 # don't wrap around?

    if command == "+":
      array[mem_ptr] = array[mem_ptr] + 1

    if command == "-":
      array[mem_ptr] = array[mem_ptr] - 1

    if command == "[" and array[mem_ptr] == 0:
       pc = bracket_map[pc]
    if command == "]" and array[mem_ptr] != 0:
       pc = bracket_map[pc]

    pc += 1


def clean_program(program):
  return ''.join(filter(
    lambda x: x in ['.', ',', '[', ']', '<', '>', '+', '-'],
    program
  ))


def build_bracket_map(program):
  bracket_stack = []
  bracket_map = {}

  for pc, command in enumerate(program):
    if command == "[":
       bracket_stack.append(pc)
    if command == "]":
      start = bracket_stack.pop()
      bracket_map[start] = pc
      bracket_map[pc] = start
  return bracket_map


# ----------------  EVALUATE_FITNESS -------------------------------------------
def evaluate_fitness(target, program, interpreter):
  actual = [0] * len(target)

  interpreter(program, actual)

  sum_diff = 0
  for i in range(len(actual)):
    sum_diff += abs(actual[i] - target[i])

  return sum_diff


# ----------------  CROSSOVER --------------------------------------------------
def crossover(program_x, program_y):
  len_x = len(program_x)
  len_y = len(program_y)
  min_len = len_x if len_x < len_y else len_y

  index = int(random.random()*min_len)
  return (program_x[:index]+program_y[index:], program_y[:index]+program_x[index:])


def main():
  program = ">>+<->>++>+<+"
  array = [0] * 8

  # test interpret
  #print(array)
  #interpret(program, array)
  #print(array)

  # test evaluate fitness
  target = [1, 2, 3, 4, 5, 6, 7, 8]
  program = ">>+<->>++>+<+"
  print('target', target)
  #interpreter = interpret
  fitness = evaluate_fitness(target, program, interpret)
  print(fitness)

if __name__ == "__main__": main()
