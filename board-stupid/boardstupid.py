# Name:        Lexa Hall
# Course:      CSC 480
# Instructor:  Daniel Kauffman
# Assignment:  Board Stupid
# Term:        Winter 2018

import copy
import math
import random


class Node(object):
  def __init__(self, player, wins, losses, total, visits, board):
    self.player = player
    self.wins = wins
    self.total = total
    self.visits = visits
    self.board = board


#TODO: keep track of how many times visited, insert node with correct win/loss
# record.. switch depending on player when pulling out of tree
def search_tree_mc(board, width, player, table):
  if is_terminal(board, width, player):
    utility = get_utility_3d(board, width, player)
    print('utility', utility)
    return utility

  best_ucb = - float("inf")
  best_node = None
  possible_boards = get_possible_boards(board, width, player)
  for current_board in possible_boards:
    node = get_node_from_table(current_board, table, width)
    if not node:
      node = Node(player, 0, 0, 1, 1, current_board) #TODO: assign total and visits properly?
    ucb = get_upper_confidence_bound(node)
    if ucb > best_ucb:
      best_ucb = ucb
      best_node = node
    elif ucb == best_ucb:
      # for ties, randomly select a node
      rand_selection = random.randint(0, 2)
      if rand_selection == 0:
        best_node = node

    print(ucb)
    print(best_ucb)

  utility = search_tree_mc(best_node.board, width, -player, table)
  node = get_node_from_table(best_node.board, table, width)
  if not node:
    node = Node(player, 0, 0, 1, 1, best_node.board) #TODO: assign total and visits properly?
  update_node_in_table(board, table, node, width)
  return utility


def get_node_from_table(board, table, width):
  transpositions = make_transpositions(board, width)
  minimum_hash = get_minimum_hash(transpositions)
  return table.get(minimum_hash)


def update_node_in_table(board, table, node, width):
  transpositions = make_transpositions(board, width)
  minimum_hash = get_minimum_hash(transpositions)
  table.update({minimum_hash : node})


def search_tree(board, width, player):
  if is_terminal(board, width, player):
    return player * get_utility(board, width, player)

  best_value = - float("inf")

  possible_boards = get_possible_boards(board, width, player)

  for next_board in possible_boards:
    u = -search_tree(next_board, width, -player)
    best_value = max(best_value, u)
    if best_value == 1:
      break

  return best_value


def get_minimum_hash(transpositions):
  minimum_hash = float("inf")

  for transposition in transpositions:
    current_hash = hash(transposition)
    minimum_hash = min(current_hash, minimum_hash)

  return minimum_hash

def get_upper_confidence_bound(node):
  return ((node.wins + 1) / (node.visits + 1) +
    math.sqrt((2 *math.log1p(node.total) + 1 ) / (node.visits + 1))
  )


def get_utility_3d(board, width, player):
  flat_boards = build_boards(board, width)

  for flat_board in flat_boards:
    if is_terminal(flat_board, width, player):
      lanes = build_board_lanes(flat_board, width)
      result = get_result(flat_board, width, lanes)
      return result

  return None


def get_utility(board, width, player):
  if is_terminal(board, width, player):
    lanes = build_board_lanes(board, width)
    result = get_result(board, width, lanes)
    return result

  return None


def make_transpositions(board, width):
  if type(board[0]) is list:
    all_transpositions = []
    transpositions_3d = []

    for flat_board in board:
      transpositions = make_individual_transpositions(flat_board, width)
      all_transpositions.append(transpositions)

    num_transpositions = 8
    for j in range(num_transpositions):
      transpostion_3d = []
      for i in range(width):
        transpostion_3d.append(all_transpositions[i][j])
      transpositions_3d.append(tuple(transpostion_3d))

    reverse_transpositions = []
    for transposition in transpositions_3d:
      reverse_transpositions.append(transposition[::-1])

    for reverse in reverse_transpositions:
      transpositions_3d.append(reverse)

    return tuple(transpositions_3d)

  else:
    transpositions = make_individual_transpositions(board, width)

  return transpositions


def make_individual_transpositions(board, width):
  transpositions = []
  rows = [board[i:i + width] for i in range(0, width * width, width)]
  cols = [board[i::width] for i in range(0, width)]

  board_one = []

  for i in range(width):
    for j in range(width - 1, -1, -1):
      board_one.append(rows[i][j])

  transpositions.append(tuple(board))
  transpositions.append(tuple(board_one))

  rotate_board(width, width - 1, -1, -1, rows, transpositions)
  rotate_board(width, 0, width, 1, cols, transpositions)
  rotate_board(width, width - 1, -1, -1, cols, transpositions)

  return tuple(transpositions)


def rotate_board(width, start, stop, step, lists, transpositions):
  board_one = []
  board_two = []

  for i in range(start, stop, step):
    board_one += lists[i]
    for j in range(width - 1, -1, -1):
      board_two.append(lists[i][j])

  transpositions.append(tuple(board_one))
  transpositions.append(tuple(board_two))


def is_terminal(board, width, player):
  if type(board[0]) is list:
    for flat_board in board:
      is_terminal = is_terminal_2d(flat_board, width, player)
      if not is_terminal:
        return False
  else:
    return is_terminal_2d(board, width, player)

  return True


def is_terminal_2d(board, width, player):
  lanes = build_board_lanes(board, width)
  if type(board[0]) is list:
    for flat_board in board:
      result = get_result(board, width, lanes)
  else:
    result = get_result(board, width, lanes)

  if result:
    return True

  return is_tie_board(board, width, player)


def is_tie_board(board, width, player):
  current_player_piece = get_player_piece(player)
  next_player_piece = get_player_piece(-player)

  blank_indicies = find_blanks(board, width)
  num_blanks = len(blank_indicies)

  if num_blanks == 0:
    return True

  total_boards = []

  if num_blanks > 2:
    return False

  if num_blanks == 1:
    possible_board = copy.copy(board)
    possible_board[blank_indicies[0]] = current_player_piece
    total_boards.append(possible_board)

  if num_blanks == 2:
    possible_board_one = copy.copy(board)
    possible_board_one[blank_indicies[0]] = current_player_piece
    possible_board_one[blank_indicies[1]] = next_player_piece
    total_boards.append(possible_board_one)

    possible_board_two = copy.copy(board)
    possible_board_two[blank_indicies[0]] = next_player_piece
    possible_board_two[blank_indicies[1]] = current_player_piece
    total_boards.append(possible_board_two)

  return check_no_winner(total_boards, width)


def check_no_winner(boards, width):
  for board in boards:
    lanes = build_board_lanes(board, width)
    if get_result(board, width, lanes):
      return False

  return True


def get_result(board, width, lanes):
  for lane in lanes:
    lane_set = set()
    for i in lane:
      lane_set.add(i)
    if lane_set == set('O'):
      return -1
    elif lane_set == set('X'):
      return 1

  return 0


def get_possible_boards(board, width, player):
  possible_boards = []
  blank_indicies = find_blanks(board, width)
  player_piece = get_player_piece(player)

  for blank in blank_indicies:
    if type(blank) is list:
      next_board = copy.deepcopy(board)
      next_board[blank[0]][blank[1]] = player_piece
    else:
      next_board = copy.copy(board)
      next_board[blank] = player_piece

    possible_boards.append(next_board)

  return possible_boards


def get_player_piece(player):
  piece = ''
  piece = 'O' if player == -1 else 'X'

  return piece


def build_boards(board, width):
  flat_boards = copy.copy(board)

  for i in range(0, width * width, width):
    row_board = []
    for flat_board in board:
      row = flat_board[i:i + width]
      row_board.append(row)
    row_board = [item for sublist in row_board for item in sublist]
    flat_boards.append(row_board)

  for i in range(width):
    col_board = []
    for flat_board in board:
      col = flat_board[i::width]
      col_board.append(col)
    col_board = [item for sublist in col_board for item in sublist]
    flat_boards.append(col_board)

  diag1_board = []
  diag2_board = []
  for flat_board in board:
    diag1_board.append([flat_board[width * i + i] for i in range(width)])
    diag2_board.append([
      flat_board[width * i + width - i - 1] for i in range(width)
    ])

  diag1_board = [item for sublist in diag1_board for item in sublist]
  diag2_board = [item for sublist in diag2_board for item in sublist]
  flat_boards.append(diag1_board)
  flat_boards.append(diag2_board)

  return flat_boards


def build_board_lanes(board, width):
  rows = [board[i:i + width] for i in range(0, width * width, width)]
  cols = [board[i::width] for i in range(width)]
  diag1 = [[board[width * i + i] for i in range(width)]]
  diag2 = [[board[width * i + width - i - 1] for i in range(width)]]
  lanes = rows + cols + diag1 + diag2
  return lanes


def find_blanks(board, width):
  blank_indicies = []

  if type(board[0]) is list:
    board_length = len(board[0])
    for i in range(width):
      for j in range(board_length):
        if isinstance(board[i][j], int):
          blank_indicies.append([i, j])
  else:
    board_length = len(board)
    for i in range(board_length):
      if isinstance(board[i], int):
        blank_indicies.append(i)

  return blank_indicies
