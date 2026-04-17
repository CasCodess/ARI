import tkinter as tk
import random
from tictactoe import initial_state, result, minimax, terminal, winner

X = "X"
O = "O"
EMPTY = None


class TicTacToeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe AI")
        self.root.configure(bg="black")

        self.difficulty = tk.StringVar(value="Impossible")

        self.board = None
        self.buttons = None

        self.x_score = 0
        self.o_score = 0
        self.draws = 0

        self.show_menu()

    # ---------------- MENU SCREEN ----------------
    def show_menu(self):

        self.clear_screen()

        tk.Label(
            self.root,
            text="TIC TAC TOE AI",
            font=("Arial", 24, "bold"),
            fg="white",
            bg="black"
        ).pack(pady=20)

        tk.Label(self.root, text="Select Difficulty:", fg="white", bg="black").pack()

        tk.OptionMenu(
            self.root,
            self.difficulty,
            "Easy",
            "Medium",
            "Impossible"
        ).pack(pady=10)

        tk.Button(
            self.root,
            text="Start Game",
            font=("Arial", 16, "bold"),
            bg="green",
            fg="white",
            command=self.start_game
        ).pack(pady=10)

        tk.Button(
            self.root,
            text="Quit",
            font=("Arial", 14),
            bg="red",
            fg="white",
            command=self.root.destroy
        ).pack(pady=10)

    # ---------------- START GAME ----------------
    def start_game(self):
        self.board = initial_state()
        self.show_game()

    # ---------------- GAME SCREEN ----------------
    def show_game(self):

        self.clear_screen()

        self.buttons = [[None for _ in range(3)] for _ in range(3)]

        # SCOREBOARD
        self.score_label = tk.Label(
            self.root,
            text="X: 0   O: 0   Draws: 0",
            font=("Arial", 14, "bold"),
            fg="white",
            bg="black"
        )
        self.score_label.grid(row=0, column=0, columnspan=3)

        # BOARD
        frame = tk.Frame(self.root, bg="black")
        frame.grid(row=1, column=0, columnspan=3)

        for i in range(3):
            for j in range(3):
                btn = tk.Button(
                    frame,
                    text="",
                    font=("Arial", 30, "bold"),
                    height=2,
                    width=5,
                    bg="black",
                    fg="white",
                    command=lambda r=i, c=j: self.human_move(r, c)
                )
                btn.grid(row=i, column=j)
                self.buttons[i][j] = btn

        tk.Button(
            self.root,
            text="Back to Menu",
            bg="gray",
            fg="white",
            command=self.show_menu
        ).grid(row=2, column=0, columnspan=3, pady=10)

    # ---------------- HUMAN MOVE ----------------
    def human_move(self, r, c):

        if self.board[r][c] != EMPTY or terminal(self.board):
            return

        self.board = result(self.board, (r, c))
        self.draw()

        if self.check_game_over():
            return

        self.root.after(200, self.ai_move)

    # ---------------- AI MOVE ----------------
    def ai_move(self):

        if terminal(self.board):
            return

        diff = self.difficulty.get()

        if diff == "Easy":
            move = random.choice(list(self.actions()))
        elif diff == "Medium":
            move = minimax(self.board) if random.random() < 0.6 else random.choice(list(self.actions()))
        else:
            move = minimax(self.board)

        if move:
            self.board = result(self.board, move)

        self.draw()
        self.check_game_over()

    # ---------------- ACTIONS ----------------
    def actions(self):
        return {
            (i, j)
            for i in range(3)
            for j in range(3)
            if self.board[i][j] == EMPTY
        }

    # ---------------- DRAW ----------------
    def draw(self):

        for i in range(3):
            for j in range(3):
                val = self.board[i][j]

                if val == X:
                    self.buttons[i][j]["text"] = "X"
                    self.buttons[i][j]["fg"] = "red"

                elif val == O:
                    self.buttons[i][j]["text"] = "O"
                    self.buttons[i][j]["fg"] = "blue"

                else:
                    self.buttons[i][j]["text"] = ""

    # ---------------- GAME OVER ----------------
    def check_game_over(self):

        if terminal(self.board):

            w = winner(self.board)

            if w == X:
                self.x_score += 1
                msg = "You Win!"
            elif w == O:
                self.o_score += 1
                msg = "AI Wins!"
            else:
                self.draws += 1
                msg = "Draw!"

            self.update_score()
            self.show_result(msg)
            return True

        return False

    # ---------------- SCORE ----------------
    def update_score(self):
        self.score_label.config(
            text=f"X: {self.x_score}   O: {self.o_score}   Draws: {self.draws}"
        )

    # ---------------- RESULT ON BOARD ----------------
    def show_result(self, msg):
        tk.Label(
            self.root,
            text=msg,
            font=("Arial", 18, "bold"),
            fg="yellow",
            bg="black"
        ).grid(row=3, column=0, columnspan=3)

    # ---------------- SCREEN RESET ----------------
    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()


# ---------------- RUN APP ----------------
if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToeApp(root)
    root.mainloop()