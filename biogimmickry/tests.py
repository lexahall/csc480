import biogimmickry as bio

def main():
  program = ">>+<->>++>+<+"
  array = [0] * 8
  interpreter = bio.interpret

  # test interpret
  #print(array)
  #bio.interpret(program, array)
  #print(array)

  # test evaluate fitness
  target = [0, 0, 0, 0, 0, 0, 0, 0]
  program = ">>+<->>++>+<+"
  fitness = bio.evaluate_fitness(program, target, interpreter)
  print(fitness)

  target = [0, 0, 0, 0, 0, 0, 0, 0]
  program = ">><>>><"
  fitness = bio.evaluate_fitness(program, target, interpreter)
  print(fitness)

  target = [0, 0, 0, 0, 0, 0, 0, 0]
  program = ">[>+]<++++++++>>[-------]-><"
  fitness = bio.evaluate_fitness(program, target, interpreter)
  print(fitness)

  # test crossover
  program_x = '<<<<<<<<'
  program_y = '>>>>'
  prog_x, prog_y = bio.crossover(program_x, program_y)
  print(prog_x, prog_y)

  # test create simple arrary
  target = [0, 0, 8, 1]
  program = bio.create_simple_program(target, interpreter)
  arrary = [0, 0, 0, 0]
  bio.interpret(program, arrary)
  print(arrary)

  # test calculate_min_prog_length
  min_len = bio.calculate_min_prog_length([1, 0, -2, 5, 0, 2])
  print(min_len)

if __name__ == "__main__": main()
