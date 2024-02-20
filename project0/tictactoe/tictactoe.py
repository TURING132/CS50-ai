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
    """
    Returns player who has the next turn on a board.
    """
    o_count = sum(row.count(O) for row in board)
    x_count = sum(row.count(X) for row in board)
    return X if x_count <= o_count else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    positions = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                positions.append((i, j))
    return positions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if board[action[0]][action[1]] != EMPTY:
        raise Exception
    updated_board = [row[:] for row in board]
    updated_board[action[0]][action[1]] = player(board)
    return updated_board


def win(flag, board):
    if flag == board[0][0] == board[0][1] == board[0][2] \
            or flag == board[1][0] == board[1][1] == board[1][2] \
            or flag == board[2][0] == board[2][1] == board[2][2] \
            or flag == board[0][0] == board[1][0] == board[2][0] \
            or flag == board[0][1] == board[1][1] == board[2][1] \
            or flag == board[0][2] == board[1][2] == board[2][2] \
            or flag == board[0][0] == board[1][1] == board[2][2] \
            or flag == board[2][0] == board[1][1] == board[0][2]:
        return True
    else:
        return False


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    if win(X, board):
        return X
    elif win(O, board):
        return O
    else:
        return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None:
        return True
    if sum(row.count(EMPTY) for row in board) == 0:
        return True
    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if X == winner(board):
        return 1
    if O == winner(board):
        return -1
    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    if player(board) == X:
        value, move = max_value(board)
        return move
    else:
        value, move = min_value(board)
        return move


def max_value(board):
    move = None
    if terminal(board):
        return utility(board), move
    v = float("-inf")
    for action in actions(board):
        temp, act = min_value(result(board, action))
        if temp > v:
            v = temp
            move = action
    return v, move


def min_value(board):
    move = None
    if terminal(board):
        return utility(board), move
    v = float("inf")
    for action in actions(board):
        temp, act = max_value(result(board, action))
        if temp < v:
            v = temp
            move = action
    return v, move
