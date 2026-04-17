import math
import copy

X = "X"
O = "O"
EMPTY = None


# -----------------------
# INITIAL STATE
# -----------------------
def initial_state():
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


# -----------------------
# PLAYER
# -----------------------
def player(board):
    count_x = sum(row.count(X) for row in board)
    count_o = sum(row.count(O) for row in board)
    return X if count_x == count_o else O


# -----------------------
# ACTIONS
# -----------------------
def actions(board):
    if terminal(board):
        return set()

    return {
        (i, j)
        for i in range(3)
        for j in range(3)
        if board[i][j] == EMPTY
    }


# -----------------------
# RESULT
# -----------------------
def result(board, action):
    if action not in actions(board):
        raise Exception("Invalid action")

    new_board = copy.deepcopy(board)
    i, j = action
    new_board[i][j] = player(board)
    return new_board


# -----------------------
# WINNER
# -----------------------
def winner(board):
    lines = []

    lines.extend(board)
    lines.extend([[board[r][c] for r in range(3)] for c in range(3)])

    lines.append([board[0][0], board[1][1], board[2][2]])
    lines.append([board[0][2], board[1][1], board[2][0]])

    for line in lines:
        if line == [X, X, X]:
            return X
        if line == [O, O, O]:
            return O

    return None


# -----------------------
# TERMINAL
# -----------------------
def terminal(board):
    if winner(board) is not None:
        return True

    return all(EMPTY not in row for row in board)


# -----------------------
# UTILITY
# -----------------------
def utility(board):
    w = winner(board)

    if w == X:
        return 1
    if w == O:
        return -1
    return 0


# -----------------------
# MINIMAX
# -----------------------
def minimax(board):
    if terminal(board):
        return None

    if player(board) == X:
        best = -math.inf
        move = None

        for action in actions(board):
            value = min_value(result(board, action))
            if value > best:
                best = value
                move = action

        return move

    else:
        best = math.inf
        move = None

        for action in actions(board):
            value = max_value(result(board, action))
            if value < best:
                best = value
                move = action

        return move


# -----------------------
# MAX VALUE
# -----------------------
def max_value(board):
    if terminal(board):
        return utility(board)

    v = -math.inf

    for action in actions(board):
        v = max(v, min_value(result(board, action)))

    return v


# -----------------------
# MIN VALUE
# -----------------------
def min_value(board):
    if terminal(board):
        return utility(board)

    v = math.inf

    for action in actions(board):
        v = min(v, max_value(result(board, action)))

    return v