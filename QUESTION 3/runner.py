from tictactoe import initial_state, minimax, result


# -----------------------
# PRINT BOARD
# -----------------------
def print_board(board):
    for row in board:
        print(row)
    print()


# -----------------------
# MAIN GAME LOOP
# -----------------------
def main():
    board = initial_state()

    print("Tic Tac Toe - Human (O) vs AI (X)")
    print_board(board)

    while True:

        # AI turn (X)
        if not terminal(board):
            ai_move = minimax(board)
            board = result(board, ai_move)
            print("AI plays:", ai_move)
            print_board(board)

        if terminal(board):
            break

        # Human turn (O)
        print("Your turn (row col): ")
        r, c = map(int, input().split())

        board = result(board, (r, c))
        print_board(board)

        if terminal(board):
            break


# helper import fix (so it runs cleanly)
from tictactoe import terminal


if __name__ == "__main__":
    main()