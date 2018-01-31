# Name:        Lexa Hall
# Course:      CSC 480
# Instructor:  Daniel Kauffman
# Assignment:  Tile Driver
# Term:        Winter 2018

import math
import random
import queue
import copy

## TILE -----------------------------------------------------------------------
class Tile(object):
   def __init__(self, value, row, col, index = 0):
      self.value = value
      self.row = row
      self.col = col
      self.index = index

## PUZZLE ---------------------------------------------------------------------
class Puzzle(object):
   def __init__(self, board, width):
      self.moves = ['h', 'j', 'k', 'l']
      self.width = width
      self.num_conflicts = 0
      self.path_cost = 0
      self.path = ''
      self.manhattan_dist = 0
      self.combined_cost = (self.path_cost +
                            self.manhattan_dist +
                            self.num_conflicts)
      self.board = board
      self.blank_tile = Tile(0, 0, 0)
      self.board_len = len(board)

   def __lt__(self, other):
      return self.combined_cost < other.combined_cost

   def __hash__(self):
      return hash(tuple(self.board)) ^ hash(self.path_cost)

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
      blank_index = self.find_blank_index()

      row = int(blank_index / self.width)
      col = blank_index % self.width

      blank_tile = Tile(self.board[blank_index], row, col, blank_index)
      self.blank_tile = blank_tile

   def find_blank_index(self):
      blank_index = 0
      for i in range(self.board_len):
         if self.board[i] == 0:
            blank_index = i
            break
      return blank_index

   def get_target(self, move):
      if self.is_comp_move(move):
         return None

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

   def is_comp_move(self, move):
      if self.path_cost == 0:
         return False

      prev_move = self.path[self.path_cost - 1]

      if (move == 'h' and prev_move == 'l'):
         return True
      elif (move == 'j' and prev_move == 'k'):
         return True
      elif (move == 'k' and prev_move == 'j'):
         return True
      elif (move == 'l' and prev_move == 'h'):
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


## CONFLICT TILES -------------------------------------------------------------
def conflict_tiles(width):
   tiles = fill_tiles_in_order(width)
   puzzle = create_init_puzzle(tiles, width)
   tiles = simulated_annealing(puzzle)
   #tiles = conflict_hill_climb(width)
   return tiles

def conflict_hill_climb(width):
   total_hill_climbs = 1000
   hill_climbs = 0
   tiles = fill_tiles_in_order(width)
   global_max = create_init_puzzle(tiles, width)
   global_max.num_conflicts = find_num_conflicts(global_max.board, width)
   global_cost = 0
   explored = set()
   explored.add(tuple(global_max.board))

   while(hill_climbs < total_hill_climbs):
      hill_climbs += 1
      num_better_states = 1
      tiles = generate_random_board(width)

      # keep generating a random baord if current board has been explored
      while(tuple(tiles) in explored):
         tiles = generate_random_board(width)

      local_max = create_init_puzzle(tiles, width)
      local_max.num_conflicts = find_num_conflicts(local_max.board, width)
      explored.add(tuple(tiles))

      # find local max
      while num_better_states:
         #print("in while")
         num_better_states = 0

         fringe_states = get_fringe_states(local_max)

         # find best next state
         max_cost = 0
         max_index = 0
         index = 0

         for state in fringe_states:
            #print("states")
            if not tuple(state.board) in explored:
               if state.num_conflicts > max_cost:
                  max_cost = state.num_conflicts
                  max_index = index

            index += 1

         fringe_max = fringe_states[max_index]

         # state.manhattan_dist = state.get_manhattan_dist()
         #print()
         #print("local conflicts:", local_max.num_conflicts)
         #print("fringe conflicts:", fringe_max.num_conflicts)
         if fringe_max.num_conflicts > local_max.num_conflicts:
            local_max = fringe_max
            num_better_states += 1
            #print("better state")

      # update glabal_max as needed
      #print()
      #print("Iteration:", hill_climbs)
      #print("Local max:", local_max.board)
      #print("local conflicts:", local_max.num_conflicts)
      #print("global max:", global_max.board)
      #print("global conflicts:", global_max.num_conflicts)

      if (local_max.num_conflicts > global_max.num_conflicts):
         local_cost = len(solve_puzzle(local_max.board))
         #print("Local cost:", local_cost)
         if local_cost > global_cost:
            global_max = local_max
            global_cost = local_cost

   #print(global_max.board)
   #print(global_cost)
   return global_max.board


def simulated_annealing(puzzle):
   total_iterations = 20
   num_iterations = 0
   global_max = puzzle

   while (num_iterations < total_iterations):
      num_iterations += 1
      new_puzzle = anneal(puzzle)
      if (new_puzzle.num_conflicts > global_max.num_conflicts):
         global_max = new_puzzle

   return global_max.board


def anneal(puzzle):
   old_complexity = find_num_conflicts(puzzle.board, puzzle.width)
   T = 1.0
   T_min = 0.0001
   alpha = 0.91
   while T > T_min:
      i = 1
      num_iterations = 500
      while i <= num_iterations:
         # get all fringe states
         fringe_states = get_fringe_states(puzzle)
         next_puzzle = pick_randon_state(fringe_states)
         new_complexity = find_num_conflicts(next_puzzle.board,
                                             next_puzzle.width)
         ap = acceptance_probability(old_complexity, new_complexity, T)
         if ap > random.random():
            puzzle = next_puzzle
            old_complexity = new_complexity
         i += 1
      T = T * alpha
   return puzzle


def acceptance_probability(old_complexity, new_complexity, T):
   if new_complexity > old_complexity:
      return 1

   if (old_complexity == new_complexity):
      return random.random()

   return math.exp((new_complexity - old_complexity) / T)


def pick_randon_state(fringe_states):
   random.shuffle(fringe_states)
   return fringe_states[0]


def find_num_conflicts(tiles, width):
   num_conflicts = 0
   board = build_board(tiles, width)
   num_conflicts += count_row_conflicts(board, width)
   num_conflicts += count_col_conflicts(board, width)

   return num_conflicts


def build_board(tiles, width):
   board = []
   for i in range(width):
      chunk_start = i * width
      chunk_end = i * width + width

      board.append(
         [value for value in tiles[chunk_start : chunk_end]]
      )

   return board


def count_row_conflicts(board, width):
   row = []
   num_conflicts = 0

   for i in range(width):
      for j in range(width):
         value = board[i][j]
         if (value != 0 and ((value // width) == i)):
            row.append(board[i][j])
      if len(row) > 1:
         num_conflicts += count_conflicts(row)
      row = []

   return num_conflicts


def count_col_conflicts(board, width):
   col = []
   num_conflicts = 0

   for j in range(width):
      for i in range(width):
         value = board[i][j]
         if (value != 0 and ((value % width) == j)):
            col.append(board[i][j])
      if len(col) > 1:
         num_conflicts += count_conflicts(col)
      col = []

   return num_conflicts


def count_conflicts(tiles):
   length = len(tiles)

   if length == 1: # Base Case
      return 0

   head = tiles[0]
   for i in range(1, length):
      if tiles[i] < head:
         return 1 + count_conflicts(tiles[1:length]) # conflict detected

   return count_conflicts(tiles[1:length]) # no conflict detected

## SHUFFLE TILES --------------------------------------------------------------
def shuffle_tiles(width):
   #tiles = hill_climb(width)
   tiles = fill_tiles_in_order(width)
   puzzle = create_init_puzzle(tiles, width)
   tiles = simulated_annealing_path_cost(puzzle)
   return tiles

def simulated_annealing_path_cost(puzzle):
   total_iterations = 20
   threshold = 28 if puzzle.width == 3 else 0
   num_iterations = 0
   global_max = puzzle
   global_max.path_cost = len(solve_puzzle(puzzle.board))

   while (global_max.path_cost < threshold or num_iterations < total_iterations):
      num_iterations += 1
      new_puzzle = anneal_path_cost(puzzle)
      if (new_puzzle.manhattan_dist > global_max.manhattan_dist):
         new_puzzle.path_cost = len(solve_puzzle(new_puzzle.board))
         if (new_puzzle.path_cost > global_max.path_cost):
            global_max = new_puzzle

   return global_max.board


def anneal_path_cost(puzzle):
   old_complexity = puzzle.manhattan_dist
   T = 1.0
   T_min = 0.0001
   alpha = 0.91
   while T > T_min:
      i = 1
      num_iterations = 500
      while i <= num_iterations:
         # get all fringe states
         fringe_states = get_fringe_states(puzzle)
         next_puzzle = pick_randon_state(fringe_states)
         new_complexity = next_puzzle.manhattan_dist
         ap = acceptance_probability(old_complexity, new_complexity, T)
         if ap > random.random():
            puzzle = next_puzzle
            old_complexity = new_complexity
         i += 1
      T = T * alpha
   return puzzle


def hill_climb(width):
   total_hill_climbs = 1000
   hill_climbs = 0
   tiles = fill_tiles_in_order(width)
   global_max = create_init_puzzle(tiles, width)
   global_cost = 0
   explored = set()
   explored.add(tuple(global_max.board))

   while(hill_climbs < total_hill_climbs):
      hill_climbs += 1
      num_better_states = 1
      tiles = generate_random_board(width)

      # keep generating a random baord if current board has been explored
      while(tuple(tiles) in explored):
         tiles = generate_random_board(width)

      local_max = create_init_puzzle(tiles, width)
      explored.add(tuple(tiles))

      # find local max
      while num_better_states:
         print("in while")
         num_better_states = 0

         fringe_states = get_fringe_states(local_max)

         # find best next state
         max_cost = 0
         max_index = 0
         index = 0

         for state in fringe_states:
            print("states")
            if not tuple(state.board) in explored:
               if state.manhattan_dist > max_cost:
                  max_cost = state.manhattan_dist
                  max_index = index

            index += 1

         fringe_max = fringe_states[max_index]

         # state.manhattan_dist = state.get_manhattan_dist()
         print()
         print("local manhattan:", local_max.manhattan_dist)
         print("fringe manhattan:", fringe_max.manhattan_dist)
         if fringe_max.manhattan_dist > local_max.manhattan_dist:
            local_max = fringe_max
            num_better_states += 1
            print("better state")

      # update glabal_max as needed
      print()
      print("Iteration:", hill_climbs)
      print("Local max:", local_max.board)
      print("local manhattan_dist:", local_max.manhattan_dist)
      print("global max:", global_max.board)
      print("global manhattan_dist:", global_max.manhattan_dist)

      if (local_max.manhattan_dist > global_max.manhattan_dist):
         local_cost = len(solve_puzzle(local_max.board))
         print("Local cost:", local_cost)
         if local_cost > global_cost:
            global_max = local_max
            global_cost = local_cost

   print(global_max.board)
   print(global_cost)
   return global_max.board


def generate_random_board(width):
   tiles = []
   solvable = False

   while not solvable:
      tiles = fill_tiles_in_order(width)
      random.shuffle(tiles)
      solvable = is_solvable(copy.deepcopy(tiles))

   return tiles

## SHARED ---------------------------------------------------------------------
def fill_tiles_in_order(width):
   tiles = []
   for i in range(int(pow(width, 2))):
      tiles.append(i)
   return tiles


def is_solvable(tiles):
   length = len(tiles)
   board_width = int(math.sqrt(length))
   blank = find_blank_tile(tiles, board_width, length)
   num_inversions = count_inversions(tiles, length, blank.index)

   if (board_width % 2 == 0):
      if (blank.row % 2 == 0):
         return num_inversions % 2 == 0
      if (blank.row % 2 != 0):
         return num_inversions % 2 != 0
   elif (board_width % 2 != 0):
      return num_inversions % 2 == 0

# def count_inversions_simple(tiles, length, blank_index):
#    del tiles[blank_index]
#    length = length - 1
#    num_inversions = 0
#    for i in range(length - 1):
#       for j in range(i + 1, length):
#          if (tiles[i] > tiles[j]):
#             num_inversions += 1
#
#    return num_inversions

def count_inversions(tiles, length, blank_index):
   del tiles[blank_index]
   length = length - 1
   temp = [None] * length
   return merge_sort(tiles, temp, 0, length - 1)


def find_blank_tile(tiles, width, length):
   blank_tile = None
   blank_index = find_blank_tile_index(tiles, length)

   row = blank_index // width
   col = blank_index % width

   blank_tile = Tile(tiles[blank_index], row, col, blank_index)
   return blank_tile


def find_blank_tile_index(tiles, length):
   blank_index = 0
   for i in range(length):
      if tiles[i] == 0:
         blank_index = i
   return blank_index


def merge_sort(arr, temp, left, right):
   mid = 0
   num_inversions = 0

   if right > left:
      mid = (right + left) // 2
      num_inversions = merge_sort(arr, temp, left, mid)
      num_inversions += merge_sort(arr, temp, mid + 1, right)
      num_inversions += merge(arr, temp, left, mid + 1, right)

   return num_inversions


def merge(arr, temp, left, mid, right):
   num_inversions = 0
   i = left    # index for left subarray
   j = mid     # index for right subarray
   k = left    # index for resultant merged subarray

   while (i <= mid - 1) and (j <= right):
      if arr[i] <= arr[j]:
         temp[k] = arr[i]
         i += 1
         k += 1
      else:
         temp[k] = arr[j]
         j += 1
         k += 1
         num_inversions += mid - i

   while (i <= mid - 1):
      temp[k] = arr[i]
      i += 1
      k += 1

   while (j <= right):
      temp[k] = arr[j]
      j += 1
      k += 1

   for i in range(left, right + 1):
      arr[i] = temp[i]

   return num_inversions

## SOLVE PUZZLE ---------------------------------------------------------------
def solve_puzzle(tiles):
   # set up inital puzzle state
   width = int(math.sqrt(len(tiles)))

   init_puzzle = create_init_puzzle(tiles, width)
   if init_puzzle.manhattan_dist == 0:
      return ''

   # initialize frontier and explored
   frontier_q = queue.PriorityQueue()
   frontier_set = set()
   explored = set()

   # add inital puzzle state to frontier
   frontier_q.put(init_puzzle)
   frontier_set.add(init_puzzle)

   # while there are still states in the frontier
   while not frontier_q.empty():
      # pop node with the lowest f(n) - node q
      parent = frontier_q.get()

      # generate all of q's successors and set their parent to q
      fringe_states = get_fringe_states(parent)

      # for each successor:
      for state in fringe_states:
         # check that the current state has not already been explored
         if ((not tuple(state.board) in explored)
            and (not state in frontier_set)):

            # if the successor is the goal, stop
            if state.manhattan_dist == 0:
               return(state.path)

            frontier_q.put(state)
            frontier_set.add(state)

      # push parent on the closed list
      explored.add(tuple(parent.board))


def create_init_puzzle(tiles, width):
   init_puzzle = Puzzle(tiles, width)

   init_puzzle.find_blank()
   init_puzzle.manhattan_dist = init_puzzle.get_manhattan_dist()
   init_puzzle.num_conflicts = find_num_conflicts(tiles, width)
   init_puzzle.set_combined_cost()

   return init_puzzle


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
   next_puzzle = Puzzle(next_board, puzzle.width)
   next_puzzle.blank_tile.row = puzzle.blank_tile.row
   next_puzzle.blank_tile.col = puzzle.blank_tile.col
   manhattan_delta = next_puzzle.get_manhattan_delta(target)
   next_puzzle.swap_tiles(target)
   next_puzzle.path = puzzle.path + move
   next_puzzle.path_cost = puzzle.path_cost + 1
   next_puzzle.manhattan_dist = puzzle.manhattan_dist + manhattan_delta
   next_puzzle.num_conflicts = find_num_conflicts(
                                                   next_puzzle.board,
                                                   puzzle.width
                                                 )
   next_puzzle.set_combined_cost()

   return next_puzzle
