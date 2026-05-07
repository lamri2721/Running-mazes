# Maze wall data structures 
import tkinter as tk
import random
import time
from collections import deque

#  Configuration 
ROWS        = 15          # number of maze rows
COLS        = 20          # number of maze columns
CELL_SIZE   = 40          # pixels per cell
MARGIN      = 20          # canvas margin
WALL_WIDTH  = 3           # wall stroke width
GEN_DELAY   = 15          # ms between generation steps (lower = faster)
SOLVE_DELAY = 30          # ms between solver steps
EXTRA_WALL  = True        # bonus: eat 1-in-20 extra walls to create cycles


#  Coordinate helpers
def cell_px(r, c):
    """Top-left pixel corner of cell (r, c).  Row 0 is at the BOTTOM."""
    x = MARGIN + c * CELL_SIZE
    y = MARGIN + (ROWS - 1 - r) * CELL_SIZE
    return x, y


# Maze class 
class Maze:
    def __init__(self, rows, cols):
        self.R = rows
        self.C = cols
        # All walls start intact (True)
        self.northWall = [[True] * cols for _ in range(rows)]
        self.eastWall  = [[True] * cols for _ in range(rows)]
        self.visited   = [[False] * cols for _ in range(rows)]

    # Wall helpers 
    def remove_wall(self, r1, c1, r2, c2):
        """Remove the wall between adjacent cells (r1,c1) and (r2,c2)."""
        if r2 == r1 + 1:                    # r2 is north of r1
            self.northWall[r1][c1] = False
        elif r2 == r1 - 1:                  # r2 is south of r1
            self.northWall[r2][c2] = False
        elif c2 == c1 + 1:                  # r2 is east of r1
            self.eastWall[r1][c1] = False
        elif c2 == c1 - 1:                  # r2 is west of r1
            self.eastWall[r1][c2] = False

    def has_wall(self, r1, c1, r2, c2):
        """Return True if there is a wall between (r1,c1) and (r2,c2)."""
        if r2 == r1 + 1:
            return self.northWall[r1][c1]
        elif r2 == r1 - 1:
            return self.northWall[r2][c2]
        elif c2 == c1 + 1:
            return self.eastWall[r1][c1]
        elif c2 == c1 - 1:
            return self.eastWall[r1][c2]
        return True

    def neighbors(self, r, c):
        """Return valid (in-bounds) neighbors of (r, c)."""
        result = []
        for dr, dc in [(1,0),(-1,0),(0,1),(0,-1)]:
            nr, nc = r+dr, c+dc
            if 0 <= nr < self.R and 0 <= nc < self.C:
                result.append((nr, nc))
        return result

    def unvisited_neighbors(self, r, c):
        return [(nr, nc) for nr, nc in self.neighbors(r, c)
                if not self.visited[nr][nc]]


# GUI / App 
class MazeApp:
    def __init__(self, master):
        self.master = master
        master.title("Maze Generator & Solver")
        master.resizable(False, False)

        canvas_w = 2 * MARGIN + COLS * CELL_SIZE
        canvas_h = 2 * MARGIN + ROWS * CELL_SIZE

        self.canvas = tk.Canvas(master, width=canvas_w, height=canvas_h, bg="#1a1a2e")
        self.canvas.pack(padx=10, pady=10)

        btn_frame = tk.Frame(master, bg="#1a1a2e")
        btn_frame.pack(pady=(0, 10))

        style = dict(bg="#e94560", fg="white", font=("Courier", 12, "bold"),
                     relief="flat", padx=16, pady=6, cursor="hand2")
        self.gen_btn  = tk.Button(btn_frame, text="▶  Generate", command=self.start_generation, **style)
        self.gen_btn.pack(side="left", padx=6)
        self.solve_btn = tk.Button(btn_frame, text="⚡  Solve",    command=self.start_solve,
                                   state="disabled", **style)
        self.solve_btn.pack(side="left", padx=6)
        self.reset_btn = tk.Button(btn_frame, text="↺  Reset",    command=self.reset, **style)
        self.reset_btn.pack(side="left", padx=6)

        self.status = tk.Label(master, text="Press Generate to build a maze.",
                               bg="#1a1a2e", fg="#a8dadc", font=("Courier", 11))
        self.status.pack(pady=(0, 8))

        self.maze   = None
        self.start  = None
        self.end    = None
        self._job   = None

    # Drawing
    def draw_grid(self):
        """Draw all walls of the current maze state."""
        self.canvas.delete("wall")
        m = self.maze
        color = "#4fc3f7"

        for r in range(m.R):
            for c in range(m.C):
                x, y = cell_px(r, c)
                # North wall
                if m.northWall[r][c]:
                    self.canvas.create_line(x, y, x + CELL_SIZE, y,
                                            fill=color, width=WALL_WIDTH, tags="wall")
                # East wall
                if m.eastWall[r][c]:
                    self.canvas.create_line(x + CELL_SIZE, y, x + CELL_SIZE, y + CELL_SIZE,
                                            fill=color, width=WALL_WIDTH, tags="wall")

        # Outer border
        ox, oy = MARGIN, MARGIN
        bw = COLS * CELL_SIZE
        bh = ROWS * CELL_SIZE
        self.canvas.create_rectangle(ox, oy, ox+bw, oy+bh,
                                     outline=color, width=WALL_WIDTH, tags="wall")

    def draw_cell_fill(self, r, c, color, tag="fill"):
        x, y = cell_px(r, c)
        pad = 4
        self.canvas.create_rectangle(x+pad, y+pad, x+CELL_SIZE-pad, y+CELL_SIZE-pad,
                                     fill=color, outline="", tags=tag)

    def draw_dot(self, r, c, color, tag="dot"):
        x, y = cell_px(r, c)
        cx = x + CELL_SIZE // 2
        cy = y + CELL_SIZE // 2
        rad = CELL_SIZE // 4
        self.canvas.create_oval(cx-rad, cy-rad, cx+rad, cy+rad,
                                fill=color, outline="", tags=tag)

    def draw_openings(self):
        """Draw the start (green) and end (orange) openings."""
        sr, sc = self.start
        er, ec = self.end
        self.draw_cell_fill(sr, sc, "#00e676", tag="opening")
        self.draw_cell_fill(er, ec, "#ff6d00", tag="opening")
        # Erase the outer wall for start/end
        self.open_border(sr, sc)
        self.open_border(er, ec)

    def open_border(self, r, c):
        """Visually erase one outer border segment next to a border cell."""
        # We don't need to touch northWall/eastWall; just overdraw with bg
        bg = "#1a1a2e"
        if r == 0:           # south edge → erase bottom of cell
            x, y = cell_px(r, c)
            self.canvas.create_line(x+1, y+CELL_SIZE, x+CELL_SIZE-1, y+CELL_SIZE,
                                    fill=bg, width=WALL_WIDTH+1, tags="wall")
        elif r == ROWS-1:    # north edge → erase top of cell
            x, y = cell_px(r, c)
            self.canvas.create_line(x+1, y, x+CELL_SIZE-1, y,
                                    fill=bg, width=WALL_WIDTH+1, tags="wall")
        if c == 0:           # west edge → erase left of cell
            x, y = cell_px(r, c)
            self.canvas.create_line(x, y+1, x, y+CELL_SIZE-1,
                                    fill=bg, width=WALL_WIDTH+1, tags="wall")
        elif c == COLS-1:    # east edge → erase right of cell
            x, y = cell_px(r, c)
            self.canvas.create_line(x+CELL_SIZE, y+1, x+CELL_SIZE, y+CELL_SIZE-1,
                                    fill=bg, width=WALL_WIDTH+1, tags="wall")

    # Generation 
    def start_generation(self):
        if self._job:
            self.master.after_cancel(self._job)
        self.canvas.delete("all")
        self.gen_btn.config(state="disabled")
        self.solve_btn.config(state="disabled")

        self.maze = Maze(ROWS, COLS)
        self.draw_grid()
        self.status.config(text="Generating maze…")

        # Start mouse at a random cell
        start_r = random.randint(0, ROWS-1)
        start_c = random.randint(0, COLS-1)
        self.maze.visited[start_r][start_c] = True

        # Stack holds (row, col) of cells with unvisited neighbours
        stack = [(start_r, start_c)]
        self._gen_stack = stack
        self._gen_mouse = (start_r, start_c)
        self._step_generate()

    def _step_generate(self):
        stack = self._gen_stack
        m = self.maze

        if not stack:
            # Generation complete
            self.status.config(text="Maze ready! Choose start/end and solve.")
            self._pick_start_end()
            self.draw_openings()
            self.gen_btn.config(state="normal")
            self.solve_btn.config(state="normal")
            return

        r, c = stack[-1]
        unvisited = m.unvisited_neighbors(r, c)

        # Show mouse position
        self.canvas.delete("mouse")
        self.draw_dot(r, c, "#76ff03", tag="mouse")

        if unvisited:
            nr, nc = random.choice(unvisited)
            m.remove_wall(r, c, nr, nc)
            m.visited[nr][nc] = True
            stack.append((nr, nc))

            # Bonus: 1-in-20 chance eat one extra random wall (creates cycles)
            if EXTRA_WALL and random.random() < 0.05:
                all_nbrs = m.neighbors(nr, nc)
                random.shuffle(all_nbrs)
                for xr, xc in all_nbrs:
                    if m.has_wall(nr, nc, xr, xc):
                        m.remove_wall(nr, nc, xr, xc)
                        break

            self.draw_grid()
            self.draw_dot(r, c, "#76ff03", tag="mouse")
        else:
            stack.pop()

        self._job = self.master.after(GEN_DELAY, self._step_generate)

    def _pick_start_end(self):
        """Pick start on the left edge, end on the right edge."""
        sr = random.randint(0, ROWS-1)
        er = random.randint(0, ROWS-1)
        self.start = (sr, 0)
        self.end   = (er, COLS-1)

    # Solver 
    def start_solve(self):
        if self._job:
            self.master.after_cancel(self._job)
        self.canvas.delete("fill")
        self.canvas.delete("dot")
        self.canvas.delete("mouse")
        self.solve_btn.config(state="disabled")
        self.status.config(text="Solving…")

        sr, sc = self.start
        er, ec = self.end

        self._solve_stack    = [(sr, sc)]
        self._solve_visited  = {(sr, sc)}
        self._solve_target   = (er, ec)
        self.draw_openings()
        self._step_solve()

    def _step_solve(self):
        stack  = self._solve_stack
        target = self._solve_target
        m      = self.maze

        self.canvas.delete("mouse")

        if not stack:
            self.status.config(text="No path found (this shouldn't happen in a proper maze).")
            self.solve_btn.config(state="normal")
            return

        r, c = stack[-1]

        if (r, c) == target:
            self.status.config(text=f"✔ Path found! Length: {len(stack)} cells.")
            # Highlight the final path in gold
            for pr, pc in stack:
                self.draw_dot(pr, pc, "#ffd700", tag="dot")
            self.draw_openings()
            self.solve_btn.config(state="normal")
            return

        # Draw current position
        self.draw_dot(r, c, "#ef5350", tag="dot")

        # Find unvisited, reachable neighbours
        moves = []
        for nr, nc in m.neighbors(r, c):
            if (nr, nc) not in self._solve_visited and not m.has_wall(r, c, nr, nc):
                moves.append((nr, nc))

        if moves:
            next_r, next_c = random.choice(moves)
            self._solve_visited.add((next_r, next_c))
            stack.append((next_r, next_c))
        else:
            # Dead end — mark blue and backtrack
            self.draw_dot(r, c, "#1565c0", tag="dot")
            stack.pop()

        self._job = self.master.after(SOLVE_DELAY, self._step_solve)

    #  Reset

    def reset(self):
        if self._job:
            self.master.after_cancel(self._job)
            self._job = None
        self.canvas.delete("all")
        self.maze  = None
        self.start = None
        self.end   = None
        self.gen_btn.config(state="normal")
        self.solve_btn.config(state="disabled")
        self.status.config(text="Press Generate to build a maze.")


# Entry point 
if __name__ == "__main__":
    root = tk.Tk()
    app  = MazeApp(root)
    root.configure(bg="#1a1a2e")
    root.mainloop()