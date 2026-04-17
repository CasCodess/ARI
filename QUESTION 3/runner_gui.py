import tkinter as tk
import random
from tictactoe import initial_state, result, minimax, terminal, winner

X = "X"   # AI
O = "O"   # Human
EMPTY = None


class TicTacToeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe AI - Minimax")

        self.difficulty = "Impossible"

        self.board = initial_state()
        self.buttons = [[None for _ in range(3)] for _ in range(3)]

        self.create_ui()
        self.draw_board()

    # ---------------- UI ----------------
    def create_ui(self):

        # Top controls
        top = tk.Frame(self.root)
        top.grid(row=0, column=0, columnspan=3)

        tk.Label(top, text="Difficulty:").pack(side=tk.LEFT)

        self.diff_var = tk.StringVar(value="Impossible")
        diff_menu = tk.OptionMenu(top, self.diff_var, "Easy", "Medium", "Impossible")
        diff_menu.pack(side=tk.LEFT)

        tk.Button(top, text="Restart", command=self.restart).pack(side=tk.LEFT)

        # Board buttons
        board_frame = tk.Frame(self.root)
        board_frame.grid(row=1, column=0, columnspan=3)

        for i in range(3):
            for j in range(3):
                btn = tk.Button(
                    board_frame,
                    text="",
                    font=("Arial", 30),
                    height=2,
                    width=5,
                    command=lambda r=i, c=j: self.human_move(r, c)
                )
                btn.grid(row=i, column=j)
                self.buttons[i][j] = btn

    # ---------------- RESET ----------------
    def restart(self):
        self.board = initial_state()
        self.clear_colors()
        self.draw_board()

    # ---------------- HUMAN MOVE ----------------
    def human_move(self, r, c):

        if self.board[r][c] != EMPTY or terminal(self.board):
            return

        self.board = result(self.board, (r, c))
        self.draw_board()

        if self.check_game_over():
            return

        self.root.after(200, self.ai_move)

    # ---------------- AI MOVE ----------------
    def ai_move(self):

        if terminal(self.board):
            return

        difficulty = self.diff_var.get()

        if difficulty == "Easy":
            move = random.choice(list(self.get_actions()))
        elif difficulty == "Medium":
            move = self.medium_ai()
        else:
            move = minimax(self.board)

        if move:
            self.board = result(self.board, move)

        self.draw_board()
        self.check_game_over()

    # ---------------- MEDIUM AI ----------------
    def medium_ai(self):
        # 50% optimal, 50% random
        if random.random() < 0.5:
            return minimax(self.board)
        return random.choice(list(self.get_actions()))

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
                self.buttons[i][j]["text"] = val if val else ""

        self.highlight_winner()

    # ---------------- WIN HIGHLIGHT ----------------
    def highlight_winner(self):

        w = winner(self.board)
        if not w:
            return

        lines = []

        # rows
        for i in range(3):
            lines.append([(i, 0), (i, 1), (i, 2)])

        # cols
        for j in range(3):
            lines.append([(0, j), (1, j), (2, j)])

        # diagonals
        lines.append([(0,0),(1,1),(2,2)])
        lines.append([(0,2),(1,1),(2,0)])

        for line in lines:
            values = [self.board[r][c] for r, c in line]

            if values == [w, w, w]:
                for r, c in line:
                    self.buttons[r][c]["bg"] = "lightgreen"

    # ---------------- CLEAR COLORS ----------------
    def clear_colors(self):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j]["bg"] = "SystemButtonFace"

    # ---------------- GAME OVER ----------------
    def check_game_over(self):

        if terminal(self.board):

            w = winner(self.board)

            if w == X:
                msg = "AI Wins!"
            elif w == O:
                msg = "You Win!"
            else:
                msg = "Tie Game!"

            self.show_popup(msg)
            return True

        return False

    # ---------------- POPUP ----------------
    def show_popup(self, msg):
        popup = tk.Toplevel()
        popup.title("Game Over")

        tk.Label(popup, text=msg, font=("Arial", 18)).pack(padx=20, pady=20)
        tk.Button(popup, text="Close", command=self.restart).pack(pady=10)


# ---------------- RUN ----------------
if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToeGUI(root)
    root.mainloop()