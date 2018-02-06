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

  # TODO: write tests with pc starting in different places
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

  sum_diff = 0
  for i in range(len(actual)):
    sum_diff += abs(actual[i] - target[i])

  return sum_diff


# ----------------  CROSSOVER --------------------------------------------------
def crossover(program_x, program_y):
  len_x = len(program_x)
  len_y = len(program_y)
  min_len = min(len_x, len_y)

  cross_index = random.randint(1, min_len)
  prog_x = program_x[:cross_index] + program_y[cross_index:]
  prog_y = program_y[:cross_index] + program_x[cross_index:]

  return (prog_x, prog_y)


# --------------- MUTATION -----------------------------------------------------
def conditionally_mutate(program):
  # daniel: somewhere between .2 and .3
  chance_of_mutation = 0.1 # tweak

  if random.random() < chance_of_mutation:
    program = mutate(program)

  return program


def mutate(program):
  alphabet = ['<', '>', '+', '-']
  mutation_percentage = .2

  alphabet_len = len(alphabet)
  program_len = len(program)
  mutation_len = int(program_len * mutation_percentage)
  minimum_len = 1
  mutation_len = mutation_len if mutation_len > 0 else minimum_len

  mod_index = random.randint(0, program_len - mutation_len)

  mutated_program = ''

  for i in range(program_len):
    if mod_index <= i <= mod_index + mutation_len:
      mutated_program += alphabet[random.randint(0, alphabet_len - 1)]
    else:
      mutated_program += program[i]

  return mutated_program


# TODO: fill in stubs and split up mutate function

#def remove_command(program):


#def add_command(program):


#def modify_command():

# --------------- SELECTION ----------------------------------------------------
def select(population, population_size):
  top_percentile_divisor = 5 # tweak
  top_percentile_len = population_size // top_percentile_divisor

  top_percentile = population[:top_percentile_len]

  max_fitness = population[top_percentile_len - 1][1]

  top_percentile, fitness_sum = adjust_fitness(top_percentile, max_fitness)

  program_x = select_individual(top_percentile, top_percentile_len, fitness_sum)
  program_y = select_individual(top_percentile, top_percentile_len, fitness_sum)

  return program_x, program_y


def select_individual(population, population_size, fitness_sum):
  select_threshold = random.random() * fitness_sum
  selection_sum = 0
  i = 0

  while selection_sum < select_threshold:
    selection_sum += population[i][1]
    i += 1

  return population[i - 1][0]


def adjust_fitness(population, max_fitness):
  population_len = len(population)
  adjusted_population = []

  fitness_sum = 0
  for i in range(population_len):
    adjusted_fitness = abs(population[i][1] - max_fitness)
    fitness_sum += adjusted_fitness
    adjusted_entry = (population[i][0], adjusted_fitness)
    adjusted_population.append(adjusted_entry)

  return adjusted_population, fitness_sum


# --------------- CREATE SIMPLE PROGRAM ----------------------------------------
def create_simple_program(target, interpreter):
  max_iterations = 1000 # tweak
  population_size = 100 # tweak
  population = []

  # create initial population
  min_prog_len = calculate_min_prog_length(target)
  max_prog_len = min_prog_len * 3 + 1 # tweak

  fitness_sum = 0
  for i in range(population_size):
    program = generate_random_program(min_prog_len, max_prog_len)
    fitness = evaluate_fitness(program, target, interpreter)
    entry = (program, fitness)
    population.append(entry)

  population.sort(key=lambda program: program[1])
  top_fitness_score = population[0][1]

  # evolve population until target is reached
  num_iterations = 0
  while (top_fitness_score != 0 and num_iterations < max_iterations):
    next_gen = []

    while (len(next_gen) < population_size):
      # select two from top percentile (x, y)
      program_x, program_y = select(population, population_size)

      program_x, program_y = crossover(program_x, program_y)
      program_x = conditionally_mutate(program_x)
      program_y = conditionally_mutate(program_y)
      # evaluate fitness for x and y
      fitness_x = evaluate_fitness(program_x, target, interpreter)
      fitness_y = evaluate_fitness(program_y, target, interpreter)

      # add x and y to next gen
      entry_x = program_x, fitness_x
      entry_y = program_y, fitness_y
      next_gen.append(entry_x)
      next_gen.append(entry_y)

    # sort population
    next_gen.sort(key=lambda program: program[1])
    top_fitness_score = population[0][1]
    num_iterations += 1

  program = population[0][0]

  return program

def calculate_min_prog_length(target):
  prog_len = 0
  target_len = len(target)

  if target[target_len - 1] != 0:
    prog_len += target_len - 1

  for i in range(target_len):
      prog_len += abs(target[i])

  return prog_len


def generate_random_program(min_prog_len, max_prog_len):
  alphabet = ['<', '>', '+', '-']
  alphabet_len = len(alphabet)
  prog_len = random.randint(min_prog_len, max_prog_len - 1)
  program = ''

  for i in range(prog_len):
    rand_index = random.randint(0, alphabet_len - 1)
    program += alphabet[rand_index]

  return program
