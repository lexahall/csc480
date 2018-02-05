# Name:        Lexa Hall
# Course:      CSC 480
# Instructor:  Daniel Kauffman
# Assignment:  Biogimmickry
# Term:        Winter 2018

import random
import math

# ----------------  INTERPRET -------------------------------------------------
def interpret(program, array):
  program = clean_program(list(program))
  bracket_map = build_bracket_map(program)

  # test it out starting in different places
  pc = 0
  mem_ptr = 0

  while pc < len(program):
    command = program[pc]

    if command == ">":
      mem_ptr += 1
      if mem_ptr == len(array):
         mem_ptr = len(array) - 1 # don't wrap around

    if command == "<":
      mem_ptr = 0 if mem_ptr <= 0 else mem_ptr - 1 # don't wrap around

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
def evaluate_fitness(program, target, interpreter):
  actual = [0] * len(target)

  interpreter(program, actual)

  print(actual)

  sum_diff = 0
  for i in range(len(actual)):
    sum_diff += pow(actual[i] - target[i], 2)

  return sum_diff


# ----------------  CROSSOVER --------------------------------------------------
def crossover(program_x, program_y):
  len_x = len(program_x)
  len_y = len(program_y)
  min_len = len_x if len_x < len_y else len_y

  index = int(random.random() * min_len)
  return (program_x[:index] + program_y[index:], program_y[:index] + program_x[index:])


def main():
  program = ">>+<->>++>+<+"
  array = [0] * 8

  # test interpret
  #print(array)
  #interpret(program, array)
  #print(array)

  # test evaluate fitness
  target = [0, 0, 0, 0, 0, 0, 0, 0]
  program = ">>+<->>++>+<+"
  #interpreter = interpret
  fitness = evaluate_fitness(program, target, interpret)
  print(fitness)

  target = [0, 0, 0, 0, 0, 0, 0, 0]
  program = ">><>>><"
  #interpreter = interpret
  fitness = evaluate_fitness(program, target, interpret)
  print(fitness)

  target = [0, 0, 0, 0, 0, 0, 0, 0]
  program = ">[>+]<++++++++>>[-------]-><"
  #interpreter = interpret
  fitness = evaluate_fitness(program, target, interpret)
  print(fitness)

  # test crossover
  program_x = '<<<<<<<<'
  program_y = '>>>>'
  prog_x, prog_y = crossover(program_x, program_y)
  print(prog_x, prog_y)

  # test create simple arrary
  target = [0, 0, 0, 0, 0, 0, 0]
  create_simple_program(target, interpret)

if __name__ == "__main__": main()
