from math import inf as infinity
from random import choice
import random
import platform
import time
from os import system

HUMAN = -1
COMP = +1
n_size = 1
board = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
]

directions = [
    (0, 1),  # right
    (1, 0),  # down
    (1, 1),  # diagonal down-right
    (1, -1),  # diagonal down-left
]


def create_board(n_size):
    global board
    board = [[0 for _ in range(n_size)] for _ in range(n_size)]


def clean():
    """
    Clears the console
    """
    os_name = platform.system().lower()
    if "windows" in os_name:
        system("cls")
    else:
        system("clear")


def render(state, c_choice, h_choice):
    """
    Print the board on console
    :param state: current state of the board
    """

    chars = {-1: h_choice, +1: c_choice, 0: " "}
    str_line = "---------------"

    print("\n" + str_line)
    for row in state:
        for cell in row:
            symbol = chars[cell]
            print(f"| {symbol} |", end="")
        print("\n" + str_line)


def empty_cells(state):
    """
    Each empty cell will be added into cells' list
    :param state: the state of the current board
    :return: a list of empty cells
    """
    cells = []

    for x, row in enumerate(state):
        for y, cell in enumerate(row):
            if cell == 0:
                cells.append([x, y])

    return cells


def valid_move(x, y):
    """
    A move is valid if the chosen cell is empty
    :param x: X coordinate
    :param y: Y coordinate
    :return: True if the board[x][y] is empty
    """
    return board[x][y] == 0


def wins(state, player):
    """
    WIN CONDITION = 5 same symbols in row, column or diagonal
    :param state: the state of the current board
    :param player: a human or a computer
    :return: True if the player wins
    """

    def first_cell(state, player):
        for x, row in enumerate(state):
            for y, cell in enumerate(row):
                if cell == player:
                    return [x, y]
        return [-1, -1]

    first_row, first_col = first_cell(state, player)
    if first_row == -1 or first_col == -1:
        return False

    def check_five(i, j, di, dj):
        start_val = state[i][j]
        if start_val == 0:  # Skip empty cells (optional)
            return False

        for k in range(1, 5):
            ni, nj = i + k * di, j + k * dj
            if not (0 <= ni < n_size and 0 <= nj < n_size):  # Out of bounds
                return False
            if state[ni][nj] != start_val:  # Values must match
                return False
        return True

    for i in range(first_row, n_size):
        for j in range(first_col, n_size):
            for di, dj in directions:
                if check_five(i, j, di, dj):
                    return True
    return False


def game_over(state):
    """
    This function test if the human or computer wins
    :param state: the state of the current board
    :return: True if the human or computer wins
    """
    return wins(state, HUMAN) or wins(state, COMP)


def set_move(x, y, player):
    """
    Set the move on board, if the coordinates are valid
    :param x: X coordinate
    :param y: Y coordinate
    :param player: the current player
    """
    if valid_move(x, y):
        board[x][y] = player
        return True
    else:
        return False


def evaluate(state):
    """
    Function to heuristic evaluation of state.
    :param state: the state of the current board
    :return: +1 if the computer wins; -1 if the human wins; 0 draw
    """
    if wins(state, COMP):
        score = +1
    elif wins(state, HUMAN):
        score = -1
    else:
        score = 0

    return score


def minimax(state, depth, player):
    """
    AI function that choice the best move
    :param state: current state of the board
    :param depth: node index in the tree (0 <= depth <= 9),
    but never nine in this case (see iaturn() function)
    :param player: an human or a computer
    :return: a list with [the best row, best col, best score]
    """
    if player == COMP:
        best = [-1, -1, -infinity]
    else:
        best = [-1, -1, +infinity]

    if depth == 0 or game_over(state):
        score = evaluate(state)
        return [-1, -1, score]

    for cell in empty_cells(state):
        x, y = cell[0], cell[1]
        state[x][y] = player
        score = minimax(state, depth - 1, -player)
        state[x][y] = 0
        score[0], score[1] = x, y

        if player == COMP:
            if score[2] > best[2]:
                best = score  # max value
        else:
            if score[2] < best[2]:
                best = score  # min value

    return best


def ai_turn(c_choice, h_choice):
    """
    :param c_choice: computer's choice X or O
    :param h_choice: human's choice X or O
    :return:
    """
    depth = len(empty_cells(board))
    if depth == 0 or game_over(board):
        return

    clean()
    print(f"Computer turn [{c_choice}]")
    render(board, c_choice, h_choice)

    if depth == n_size * n_size:
        x = random.randint(1, n_size)
        y = random.randint(1, n_size)
    else:
        move = minimax(board, depth, COMP)
        x, y = move[0], move[1]

    set_move(x, y, COMP)
    time.sleep(1)


def human_turn(c_choice, h_choice):
    """
    The Human plays choosing a valid move.
    :param c_choice: computer's choice X or O
    :param h_choice: human's choice X or O
    :return:
    """
    depth = len(empty_cells(board))
    if depth == 0 or game_over(board):
        return

    clean()
    print(f"Human turn [{h_choice}]")
    render(board, c_choice, h_choice)

    move_x = 0
    move_y = 0
    while move_x < 1 or move_x > n_size or move_y < 1 or move_y > n_size:
        try:
            move_x = int(input("Use numpad (x, y) \n x = : "))
            move_y = int(input("\n y = : "))
            can_move = set_move(move_x - 1, move_y - 1, HUMAN)

            if not can_move:
                print("Bad move")
                move_x = 0
                move_y = 0
        except (EOFError, KeyboardInterrupt):
            print("Bye")
            exit()
        except (KeyError, ValueError):
            print("Bad choice")


def main():
    clean()
    global n_size
    h_choice = ""  # X or O
    c_choice = ""  # X or O
    first = ""  # if human is the first
    print("Bài tập LAB 4 - CARO 5 ô")
    # Chọn kích thước bảng
    while n_size < 5 or n_size > 20:
        try:
            print("")
            n_size = int(input("Kích thước bảng (5 - 20) \nChọn: "))
        except (EOFError, KeyboardInterrupt):
            print("Bye")
            exit()
        except (KeyError, ValueError):
            print("Bad choice")

    create_board(n_size)

    # Human chooses X or O to play
    while h_choice != "O" and h_choice != "X":
        try:
            print("")
            h_choice = input("Choose X or O\nChosen: ").upper()
        except (EOFError, KeyboardInterrupt):
            print("Bye")
            exit()
        except (KeyError, ValueError):
            print("Bad choice")

    # Setting computer's choice
    if h_choice == "X":
        c_choice = "O"
    else:
        c_choice = "X"

    # Human may starts first
    clean()
    while first != "Y" and first != "N":
        try:
            first = input("First to start?[y/n]: ").upper()
        except (EOFError, KeyboardInterrupt):
            print("Bye")
            exit()
        except (KeyError, ValueError):
            print("Bad choice")

    # Main loop of this game
    while len(empty_cells(board)) > 0 and not game_over(board):
        if first == "N":
            ai_turn(c_choice, h_choice)
            first = ""

        human_turn(c_choice, h_choice)
        ai_turn(c_choice, h_choice)

    # Game over message
    if wins(board, HUMAN):
        clean()
        print(f"Human turn [{h_choice}]")
        render(board, c_choice, h_choice)
        print("YOU WIN!")
    elif wins(board, COMP):
        clean()
        print(f"Computer turn [{c_choice}]")
        render(board, c_choice, h_choice)
        print("YOU LOSE!")
    else:
        clean()
        render(board, c_choice, h_choice)
        print("DRAW!")

    exit()


if __name__ == "__main__":
    main()
