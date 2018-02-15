# Name:        Lexa Hall
# Course:      CSC 480
# Instructor:  Daniel Kauffman
# Assignment:  Board Stupid
# Term:        Winter 2018

import copy

# ------------------- REQUIRED FUNCTIONS --------------------------------------


# player: player making the move
#   1: MAX, -1: MIN
# returns: appropriate utility backtracked up from on of the leaves of the game
# tree
def search_tree(board, width, player):
  # if the current game state is a terminal state:
  if is_terminal(board, width, player):
  #   return a utility based on the player that moved
    return get_utility(board, width, player)

  best_value = - sys.maxint
  possible_boards = get_possible_boards(board, player)
  # for each valid move in the current game state:
  for next_board in possible_boards:
#   call search_tree with the move applied to the game state
    u = -search_tree(next_board, width, -player)
#   negate the utility returned by search_tree
    best_value = max(best_value, u)
#   if this utility is the current best, store it
# return the best utility
  return best_value


def get_utility(board, width, player):
  if is_terminal(board, width, player):
    result = get_result(board, width)
    return result

  return None


# ------------------- HELPER FUNCTIONS ----------------------------------------

def is_terminal(board, width, player):
  result = get_result(board, width)

  if result:
    return True

  return is_tie_board(board, width, player)


def is_tie_board(board, width, player):
  current_player_piece = get_player_piece(player)
  next_player_piece = get_player_piece(-player)

  blank_indicies = find_blanks(board)
  num_blanks = len(blank_indicies)

  if num_blanks == 0:
    return True

  total_boards = []

  if num_blanks > 2:
    return False

  if num_blanks == 1:
    possible_board = copy.deepcopy(board)
    possible_board[blank_indicies[0]] = current_player_piece
    total_boards.append(possible_board)

  if num_blanks == 2:
    possible_board_one = copy.deepcopy(board)
    possible_board_one[blank_indicies[0]] = current_player_piece
    possible_board_one[blank_indicies[1]] = next_player_piece
    total_boards.append(possible_board_one)

    possible_board_two = copy.deepcopy(board)
    possible_board_two[blank_indicies[0]] = next_player_piece
    possible_board_two[blank_indicies[1]] = current_player_piece
    total_boards.append(possible_board_two)

  return check_no_winner(total_boards, width)


def check_no_winner(boards, width):
  for board in boards:
    if get_result(board, width):
      return False

  return True


def get_result(board, width):
  lanes = build_lanes(board, width)

  for lane in lanes:
    if lane[0] == lane[1] == lane[2]:
      if lane[0] == 'O':
        return -1
      else:
        return 1

  return 0


def get_possible_boards(board, player):
  possible_boards = []
  blank_indicies = find_blanks(board)
  player_piece = get_player_piece(player)

  for blank in blank_indicies:
    next_board = copy.deepcopy(board)
    next_board[blank] = player_piece
    possible_boards.append(next_board)

  return possible_boards


def get_player_piece(player):
  piece = ''
  piece = 'O' if player == -1 else 'X'

  return piece


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
