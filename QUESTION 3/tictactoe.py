import math
import copy

X = "X"
O = "O"
EMPTY = None


# -----------------------
# INITIAL STATE (optional helper)
# -----------------------
def initial_state():
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


# -----------------------
# PLAYER FUNCTION
# -----------------------
def player(board):
    count_x = sum(row.count(X) for row in board)
    count_o = sum(row.count(O) for row in board)

    return X if count_x == count_o else O


# -----------------------
# ACTIONS FUNCTION
# -----------------------
def actions(board):
    if terminal(board):
        return set()

    result = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                result.add((i, j))
    return result


# -----------------------
# RESULT FUNCTION
# -----------------------
def result(board, action):
    if action not in actions(board):
        raise Exception("Invalid action")

    new_board = copy.deepcopy(board)
    i, j = action

    new_board[i][j] = player(board)
    return new_board


# -----------------------
# WINNER FUNCTION
# -----------------------
def winner(board):

    lines = []

    # rows
    lines.extend(board)

    # columns
    lines.extend([[board[r][c] for r in range(3)] for c in range(3)])

    # diagonals
    lines.append([board[0][0], board[1][1], board[2][2]])
    lines.append([board[0][2], board[1][1], board[2][0]])

    for line in lines:
        if line == [X, X, X]:
            return X
        if line == [O, O, O]:
            return O

    return None


# -----------------------
# TERMINAL FUNCTION
# -----------------------
def terminal(board):
    if winner(board) is not None:
        return True

    for row in board:
        if EMPTY in row:
            return False

    return True


# -----------------------
# UTILITY FUNCTION
# -----------------------
def utility(board):
    w = winner(board)

    if w == X:
        return 1
    if w == O:
        return -1
    return 0


# -----------------------
# MINIMAX ALGORITHM
# -----------------------
def minimax(board):

    if terminal(board):
        return None

    current_player = player(board)

    if current_player == X:
        best_value = -math.inf
        best_move = None

        for action in actions(board):
            value = min_value(result(board, action))
            if value > best_value:
                best_value = value
                best_move = action

        return best_move

    else:
        best_value = math.inf
        best_move = None

        for action in actions(board):
            value = max_value(result(board, action))
            if value < best_value:
                best_value = value
                best_move = action

        return best_move


# -----------------------
# MIN VALUE (O)
# -----------------------
def min_value(board):

    if terminal(board):
        return utility(board)

    v = math.inf

    for action in actions(board):
        v = min(v, max_value(result(board, action)))

    return v


# -----------------------
# MAX VALUE (X)
# -----------------------
def max_value(board):

    if terminal(board):
        return utility(board)

    v = -math.inf

    for action in actions(board):
        v = max(v, min_value(result(board, action)))

    return v