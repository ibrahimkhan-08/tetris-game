import tkinter as tk
import random

# Game settings
CELL_SIZE = 30
WIDTH = 10
HEIGHT = 20

SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[0, 1, 0], [1, 1, 1]],  # T
    [[1, 0, 0], [1, 1, 1]],  # J
    [[0, 0, 1], [1, 1, 1]],  # L
    [[0, 1, 1], [1, 1, 0]],  # S
    [[1, 1, 0], [0, 1, 1]],  # Z
]

COLORS = [
    "cyan", "yellow", "purple",
    "blue", "orange", "green", "red"
]


class Piece:
    def __init__(self):
        i = random.randint(0, len(SHAPES) - 1)
        self.shape = SHAPES[i]
        self.color = COLORS[i]
        self.x = WIDTH // 2 - len(self.shape[0]) // 2
        self.y = 0

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]


class Tetris:
    def __init__(self, root):
        self.root = root
        self.root.title("Tetris")

        self.canvas = tk.Canvas(
            root,
            width=WIDTH * CELL_SIZE,
            height=HEIGHT * CELL_SIZE,
            bg="black"
        )
        self.canvas.pack()

        self.score_label = tk.Label(root, text="Score: 0")
        self.score_label.pack()

        self.grid = [[None for _ in range(WIDTH)] for _ in range(HEIGHT)]

        self.score = 0
        self.current = Piece()

        root.bind("<Left>", self.move_left)
        root.bind("<Right>", self.move_right)
        root.bind("<Down>", self.move_down)
        root.bind("<Up>", self.rotate)

        self.update()

    def valid(self, piece, dx=0, dy=0):
        for y, row in enumerate(piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    nx = piece.x + x + dx
                    ny = piece.y + y + dy

                    if nx < 0 or nx >= WIDTH:
                        return False

                    if ny >= HEIGHT:
                        return False

                    if ny >= 0 and self.grid[ny][nx]:
                        return False
        return True

    def lock_piece(self):
        for y, row in enumerate(self.current.shape):
            for x, cell in enumerate(row):
                if cell:
                    self.grid[self.current.y + y][self.current.x + x] = self.current.color

        self.clear_lines()

        self.current = Piece()

        if not self.valid(self.current):
            self.game_over()

    def clear_lines(self):
        new_grid = []

        cleared = 0

        for row in self.grid:
            if all(row):
                cleared += 1
            else:
                new_grid.append(row)

        while len(new_grid) < HEIGHT:
            new_grid.insert(0, [None for _ in range(WIDTH)])

        self.grid = new_grid

        self.score += cleared * 100
        self.score_label.config(text=f"Score: {self.score}")

    def move_left(self, event=None):
        if self.valid(self.current, dx=-1):
            self.current.x -= 1

    def move_right(self, event=None):
        if self.valid(self.current, dx=1):
            self.current.x += 1

    def move_down(self, event=None):
        if self.valid(self.current, dy=1):
            self.current.y += 1

    def rotate(self, event=None):
        old = [row[:] for row in self.current.shape]
        self.current.rotate()

        if not self.valid(self.current):
            self.current.shape = old

    def draw(self):
        self.canvas.delete("all")

        # Draw fixed blocks
        for y in range(HEIGHT):
            for x in range(WIDTH):
                if self.grid[y][x]:
                    self.draw_cell(x, y, self.grid[y][x])

        # Draw current piece
        for y, row in enumerate(self.current.shape):
            for x, cell in enumerate(row):
                if cell:
                    self.draw_cell(
                        self.current.x + x,
                        self.current.y + y,
                        self.current.color
                    )

    def draw_cell(self, x, y, color):
        self.canvas.create_rectangle(
            x * CELL_SIZE,
            y * CELL_SIZE,
            (x + 1) * CELL_SIZE,
            (y + 1) * CELL_SIZE,
            fill=color,
            outline="white"
        )

    def update(self):
        if self.valid(self.current, dy=1):
            self.current.y += 1
        else:
            self.lock_piece()

        self.draw()
        self.root.after(500, self.update)

    def game_over(self):
        self.canvas.create_text(
            WIDTH * CELL_SIZE // 2,
            HEIGHT * CELL_SIZE // 2,
            text="GAME OVER",
            fill="white",
            font=("Arial", 24)
        )
        return


root = tk.Tk()
game = Tetris(root)
root.mainloop()
