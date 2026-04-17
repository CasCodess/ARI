import tkinter as tk
import random
from tictactoe import initial_state, result, minimax, terminal, winner

X = "X"  # Human
O = "O"  # AI
EMPTY = None


class TicTacToeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe AI - Minimax")
        self.root.configure(bg="black")

        # SCOREBOARD
        self.x_score = 0
        self.o_score = 0
        self.draws = 0

        self.board = initial_state()
        self.buttons = [[None for _ in range(3)] for _ in range(3)]

        self.create_ui()
        self.draw_board()

    # ---------------- UI ----------------
    def create_ui(self):

        # SCOREBOARD
        self.score_label = tk.Label(
            self.root,
            text="X: 0   O: 0   Draws: 0",
            font=("Arial", 14, "bold"),
            fg="white",
            bg="black"
        )
        self.score_label.grid(row=0, column=0, columnspan=3)

        # DIFFICULTY MENU (RESTORED)
        self.difficulty = tk.StringVar(value="Impossible")

        diff_frame = tk.Frame(self.root, bg="black")
        diff_frame.grid(row=1, column=0, columnspan=3)

        tk.Label(diff_frame, text="Difficulty:", fg="white", bg="black").pack(side=tk.LEFT)

        tk.OptionMenu(
            diff_frame,
            self.difficulty,
            "Easy",
            "Medium",
            "Impossible"
        ).pack(side=tk.LEFT)

        # BOARD
        board_frame = tk.Frame(self.root, bg="black")
        board_frame.grid(row=2, column=0, columnspan=3)

        for i in range(3):
            for j in range(3):
                btn = tk.Button(
                    board_frame,
                    text="",
                    font=("Arial", 30, "bold"),
                    height=2,
                    width=5,
                    bg="black",
                    fg="white",
                    activebackground="gray20",
                    command=lambda r=i, c=j: self.human_move(r, c)
                )
                btn.grid(row=i, column=j)
                self.buttons[i][j] = btn

        # RESTART BUTTON
        tk.Button(
            self.root,
            text="Restart",
            font=("Arial", 12, "bold"),
            bg="gray20",
            fg="white",
            command=self.restart
        ).grid(row=3, column=0, columnspan=3, pady=10)

    # ---------------- HUMAN MOVE ----------------
    def human_move(self, r, c):

        if self.board[r][c] != EMPTY or terminal(self.board):
            return

        self.animate_click(r, c)

        self.board = result(self.board, (r, c))
        self.draw_board()

        if self.check_game_over():
            return

        self.root.after(250, self.ai_move)

    # ---------------- AI MOVE ----------------
    def ai_move(self):

        if terminal(self.board):
            return

        diff = self.difficulty.get()

        if diff == "Easy":
            move = random.choice(list(self.get_actions()))
        elif diff == "Medium":
            move = minimax(self.board) if random.random() < 0.6 else random.choice(list(self.get_actions()))
        else:
            move = minimax(self.board)

        if move:
            self.board = result(self.board, move)

        self.draw_board()
        self.check_game_over()

    # ---------------- ACTIONS ----------------
    def get_actions(self):
        return {
            (i, j)
            for i in range(3)
            for j in range(3)
            if self.board[i][j] == EMPTY
        }

    # ---------------- DRAW BOARD ----------------
    def draw_board(self):

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
                    self.buttons[i][j]["fg"] = "white"

    # ---------------- CLICK ANIMATION ----------------
    def animate_click(self, r, c):
        btn = self.buttons[r][c]
        original = btn["bg"]

        btn["bg"] = "yellow"
        self.root.update()
        self.root.after(80, lambda: btn.config(bg=original))

    # ---------------- WIN HIGHLIGHT ----------------
    def highlight_winner(self):
        w = winner(self.board)
        if not w:
            return

        lines = [
            [(0,0),(0,1),(0,2)],
            [(1,0),(1,1),(1,2)],
            [(2,0),(2,1),(2,2)],
            [(0,0),(1,0),(2,0)],
            [(0,1),(1,1),(2,1)],
            [(0,2),(1,2),(2,2)],
            [(0,0),(1,1),(2,2)],
            [(0,2),(1,1),(2,0)]
        ]

        for line in lines:
            vals = [self.board[r][c] for r,c in line]
            if vals == [w, w, w]:
                for r,c in line:
                    self.buttons[r][c]["bg"] = "green"

    # ---------------- GAME OVER (NO POPUP NOW) ----------------
    def check_game_over(self):

        if terminal(self.board):

            self.highlight_winner()

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
            self.show_result_on_board(msg)
            return True

        return False

    # ---------------- SHOW RESULT ON BOARD ----------------
    def show_result_on_board(self, msg):

        overlay = tk.Label(
            self.root,
            text=msg,
            font=("Arial", 20, "bold"),
            fg="yellow",
            bg="black"
        )

        overlay.grid(row=4, column=0, columnspan=3)

    # ---------------- SCORE UPDATE ----------------
    def update_score(self):
        self.score_label.config(
            text=f"X: {self.x_score}   O: {self.o_score}   Draws: {self.draws}"
        )

    # ---------------- RESTART ----------------
    def restart(self):
        self.board = initial_state()

        for i in range(3):
            for j in range(3):
                self.buttons[i][j]["bg"] = "black"

        self.draw_board()


# ---------------- RUN ----------------
if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToeGUI(root)
    root.mainloop()