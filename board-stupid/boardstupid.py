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




# determines whether the game is a terminal state
#   if so, determines which player wins
# return:
#   0 for tie
#   1 for MAX wins
#   -1 for MIN wins
#   None otherwise
def get_utility(board, width):


# ------------------- HELPER FUNCTIONS ----------------------------------------
# def is_terminal_state(board, width):
#   return True/False
#
# def find_possible_moves(board, width, player):
#
