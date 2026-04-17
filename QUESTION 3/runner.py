from tictactoe import initial_state, minimax, result


def print_board(board):
    for row in board:
        print(row)
    print()


def main():
    board = initial_state()

    print("Initial Board:")
    print_board(board)

    while True:

        if minimax(board) is None:
            break

        move = minimax(board)
        board = result(board, move)

        print("AI Move:", move)
        print_board(board)

        if minimax(board) is None:
            break


if __name__ == "__main__":
    main()