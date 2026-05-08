🧩 Maze Generator & Solver

An interactive Python application that generates and solves mazes visually using Depth First Search (DFS) and Backtracking algorithms, with real-time animation using Tkinter.

🔗 Demo Video:
https://www.loom.com/share/3fb4dbcca078410e98a35596024a58d5

👨‍💻 Author Information
Name: Tsion Tibebeb
ID: UGR/5796/16
✨ Project Overview

This project simulates how a maze is:

Generated automatically using DFS (stack-based backtracking)
Solved automatically using a second DFS backtracking algorithm
Visualized step-by-step using Tkinter animations

The maze is guaranteed to be a perfect maze (spanning tree), meaning:

Every cell is reachable
There is exactly one unique path between any two cells
🧠 Algorithms Used
🔹 1. Maze Generation (DFS Stack)

The maze is created using Depth First Search (DFS):

Start from a random cell
Visit unvisited neighbors randomly
Remove walls between cells
Backtrack using a stack when stuck

✔ Ensures a perfect maze (no loops, no isolated cells)

🔹 2. Maze Solving (Backtracking DFS)

The solver uses a second DFS process:

Starts from the start cell
Explores available paths (no walls)
Uses a stack to backtrack when dead ends occur
Continues until the end cell is reached

🎨 Visualization System

The maze uses color-coded animation for better understanding:

| Color             | Meaning                           |
| ----------------- | --------------------------------- |
| 🔵 Dark Blue      | Current cell during generation    |
| 🟢 Green          | Newly visited cell (maze carving) |
| ⚫ Dark Background | Backtracking step                 |
| 🟡 Yellow         | Current solver path               |
| 🔵 Light Blue     | Forward movement (solver)         |
| 🔴 Red            | Dead end (backtracking)           |
| 🟢 Cyan           | Final correct solution path       |


🧱 Maze Representation

Each cell stores walls using:

<img width="630" height="81" alt="Screenshot 2026-05-08 124620" src="https://github.com/user-attachments/assets/611be90a-85eb-4f01-99fb-119d79c83d43" />

Wall Rules:
True → wall exists
False → wall removed

This simplifies maze drawing and path checking.

🖥️ Features

✔ Random maze generation
✔ Guaranteed solvable maze
✔ Animated DFS generation
✔ Animated backtracking solver
✔ Clean Tkinter GUI
✔ Start and end path solving
✔ Color-coded visualization
✔ Stack-based logic (no recursion issues)

📌 How It Works (Simple Explanation)
Maze Generation:

Think of a “mouse” walking through cells:

It randomly moves forward
Breaks walls between cells
If stuck → it backtracks using a stack
Maze Solving:

Another “mouse”:

Tries to move forward
If blocked → tries another direction
If stuck → goes back (backtracking)
🎥 Demonstration

Watch the full working demo here:

👉 https://www.loom.com/share/3fb4dbcca078410e98a35596024a58d5

The video shows:

Maze generation process (animated carving)
Solver exploring paths
Backtracking at dead ends
Final solution path discovery
🚀 Future Improvements
A* pathfinding algorithm
BFS shortest path visualization
Maze size slider (UI control)
Save/load maze feature
3D maze visualization
Sound effects for movement
📜 License

This project is created for educational purposes as part of a data structures and algorithms assignment.

⭐ Summary

This project demonstrates:

Graph traversal (DFS)
Stack-based backtracking
Pathfinding logic
GUI programming in Python
Algorithm visualization
