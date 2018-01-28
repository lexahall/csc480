import random

## TILE -----------------------------------------------------------------------
class Tile(object):
   def __init__(self, value, row, col):
      self.value = value
      self.row = row
      self.col = col

## PUZZLE ---------------------------------------------------------------------
class Puzzle(object):
   def __init__(self, board, width):
      self.moves = ['h', 'j', 'k', 'l']
      self.width = width
      self.path_cost = 0
      self.path = ''
      self.manhattan_dist = 0
      self.combined_cost = self.path_cost + self.manhattan_dist
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
      for i in range(self.board_len):
         if self.board[i] == 0:
            row = int(i / self.width)
            col = i % self.width
            blank_tile = Tile(self.board[i], row, col)
      self.blank_tile = blank_tile

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
   board = anneal(width)[0]
   return board

# TODO: rewrite for tiledriver
def anneal(solution):
   old_cost = cost(solution)
   T = 1.0
   T_min = 0.00001
   alpha = 0.9
   while T > T_min:
      i = 1
      while i <= 100:
         new_solution = neighbor(solution)
         new_cost = cost(new_solution)
         ap = acceptance_probability(old_cost, new_cost, T)
         if ap > random():
            solution = new_solution
            old_cost = new_cost
         i += 1
      T = T*alpha
   return solution, old_cost

def find_num_conflicts(tiles):

   #for all rows/columns:
      #construct list of tiles in goal row/col
      #call count_conflicts
   # return sum of all conflicts

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
   board = hill_climb(width)
   return board

def hill_climb(width):
   total_hill_climbs = 1000

   retun board

## SHARED ---------------------------------------------------------------------
def is_solvable(tiles):
   sqr_rt = 0.5
   board_width = len(tiles)**(sqr_rt)
   num_inverstions = count_inversions(tiles)

   if (board_width % 2 == 0):
      blank = findBlank(tiles)
      if (blank.row % 2 == 0) and (num_inversions % 2 != 0):
         return True
      if (blank.row % 2 != 0) and (num_inversions % 2 == 0):
         return True
   elif (board_width % 2 != 0) and (num_inversions % 2 == 0):
      return True

   return False

def count_inversions(tiles):
   length = len(tiles)
   temp = []
   return merge_sort(tiles, temp, 0, length - 1)

def merge_sort(arr, temp, left, right):
   mid = 0
   num_inversions = 0

   if right > left:
      mid = (right + left) // 2
      num_inversions = merge_sort(arr, temp, left, mid)
      num_inversions += merge_sort(arr, temp, mid + 1, right)
      num_inversions += merge(arr, temp, left, mid + 1, right)

   return num_inverstions

def merge(arr, temp, left, mid, right):
   num_inversions = 0
   i = left    # index for left subarray
   j = mid     # index for right subarray
   k = left    # index for resultant merged subarray

   while (i <= mid - 1) and (j <= right):
      if arr[i] = arr[j]:
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

   for i in range(left, right):
      arr[i] = temp[i]

   return num_inverstions

## SOLVE PUZZLE ---------------------------------------------------------------
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
               # if len(state.path) == 22:
               #   return (state.path[0:20])
               return(state.path)
               #calculate_soln()
               #exit

            frontier_q.put(state)
            frontier_set.add(state)

      # push parent on the closed list
      explored.add(tuple(parent.board))


def create_init_puzzle(tiles, width):
   init_puzzle = Puzzle(tiles, width)

   init_puzzle.find_blank()
   init_puzzle.manhattan_dist = init_puzzle.get_manhattan_dist()
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
   next_puzzle.set_combined_cost()

   return next_puzzle
