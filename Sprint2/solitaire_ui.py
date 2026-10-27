import tkinter as tk
from tkinter import messagebox
from board_logic import SolitaireLogic

class SolitaireUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Peg Solitaire - Sprint 2")
        
        self.logic = SolitaireLogic(7, "English")
        self.selected_peg = None

        self.setup_widgets()
        self.redraw_board()

    def setup_widgets(self):
        # Control panel on the left
        control_frame = tk.Frame(self.root, padx=10, pady=10)
        control_frame.pack(side=tk.LEFT, fill=tk.Y)

        tk.Label(control_frame, text="Board Type:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=5)
        self.type_var = tk.StringVar(value="English")
        for t in ["English", "Hexagon", "Diamond"]:
            rb = tk.Radiobutton(control_frame, text=t, variable=self.type_var, value=t)
            rb.pack(anchor=tk.W)

        tk.Label(control_frame, text="Board Size:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(15, 5))
        self.size_var = tk.IntVar(value=7)
        size_entry = tk.Entry(control_frame, textvariable=self.size_var, width=6)
        size_entry.pack(anchor=tk.W)

        new_game_btn = tk.Button(control_frame, text="New Game", command=self.handle_new_game, width=12)
        new_game_btn.pack(anchor=tk.W, pady=20)

        # Canvas on the right for the board
        self.canvas = tk.Canvas(self.root, width=420, height=420, bg="white")
        self.canvas.pack(side=tk.RIGHT, padx=10, pady=10)
        self.canvas.bind("<Button-1>", self.handle_click)

    def handle_new_game(self):
        try:
            sz = self.size_var.get()
            b_type = self.type_var.get()
            if sz < 3 or sz % 2 == 0:
                messagebox.showerror("Error", "Size must be an odd number greater than or equal to 3.")
                return
            
            self.logic = SolitaireLogic(sz, b_type)
            self.selected_peg = None
            self.redraw_board()
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid integer for size.")

    def redraw_board(self):
        self.canvas.delete("all")
        sz = self.logic.size
        cell = min(400 // sz, 50)
        ox = (420 - (sz * cell)) // 2
        oy = (420 - (sz * cell)) // 2

        for r in range(sz):
            for c in range(sz):
                val = self.logic.board[r][c]
                if val == -1:
                    continue

                x1 = ox + c * cell + 3
                y1 = oy + r * cell + 3
                x2 = x1 + cell - 6
                y2 = y1 + cell - 6

                color = "skyblue" if val == 1 else "lightgray"
                outline = "red" if self.selected_peg == (r, c) else "black"
                width = 3 if self.selected_peg == (r, c) else 1

                self.canvas.create_oval(x1, y1, x2, y2, fill=color, outline=outline, width=width)

    def handle_click(self, event):
        sz = self.logic.size
        cell = min(400 // sz, 50)
        ox = (420 - (sz * cell)) // 2
        oy = (420 - (sz * cell)) // 2

        c = (event.x - ox) // cell
        r = (event.y - oy) // cell

        if not (0 <= r < sz and 0 <= c < sz):
            return

        if self.logic.board[r][c] == -1:
            return

        if self.selected_peg is None:
            if self.logic.board[r][c] == 1:
                self.selected_peg = (r, c)
        else:
            p1 = self.selected_peg
            p2 = (r, c)
            success = self.logic.make_move(p1, p2)
            if success:
                self.selected_peg = None
                if self.logic.is_game_over or not self.logic.has_any_moves():
                    self.redraw_board()
                    messagebox.showinfo("Game Over", "No valid moves left!")
                    return
            else:
                # If clicking another peg, change selection
                if self.logic.board[r][c] == 1:
                    self.selected_peg = (r, c)
                else:
                    self.selected_peg = None

        self.redraw_board()

if __name__ == "__main__":
    app_root = tk.Tk()
    ui = SolitaireUI(app_root)
    app_root.mainloop()