# Name:        Lexa Hall
# Course:      CSC 480
# Instructor:  Daniel Kauffman
# Assignment:  Tile Driver
# Term:        Winter 2018

import queue
import copy
import time

class Tile(object):
   def __init__(self, value, row, col):
      self.value = value
      self.row = row
      self.col = col


class Puzzle(object):
   def __init__(self, board):
      self.moves = ['h', 'j', 'k', 'l']
      sqr_root_exp = 0.5
      self.width = int(len(board) ** (sqr_root_exp))
      self.path_cost = 0
      self.path = ''
      self.manhattan_dist = 0
      self.combined_cost = self.path_cost + self.manhattan_dist
      self.board = board
      self.blank_tile = Tile(0, 0, 0)
      self.board_len = len(board)

   def __lt__(self, other):
      return self.combined_cost < other.combined_cost

   def set_tuple_board(self):
      self.tuple_board = tuple(self.board)

   def set_combined_cost(self):
      self.combined_cost = self.path_cost + self.manhattan_dist

   def get_manhattan_dist(self):
      total_dist = 0
      for i in range(self.board_len):
         row = int(i / self.width)
         col = i % self.width
         total_dist += self.get_tile_manhattan_dist(self.board[i], row, col)
      return total_dist

   def get_manhattan_delta(self, target):
      blank = self.blank_tile
      old_dist = self.get_tile_manhattan_dist(target.value,
                                              target.row, target.col)
      new_dist = self.get_tile_manhattan_dist(target.value,
                                              blank.row, blank.col)
      return new_dist - old_dist

   def get_tile_manhattan_dist(self, value, row, col):
      # don't count the blank space
      if value == 0:
         return 0

      goal_col = value % self.width
      goal_row = int(value / self.width)
      return abs(col - goal_col) + abs(row - goal_row)

   def find_blank(self):
      blank_tile = None
      for i in range(self.board_len):
         if self.board[i] == 0:
            row = int(i / self.width)
            col = i % self.width
            blank_tile = Tile(self.board[i], row, col)
      self.blank_tile = blank_tile

   def get_target(self, move):
      blank = self.blank_tile
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
         target_index = target.row * self.width + target.col
         target.value = self.board[target_index]
         return target

   def in_bounds(self, target):
      if (0 <= target.row < self.width) and (0 <= target.col < self.width):
         return True
      return False

   def swap_tiles(self, target):
      blank = self.blank_tile
      target_index = target.row * self.width + target.col
      blank_index = blank.row * self.width + blank.col
      self.board[blank_index] = target.value
      self.board[target_index] = blank.value
      self.blank_tile.row = target.row
      self.blank_tile.col = target.col


def add_to_set(the_set, puzzle):
   threshold_width = 4
   if (puzzle.width < threshold_width):
      the_set.add((puzzle.combined_cost, puzzle.tuple_board))
   else:
      the_set.add(puzzle.tuple_board)
   return the_set

def check_in_set(the_set, item):
   threshold_width = 4
   if (item.width < threshold_width):
      return (item.combined_cost, item.tuple_board) in the_set
   else:
      return item.tuple_board in the_set

def solve_puzzle(tiles):
   # set up inital puzzle state
   sqr_root_exp = 0.5
   width = int(len(tiles) ** (sqr_root_exp))

   init_puzzle = create_init_puzzle(tiles, width)

   # initialize frontier and explored
   frontier_q = queue.PriorityQueue()
   frontier_set = set()
   explored = set()

   # add inital puzzle state to frontier
   frontier_q.put(init_puzzle)
   frontier_set = add_to_set(frontier_set, init_puzzle)

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
            and not check_in_set(frontier_set, state)):

            # if the successor is the goal, stop
            if state.manhattan_dist == 0:
               # if len(state.path) == 22:
               #   return (state.path[0:20])
               return(state.path)
               #calculate_soln()
               #exit

            frontier_q.put(state)
            frontier_set = add_to_set(frontier_set, state)

      # push parent on the closed list
      explored.add(parent.tuple_board)


def test_output(puzzle):
   # test: print out all tile values in the puzzle
   print('[')
   for i in range(puzzle.width):
      print('[', end='')
      for j in range(puzzle.width):
         index = i * puzzle.width + j
         print(puzzle.board[index], end=' ')
         #print(puzzle.board[i][j].value, " (", puzzle.board[i][j].row, ", ", puzzle.board[i][j].col, ")", sep="", end=' ')
      print(']')
   print(']')

   # test: print out the manhattan_dist for init puzzle
   # print("man dist:", puzzle.manhattan_dist)
   # print("path cost:", puzzle.path_cost)
   # print("path:", puzzle.path)


def print_board(puzzle):
   # test: print out all tile values in the puzzle
   print(puzzle.board)


def create_init_puzzle(tiles, width):
   init_puzzle = Puzzle(tiles)

   init_puzzle.find_blank()
   init_puzzle.manhattan_dist = init_puzzle.get_manhattan_dist()
   init_puzzle.set_combined_cost()
   init_puzzle.set_tuple_board()

   # test initial board
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
   fringe_states = []

   for move in puzzle.moves:
      target = puzzle.get_target(move)
      if target:
         next_puzzle = create_next_puzzle(puzzle, target, move)
         fringe_states.append(next_puzzle)

   return fringe_states


def create_next_puzzle(puzzle, target, move):
   next_board = copy.deepcopy(puzzle.board)
   next_puzzle = Puzzle(next_board)
   next_puzzle.blank_tile.row = puzzle.blank_tile.row
   next_puzzle.blank_tile.col = puzzle.blank_tile.col
   manhattan_delta = next_puzzle.get_manhattan_delta(target)
   next_puzzle.swap_tiles(target)
   next_puzzle.set_tuple_board()
   next_puzzle.path = puzzle.path + move
   next_puzzle.path_cost = puzzle.path_cost + 1
   next_puzzle.manhattan_dist = puzzle.manhattan_dist + manhattan_delta
   next_puzzle.set_combined_cost()

   return next_puzzle


def main():
   # test tile lists
   # answer: 6
   # tiles = [3, 2, 1, 0]

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

   # soln = solve_puzzle(tiles)
   # print("cost:", len(soln))
   # print("soln:", soln)
   test_main()

def test_main():
   # test tile lists
   # answer: 6
   print("TEST 1:")
   tiles = [3, 2, 1, 0]
   start_time = round(time.clock(), 2)
   soln = solve_puzzle(tiles)
   end_time = round(time.clock(), 2)
   print("expected cost:", 6)
   print("actual cost:", len(soln))
   print("soln:", soln)
   print("execution time:", end_time - start_time)
   print()

   # answer: 20
   print("TEST 2:")
   tiles = [7, 1, 8, 6, 3, 4, 0, 5, 2]
   start_time = round(time.clock(), 2)
   soln = solve_puzzle(tiles)
   end_time = round(time.clock(), 2)
   print("expected cost:", 20)
   print("actual cost:", len(soln))
   print("soln:", soln)
   print("execution time:", end_time - start_time)
   print()

   # answer: 28
   print("TEST 3:")
   tiles = [8, 5, 4, 7, 0, 6, 2, 1, 3]
   start_time = round(time.clock(), 2)
   soln = solve_puzzle(tiles)
   end_time = round(time.clock(), 2)
   print("expected cost:", 28)
   print("actual cost:", len(soln))
   print("soln:", soln)
   print("execution time:", end_time - start_time)
   print()

   # answer: 31
   print("TEST 4:")
   tiles = [8, 0, 6, 5, 4, 7, 2, 3, 1]
   start_time = round(time.clock(), 2)
   soln = solve_puzzle(tiles)
   end_time = round(time.clock(), 2)
   print("expected cost:", 31)
   print("actual cost:", len(soln))
   print("soln:", soln)
   print("execution time:", end_time - start_time)
   print()

   # answer: 36
   print("TEST 5:")
   tiles = [5, 1, 3, 7, 9, 6, 4, 11, 13, 8, 14, 2, 12, 10, 15, 0]
   start_time = round(time.clock(), 2)
   soln = solve_puzzle(tiles)
   end_time = round(time.clock(), 2)
   print("expected cost:", 36)
   print("actual cost:", len(soln))
   print("soln:", soln)
   print("execution time:", end_time - start_time)
   print()

   # answer: 40
   print("TEST 6:")
   tiles = [2, 12, 3, 4, 9, 1, 0, 11, 7, 6, 5, 10, 17, 13, 14, 15, 16, 8, 24, 18, 20, 21, 19, 22, 23]
   start_time = round(time.clock(), 2)
   soln = solve_puzzle(tiles)
   end_time = round(time.clock(), 2)
   print("expected cost:", 40)
   print("actual cost:", len(soln))
   print("soln:", soln)
   print("execution time:", end_time - start_time)
   print()


if __name__ == "__main__":
   main()
