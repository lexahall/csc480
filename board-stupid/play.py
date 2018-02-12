import random


def main():
  board = [1, 2, 3, 4, 5, 6, 7, 8, 9]
  width = 3
  result = None
  human_player = 'O'

  num_players = prompt_num_players()
  is_human_turn = get_first_player()
  print_game_intro(is_human_turn)

  while result == None:
    print_board(board, width)
    if is_human_turn or num_players == 2:
      if num_players == 2:
        if human_player == 'O':
          human_player = 'X'
        else:
          human_player = 'O'
      human_turn(board, human_player)
    else:
      ai_turn(board)
    is_human_turn = not is_human_turn
    result = get_utility(board, width, 'X')

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
  board[pos - 1] = human_player


def ai_turn(board):
  for i in range(len(board)):
    if isinstance(board[i], int):
      print_ai_move(i + 1)
      board[i] = 'X'
      return


def get_utility(board, width, player):
  result = get_result(board, width)
  blank_indicies = find_blanks(board)
  num_blanks = len(blank_indicies)
  if is_terminal(result, board, width, player, num_blanks, blank_indicies):
    return result

  return None


def is_terminal(result, board, width, player, num_blanks, blank_indicies):
  return (
    result
    or num_blanks == 0
    or is_tie_board(board, width, player, num_blanks, blank_indicies)
  )


def is_tie_board(board, width, player, num_blanks, blank_indicies):
  if num_blanks > 1:
    return False

  board[blank_indicies[0]] = player
  if get_result(board, width):
    return False

  return True


def get_result(board, width):
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


def find_blanks(board):
  blank_indicies = []
  for i in range(len(board)):
    if isinstance(board[i], int):
      blank_indicies.append(i)

  return blank_indicies


if __name__ == "__main__":
  main()
