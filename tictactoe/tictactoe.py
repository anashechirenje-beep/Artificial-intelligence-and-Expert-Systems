"""
Tic Tac Toe Player
"""

import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):

    x_count = 0
    o_count = 0

    for row in board:
        for cell in row:
            if cell == X:
                x_count += 1
            elif cell == O:
                o_count += 1

    if x_count == o_count:
        return X
    else:
        return O


def actions(board):

    possible_actions = set()

    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                possible_actions.add((i, j))

    return possible_actions


def result(board, action):

    if action not in actions(board):
        raise Exception("Invalid action")

    new_board = [row.copy() for row in board]

    i, j = action

    current_player = player(board)

    new_board[i][j] = current_player

    return new_board

def winner(board):

    # Checking rows
    for row in board:
        if row[0] == row[1] == row[2] and row[0] is not EMPTY:
            return row[0]

    # Checking columns
    for j in range(3):
        if board[0][j] == board[1][j] == board[2][j] and board[0][j] is not EMPTY:
            return board[0][j]

    # Checking first diagonal
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not EMPTY:
        return board[0][0]

    # Checking second diagonal
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not EMPTY:
        return board[0][2]

    return None


def terminal(board):

    if winner(board) is not None:
        return True

    if len(actions(board)) == 0:
        return True

    return False


def utility(board):

    if winner(board) == X:
        return 1

    elif winner(board) == O:
        return -1

    else:
        return 0



def minimax(board):

    # If the game is over, there is no move to make
    if terminal(board):
        return None

    # Find the highest score that X can achieve
    def max_value(board):

        if terminal(board):
            return utility(board)

        value = -math.inf

        for action in actions(board):
            value = max(
                value,
                min_value(result(board, action))
            )

        return value

    # Find the lowest score that O can achieve
    def min_value(board):

        if terminal(board):
            return utility(board)

        value = math.inf

        for action in actions(board):
            value = min(
                value,
                max_value(result(board, action))
            )

        return value

    # If it is X's turn, choose the move with the highest score
    if player(board) == X:

        best_value = -math.inf
        best_action = None

        for action in actions(board):
            value = min_value(result(board, action))

            if value > best_value:
                best_value = value
                best_action = action

        return best_action

    # If it is O's turn, choose the move with the lowest score
    else:

        best_value = math.inf
        best_action = None

        for action in actions(board):
            value = max_value(result(board, action))

            if value < best_value:
                best_value = value
                best_action = action

        return best_action

