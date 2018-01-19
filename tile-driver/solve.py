# Name:        Lexa Hall
# Course:      CSC 480
# Instructor:  Daniel Kauffman
# Assignment:  Tile Driver
# Term:        Winter 2018

import queue
import copy

class Tile(object):
   def __init__(self, value, row, col):
      self.value = value
      self.row = row
      self.col = col

class Puzzle(object):
   def __init__(self, board):
      self.moves = ['h', 'j', 'k', 'l']
      self.width = len(board)
      self.path_cost = 0
      self.path = ''
      self.manhattan_dist = 0
      self.combined_cost = self.path_cost + self.manhattan_dist
      self.board = board

   def __lt__(self, other):
      return self.combined_cost < other.combined_cost

   def set_tuple_board(self):
      tuple_board = []
      for i in range(self.width):
         for j in range(self.width):
            tuple_board.append(self.board[i][j])

      self.tuple_board = tuple(tuple_board)

   def set_combined_cost(self):
      self.combined_cost = self.path_cost + self.manhattan_dist

   def get_manhattan_dist(self):
      total_dist = 0
      for i in range(self.width):
         for j in range(self.width):
            total_dist += self.get_tile_manhattan_dist(self.board[i][j], i, j)
      return total_dist

   def get_manhattan_delta(self, blank, target):
      old_dist = self.get_tile_manhattan_dist(target.value, target.row, target.col)
      new_dist = self.get_tile_manhattan_dist(target.value, blank.row, blank.col)
      return new_dist - old_dist

   def get_tile_manhattan_dist(self, value, row, col):
      # don't count the blank space
      if value == 0:
         return 0;

      goal_col = value % self.width
      goal_row = int(value / self.width)
      return abs(col - goal_col) + abs(row - goal_row)

   def find_blank(self):
      blank_tile = None
      for i in range(self.width):
         for j in range(self.width):
            if self.board[i][j] == 0:
               blank_tile = Tile(self.board[i][j], i, j)
      return blank_tile

   def get_target(self, blank, move):
      target = Tile(-1, blank.row, blank.col)
      if (move == 'h'):
         target.col += 1
      elif (move == 'j'):
         target.row -= 1
      elif (move == 'k'):
         target.row += 1
      elif (move == 'l'):
         target.col -= 1

      if self.in_bounds(target):
         target.value = self.board[target.row][target.col]
         return target

   def in_bounds(self, target):
      if (0 <= target.row < self.width) and (0 <= target.col < self.width):
         return True
      return False

   def swap_tiles(self, target, blank):
      self.board[blank.row][blank.col] = target.value
      self.board[target.row][target.col] = blank.value

def solve_puzzle(tiles):
   # set up inital puzzle state
   width = int(len(tiles) ** (0.5))

   init_puzzle = create_init_puzzle(tiles, width)

   # initialize frontier and explored
   frontier_q = queue.PriorityQueue()
   frontier_set = set()
   explored = set()

   # add inital puzzle state to frontier
   frontier_q.put(init_puzzle)
   frontier_set.add(init_puzzle.tuple_board)

   # while there are still states in the frontier
   while not frontier_q.empty():
      # pop node with the lowest f(n) - node q
      parent = frontier_q.get()

      # generate all of q's successors and set their parent to q
      fringe_states = get_fringe_states(parent)

      # for each successor:
      for state in fringe_states:
         # check that the current state has not already been explored
         if ((not state.tuple_board in explored)
            and (not state.tuple_board in frontier_set)):
            # TEST PRINT
            print()
            print("FRINGE STATE:")
            test_output(state)

            # if the successor is the goal, stop
            if state.manhattan_dist == 0:
               return(state.path)
               #calculate_soln()
               #exit

            frontier_q.put(state)
            frontier_set.add(state.tuple_board)

      # push parent on the closed list
      explored.add(parent.tuple_board)

def test_output(puzzle):
   # test: print out all tile values in the puzzle
   for i in range(puzzle.width):
      print('[', end='')
      for j in range(puzzle.width):
         print(puzzle.board[i][j], end=' ')
         #print(puzzle.board[i][j].value, " (", puzzle.board[i][j].row, ", ", puzzle.board[i][j].col, ")", sep="", end=' ')
      print(']')
   # test: print out the manhattan_dist for init puzzle
   print("man dist:", puzzle.manhattan_dist)
   print("path cost:", puzzle.path_cost)
   print("path:", puzzle.path)

def print_board(puzzle):
   # test: print out all tile values in the puzzle
   for i in range(puzzle.width):
      print('[', end='')
      for j in range(puzzle.width):
         print(puzzle.board[i][j], end=' ')
         #print(puzzle.board[i][j].value, " (", puzzle.board[i][j].row, ", ", puzzle.board[i][j].col, ")", sep="", end=' ')
      print(']')

def create_init_puzzle(tiles, width):
   board = build_board(tiles, width)
   init_puzzle = Puzzle(board)

   init_puzzle.manhattan_dist = init_puzzle.get_manhattan_dist()
   init_puzzle.set_combined_cost()
   init_puzzle.set_tuple_board()

   # test initial board
   print("INITIAL BOARD:")
   test_output(init_puzzle)
   print()
   return init_puzzle

def build_board(tiles, width):
   board = []
   for i in range(width):
      chunk_start = i * width
      chunk_end = i * width + width

      board.append(
         [value for value in tiles[chunk_start : chunk_end]]
      )

   return board

def get_fringe_states(puzzle):
   #print()
   #print("In fringe_states:")
   #print("board passed in:")
   #print_board(puzzle)
   blank = puzzle.find_blank()
   fringe_states = []

   for move in puzzle.moves:
      target = puzzle.get_target(blank, move)
      if target:
         print("move:", move)
         #print("blank:", blank.row, blank.col, "val:", blank.value)
         #print("target:", target.row, target.col, "val:", target.value)
         #print()
         next_puzzle = create_next_puzzle(puzzle, blank, target, move)
         fringe_states.append(next_puzzle)

   return fringe_states

def create_next_puzzle(puzzle, blank, target, move):
   next_board = copy.deepcopy(puzzle.board)
   next_puzzle = Puzzle(next_board)
   manhattan_delta = next_puzzle.get_manhattan_delta(blank, target)
   print("delta:", manhattan_delta)
   next_puzzle.swap_tiles(blank, target)
   next_puzzle.path = puzzle.path + move
   next_puzzle.path_cost = puzzle.path_cost + 1
   next_puzzle.manhattan_dist = puzzle.manhattan_dist + manhattan_delta
   next_puzzle.set_combined_cost()
   next_puzzle.set_tuple_board()

   return next_puzzle

def main():
   # test tile lists
   # answer: 6
   tiles = [3, 2, 1, 0]

   # answer: 20
   # tiles = [7, 1, 8, 6, 3, 4, 0, 5, 2]

   # answer: 28
   # tiles = [8, 5, 4, 7, 0, 6, 2, 1, 3]

   # answer: 31
   # tiles = [8, 0, 6, 5, 4, 7, 2, 3, 1]

   # answer: 36
   # tiles = [5, 1, 3, 7, 9, 6, 4, 11, 13, 8, 14, 2, 12, 10, 15, 0]

   # answer: 40
   # tiles = [2, 12, 3, 4, 9, 1, 0, 11, 7, 6, 5, 10, 17, 13, 14, 15, 16, 8, 24, 18, 20, 21, 19, 22, 23]
   soln = solve_puzzle(tiles)
   print("cost:", len(soln))
   print("soln:", soln)

if __name__ == "__main__":
   main()
