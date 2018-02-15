import boardstupid as game
import copy
import random


def main():
  board = [1, 2, 3, 4, 5, 6, 7, 8, 9]
  width = 3
  result = None
  human_player = -1
  ai_player = 1

  num_players = prompt_num_players()
  is_human_turn = get_first_player()
  print_game_intro(is_human_turn)

  while result == None:
    print_board(board, width)
    if is_human_turn or num_players == 2:
      if num_players == 2:
        if human_player == -1:
          human_player = 1
        else:
          human_player = -1
      human_turn(board, human_player)
      result = game.get_utility(board, width, human_player)
    else:
      ai_turn(board)
      result = game.get_utility(board, width, ai_player)
    is_human_turn = not is_human_turn

  print_board(board, width)
  print_result(result)


def prompt_num_players():
  num_players = int(input("1 or 2  players? \n"))
  return num_players


def print_game_intro(is_human_turn):
  print()
  print("Welcome to tic-tac-toe!")
  if is_human_turn:
    print("You get to go first!")
  else:
    print("The computer will go first")

  print()


def print_board(board, width):
  for i in range(width):
    for j in range(width):
      print(board[i * width + j], end=' ')
    print()


def print_result(result):
  print()
  if result == 1:
    print("X won the game!")
  elif result == -1:
    print("O won the game!")
  else:
    print("It was a tie game")


def print_human_prompt():
  print()
  pos = int(input("Where would you like to move? \n"))
  return pos


def print_ai_move(position):
  print()
  print("AI chooses spot:", position)


def get_first_player():
  player = random.randint(0, 1)
  if player == 0:
    return True

  return False


def human_turn(board, human_player):
  pos = print_human_prompt()
  human_player_piece = game.get_player_piece(human_player)
  board[pos - 1] = human_player_piece


def ai_turn(board):
  for i in range(len(board)):
    if isinstance(board[i], int):
      print_ai_move(i + 1)
      board[i] = 'X'
      return

if __name__ == "__main__":
  main()
