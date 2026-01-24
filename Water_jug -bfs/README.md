# Water Jug Problem – BFS Simulation (using python)


## About the Project

This project is based on the classical Water Jug Problem, implemented as part of an AI assignment.
The solution is developed using Python and uses Breadth First Search (BFS) with production rules to reach the goal state.
The program also displays the state space tree and shows step-by-step transitions between jug states.


## Problem Statement

There are two water jugs:
Jug A – 4 liters capacity
Jug B – 3 liters capacity
Initially both jugs are empty.
The objective is to get 2 liters of water in Jug A using valid operations.


## Approach Used

The problem is modeled as a state-space search
Each state is represented as (A, B)
BFS is used to explore all possible states
A visited list is maintained to avoid repeated states
Production rules are applied to generate new states
This approach guarantees that one valid and shortest solution is found.


## Production Rules Used

The following production rules are used to generate successor states:
1. Fill Jug A if X < 4 → (4, Y)
2. Fill Jug B if Y < 3 → (X, 3)
3. Empty Jug A if X > 0 → (0, Y)
4. Empty Jug B if Y > 0 → (X, 0)
5. Pour from Jug B to Jug A until Jug A is full
6. Pour from Jug A to Jug B until Jug B is full
7. Pour all water from Jug B into Jug A
8. Pour all water from Jug A into Jug B
These rules are implemented directly in the code.


## About the Code

Language used: Python
Algorithm: Breadth First Search (BFS)
The program takes jug capacities and goal as input
The solution path is printed step by step
Simple animation is shown in terminal using ASCII output
The code is kept simple and readable for understanding the logic.


## How to Run the Program

1. Make sure Python is installed
2. Run the file:
        python water_jug_bfs.py
3. Enter:
        Capacity of Jug A
        Capacity of Jug B
        Goal amount in Jug A


## Output

1. State space tree
2. Production rules
3. One valid solution path
4. Final goal state is reached successfully


## Conclusion

This project shows how classical AI search techniques like BFS can be used to solve constraint based problems such as the Water Jug Problem.


## Folder Structure

Water-Jug-BFS/
│
├── waterjug_bfs.py
├── results/
│   └── screenshots
└── README.md
