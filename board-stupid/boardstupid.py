# Name:        Lexa Hall
# Course:      CSC 480
# Instructor:  Daniel Kauffman
# Assignment:  Board Stupid
# Term:        Winter 2018

# ------------------- REQUIRED FUNCTIONS --------------------------------------


# player: player making the move
#   1: MAX, -1: MIN
# returns: appropriate utility backtracked up from on of the leaves of the game
# tree
 def search_tree(board, width, player = -1):
  # if the current game state is a terminal state:
  #   return a utility based on the player that moved
  # for each valid move in the current game state:
  #   call search_tree with the move applied to the game state
  #   negate the utility returned by search_tree
  #   if this utility is the current best, store it
  # return the best utility
  return




# determines whether the game is a terminal state
#   if so, determines which player wins
# return:
#   0 for tie
#   1 for MAX wins
#   -1 for MIN wins
#   None otherwise
def get_utility(board, width, player):
  result = get_result(board, width)
  blank_indicies = find_blanks(board)
  num_blanks = len(blank_indicies)
  if is_terminal(result, board, width, player, num_blanks, blank_indicies):
    return result

  return None



# ------------------- HELPER FUNCTIONS ----------------------------------------

def is_terminal(result, board, width, player, num_blanks, blank_indicies):
  return (
    result
    or num_blanks == 0
    or is_tie_board(board, width, player, num_blanks, blank_indicies)
  )

  current_player = get_player_piece(player)
  next_player = get_player_piece(player, True)
  total_boards = []

  if num_blanks > 2:
    return False


  return check_no_winner(total_boards, width)


def is_tie_board(board, width, player, num_blanks, blank_indicies):
  current_player = get_player_piece(player)
  next_player = get_player_piece(player, True)
  total_boards = []

  if num_blanks > 2:
    return False

  if num_blanks ==1:
    possible_board = copy.deepcopy(board)
    possible_board[blank_indicies[0]] = current_player
    total_boards.append(possible_board)

  if num_blanks == 2:
    possible_board_one = copy.deepcopy(board)
    possible_board_one[blank_indicies[0]] = current_player
    possible_board_one[blank_indicies[1]] = next_player
    total_boards.append(possible_board_one)

    possible_board_two = copy.deepcopy(board)
    possible_board_two[blank_indicies[0]] = next_player
    possible_board_two[blank_indicies[1]] = current_player
    total_boards.append(possible_board_two)

  return check_no_winner(total_boards, width)


def check_no_winner(boards, width):
  for board in boards:
    if get_result(board, width):
      return False

  return True


def get_possible_boards(board, player):
  possible_boards = []
  blank_indicies = find_blanks(board)

  for blank in blank_indicies:
    next_board = copy.deepcopy(board)
    next_board[blank] = player
    possible_boards.append(next_board)

  return possible_boards


def get_player_piece(player, invert = False):
  piece = ''
  piece = 'O' if player == -1 else 'X'

  if invert:
    piece = 'X' if piece == 'O' else 'O'

  return piece


def get_result(board, width):
  lanes = build_lanes(board, width)

  for lane in lanes:
    if lane[0] == lane[1] == lane[2]:
      if lane[0] == 'O':
        return -1
      else:
        return 1

  return 0


def build_lanes(board, width):
  rows = [board[i:i + width] for i in range(0, width * width, width)]
  cols = [board[i::width] for i in range(0, width)]
  diag1 = [[board[width * i + i] for i in range(0, width)]]
  diag2 = [[board[width * i + width - i - 1] for i in range(0, width)]]
  lanes = rows + cols + diag1 + diag2
  return lanes


def find_blanks(board):
  blank_indicies = []
  for i in range(len(board)):
    if isinstance(board[i], int):
      blank_indicies.append(i)

  return blank_indicies
