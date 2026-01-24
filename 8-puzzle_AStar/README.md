# 8-Puzzle Problem using A* Search (using Java)


## About This Project

This project implements the 8-Puzzle Problem using the A* Search Algorithm in Java.
The objective is to transform a given initial puzzle configuration into the goal configuration using minimum number of moves.
The implementation uses:
    ->A* search
    ->Manhattan Distance heuristic
    ->Priority Queue for open list
    ->Set for closed list
    ->Parent tracking to show solution path
This was developed as part of an AI / Heuristic Search assignment.


## Problem Description

The 8-Puzzle consists of a 3×3 grid with:
    ->8 numbered tiles (1 to 8)
    ->One empty space represented by 0
Initial State
1 2 3
4 0 6
7 5 8
Goal State
1 2 3
4 5 6
7 8 0
The task is to reach the goal state using valid tile movements.

1. State-Space Representation

Each state is represented as a 1D integer array of size 9
0 represents the empty space
Example:[1, 2, 3, 4, 0, 6, 7, 5, 8]
This makes comparison and movement generation simple.

2. Heuristic Function

The heuristic used is Manhattan Distance.
Manhattan Distance
For each tile:
|current_row - goal_row| + |current_col - goal_col|
The empty tile (0) is ignored
Total heuristic value is the sum of distances of all tiles
This heuristic is:
    ->Admissible
    ->Efficient
    ->Suitable for A* search

3. A* Algorithm Implementation

A* search uses the evaluation function:
    f(n) = g(n) + h(n)
Where:
    ->g(n) → Path cost from start to current state
    ->h(n) → Heuristic value (Manhattan distance)
    ->f(n) → Total estimated cost
Data Structures Used
    ->PriorityQueue → Open list (based on f value)
    ->HashSet → Closed list (visited states)
    ->Parent reference → To reconstruct solution path

4. Simulation Details
Open List
    ->Maintained using a PriorityQueue
    ->Always selects the state with minimum f value
Closed List
    ->Stores already visited states
    ->Prevents repeated exploration
Path Cost and Heuristic
For every state printed:
    g → Path cost
    h → Heuristic value
    f → Total cost
Example output:
[1, 2, 3, 4, 5, 6, 7, 8, 0] g=4 h=0 f=4

5. Solution Path Display

->The solution path is reconstructed using parent pointers
->States are printed from initial to goal
->Each step clearly shows g, h, and f values
A limited depth state-space tree is also printed for visualization.


## About the Code

->Language: Java
->Algorithm: A* Search
->Heuristic: Manhattan Distance
->EightPuzzleAStar.java → Core A* logic
->tree.java → Displays limited state-space tree
The code is intentionally kept simple for understanding the algorithm flow.


## How to Run the Program

Compile the files:
    javac EightPuzzleAStar.java tree.java
Run the program:
    java EightPuzzleAStar
The solution steps and state-space tree will be printed in the console.


## Project Structure

Eight-Puzzle-AStar/
│
├── EightPuzzleAStar.java
├── tree.java
├── results/
│   └── screenshots/
└── README.md
