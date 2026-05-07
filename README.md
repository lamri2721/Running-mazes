\# Maze Generator \& Solver



\## Author

\*\*Tsion\*\*



\---



\## Project Description

This project is a Python-based graphical maze generator and solver built using Tkinter.



The maze is created using a \*\*stack-based Depth First Search (DFS)\*\* algorithm with recursive backtracking.  

A virtual “mouse” moves through the maze, carving paths by removing walls between cells. When the mouse reaches a dead end, it backtracks using a stack until all cells have been visited.



The application also includes a maze-solving visualization that searches for a valid path from the maze entrance to the exit.



\---



\## Features

\- Random maze generation

\- Stack-based DFS algorithm

\- Recursive backtracking

\- Animated maze generation

\- Maze solving visualization

\- Start and end openings

\- Tkinter graphical interface

\- Optional cycle creation using extra wall removal



\---



\## Data Structures



The maze uses two important wall arrays:



\### `northWall\[row]\[col]`

Stores the north wall status for each maze cell.



\### `eastWall\[row]\[col]`

Stores the east wall status for each maze cell.



Both arrays use Boolean values:

\- `True` → wall exists

\- `False` → wall removed



These structures efficiently represent the maze layout while satisfying the assignment requirements.



\---



\## Algorithms Used



\### Maze Generation

The maze generation process follows these steps:



1\. Start from a random cell

2\. Mark the cell as visited

3\. Randomly choose an unvisited neighbor

4\. Remove the wall between the cells

5\. Push the current cell onto a stack

6\. Continue until no unvisited neighbors remain

7\. Backtrack using the stack



This creates a fully connected maze.



\### Maze Solving

The solver:

\- Explores reachable neighboring cells

\- Avoids revisiting cells

\- Backtracks from dead ends

\- Stops when the exit is reached



The final successful path is highlighted visually.



\---



\## Technologies Used

\- Python

\- Tkinter

\- Random module



\---



\## File Structure



```text

maze3d.py      # Main maze generator and solver program

README.md      # Project documentation

```



\---



\## How to Run



\### 1. Install Python

Make sure Python 3 is installed on your computer.



\### 2. Run the Program



```bash

python maze3d.py

```



\---



\## GUI Controls



| Button | Function |

|--------|----------|

| Generate | Creates a new random maze |

| Solve | Solves the generated maze |

| Reset | Clears the maze and restarts |



\---



\## Project Objective

The purpose of this project is to demonstrate:

\- Graph traversal algorithms

\- DFS and backtracking

\- Maze representation using arrays

\- GUI programming with Tkinter

\- Problem solving and visualization techniques







