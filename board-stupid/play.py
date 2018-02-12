import random


def main():
  board = [1, 2, 3, 4, 5, 6, 7, 8, 9]
  width = 3
  result = None

  is_human_turn = get_first_player()
  print_game_intro(is_human_turn)

  while result == None:
    print_board(board, width)
    if is_human_turn:
      human_turn(board)
    else:
      ai_turn(board)
    is_human_turn = not is_human_turn
    result = get_game_result(board, width)

  print_board(board, width)
  print_result(result)


def get_first_player():
  player = random.randint(0, 1)
  if player == 0:
    return True

  return False


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


def human_turn(board):
  print()
  pos = int(input("Where would you like to move?"))
  board[pos - 1] = 'O'


def ai_turn(board):
  for i in range(len(board)):
    if isinstance(board[i], int):
      print()
      print("AI chooses spot:", i + 1)
      board[i] = 'X'
      return


def get_game_result(board, width):
  utility = get_utility(board, width)
  if utility:
    return utility
  elif check_full(board):
    return 0

  return None


def get_utility(board, width):
  lanes = build_lanes(width)
  for lane in lanes:
    if board[lane[0]] == board[lane[1]] == board[lane[2]]:
      if board[lane[0]] == 'O':
        return -1
      else:
        return 1

  return 0


def build_lanes(width):
  return [[0, 1, 2], [3, 4, 5], [6, 7, 8],
          [0, 3, 6], [1, 4, 7], [2, 5, 8],
          [0, 4, 8], [2, 4, 6]
         ]


def check_full(board):
  for i in range(len(board)):
    if isinstance(board[i], int):
      return False

  return True


if __name__ == "__main__":
  main()
