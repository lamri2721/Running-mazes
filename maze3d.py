import tkinter as tk
import random


ROWS = 15
COLS = 20
CELL = 28
MARGIN = 20

GEN_SPEED = 10
SOLVE_SPEED = 20



class Maze:
    def __init__(self, r, c):
        self.R = r
        self.C = c

        self.northWall = [[True] * c for _ in range(r)]
        self.eastWall = [[True] * c for _ in range(r)]
        self.visited = [[False] * c for _ in range(r)]

    def in_bounds(self, r, c):
        return 0 <= r < self.R and 0 <= c < self.C

    def neighbors(self, r, c):
        for dr, dc in [(1,0), (-1,0), (0,1), (0,-1)]:
            nr, nc = r + dr, c + dc
            if self.in_bounds(nr, nc):
                yield nr, nc

    def remove_wall(self, r1, c1, r2, c2):
        if r2 == r1 + 1:
            self.northWall[r1][c1] = False
        elif r2 == r1 - 1:
            self.northWall[r2][c2] = False
        elif c2 == c1 + 1:
            self.eastWall[r1][c1] = False
        elif c2 == c1 - 1:
            self.eastWall[r1][c2] = False

    def has_wall(self, r1, c1, r2, c2):
        if r2 == r1 + 1:
            return self.northWall[r1][c1]
        if r2 == r1 - 1:
            return self.northWall[r2][c2]
        if c2 == c1 + 1:
            return self.eastWall[r1][c1]
        if c2 == c1 - 1:
            return self.eastWall[r1][c2]
        return True


#  APP 
class MazeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("✨ Beautiful Maze Generator & Solver")

        self.canvas = tk.Canvas(
            root,
            width=COLS * CELL + 2 * MARGIN,
            height=ROWS * CELL + 2 * MARGIN,
            bg="#0f172a"
        )
        self.canvas.pack()

        btn_frame = tk.Frame(root, bg="#0f172a")
        btn_frame.pack()

        tk.Button(btn_frame, text="Generate", command=self.generate,
                  bg="#22c55e", fg="white", width=12).pack(side="left", padx=5)

        tk.Button(btn_frame, text="Solve", command=self.solve,
                  bg="#3b82f6", fg="white", width=12).pack(side="left", padx=5)

        self.maze = Maze(ROWS, COLS)

        self.gen_stack = []
        self.solve_stack = []

        self.start = (0, 0)
        self.end = (ROWS - 1, COLS - 1)

        self.draw_grid()

    # DRAW 
    def xy(self, r, c):
        x = MARGIN + c * CELL
        y = MARGIN + r * CELL
        return x, y

    def draw_cell(self, r, c, color):
        x, y = self.xy(r, c)
        self.canvas.create_rectangle(
            x+2, y+2,
            x+CELL-2, y+CELL-2,
            fill=color,
            outline=""
        )

    def draw_grid(self):
        self.canvas.delete("all")
        m = self.maze

        for r in range(ROWS):
            for c in range(COLS):
                x, y = self.xy(r, c)

                if m.northWall[r][c]:
                    self.canvas.create_line(x, y, x+CELL, y, fill="#94a3b8")

                if m.eastWall[r][c]:
                    self.canvas.create_line(x+CELL, y, x+CELL, y+CELL, fill="#94a3b8")

        self.canvas.create_rectangle(
            MARGIN, MARGIN,
            MARGIN + COLS * CELL,
            MARGIN + ROWS * CELL,
            outline="#94a3b8"
        )

    #  GENERATE 
    def generate(self):
        self.maze = Maze(ROWS, COLS)

        start = (random.randint(0, ROWS-1), random.randint(0, COLS-1))
        self.maze.visited[start[0]][start[1]] = True
        self.gen_stack = [start]

        self._gen_step()

    def _gen_step(self):
        if not self.gen_stack:
            self.draw_grid()
            return

        r, c = self.gen_stack[-1]

        self.draw_cell(r, c, "#1e293b")  # current (dark blue)

        options = []
        for nr, nc in self.maze.neighbors(r, c):
            if not self.maze.visited[nr][nc]:
                options.append((nr, nc))

        if options:
            nr, nc = random.choice(options)

            self.maze.remove_wall(r, c, nr, nc)
            self.maze.visited[nr][nc] = True

            self.draw_cell(nr, nc, "#22c55e")  # green expansion

            self.gen_stack.append((nr, nc))
        else:
            self.draw_cell(r, c, "#0f172a")  # backtrack
            self.gen_stack.pop()

        self.root.after(GEN_SPEED, self._gen_step)

    #  SOLVE 
    def solve(self):
        self.solve_stack = [self.start]
        self.visited = set([self.start])
        self._solve_step()

    def _solve_step(self):
        if not self.solve_stack:
            return

        r, c = self.solve_stack[-1]

        self.draw_cell(r, c, "#facc15")  # yellow path

        if (r, c) == self.end:
            for pr, pc in self.solve_stack:
                self.draw_cell(pr, pc, "#00f5d4")  # final cyan path
            return

        moves = []
        for nr, nc in self.maze.neighbors(r, c):
            if (nr, nc) not in self.visited:
                if not self.maze.has_wall(r, c, nr, nc):
                    moves.append((nr, nc))

        if moves:
            nr, nc = random.choice(moves)
            self.solve_stack.append((nr, nc))
            self.visited.add((nr, nc))
            self.draw_cell(nr, nc, "#38bdf8")  # blue move
        else:
            self.draw_cell(r, c, "#ef4444")  # red dead end
            self.solve_stack.pop()

        self.root.after(SOLVE_SPEED, self._solve_step)


# RUN 
root = tk.Tk()
app = MazeApp(root)
root.mainloop()
