# Tic-Tac-Toe Game using Minimax Algorithm  (using html+css+js)


## About This Project

This project is a Tic-Tac-Toe game where a human plays against an intelligent agent (AI).
The AI uses the Minimax algorithm to make decisions and always tries to play the best possible move.

The game is developed using:
HTML for user interface
CSS for styling
JavaScript for game logic and AI decision making
This project is done as part of AI assignment


## Problem Description

In this game:
-> Human player plays as X
-> AI agent plays as O
-> Both players take turns
 -> The goal is to either win the game or force a draw
The AI evaluates all possible future game states before making a move.

1. Game State Representation
The board is represented as a 1D array of size 9
Each cell can contain:
    "X" → Human move
    "O" → AI move
    null → Empty cell
Example:
    ["X", null, "O",
    null, "X", null,
    "O", null, null]
This representation makes it easy to generate next states.

2. Terminal States
A game state is considered terminal if:
    Win → Any player gets 3 symbols in a row, column, or diagonal
    Lose → Opponent wins
    Draw → Board is full and no player wins
These terminal states stop further recursion in Minimax.

3. Minimax Algorithm Explanation
Minimax is a recursive decision-making algorithm used in turn-based games.
AI tries to maximize the score
Human tries to minimize the score
Scoring system used:
    AI win → +10
    Human win → -10
    Draw → 0
The algorithm explores all possible future game states and chooses the move that gives the best guaranteed outcome for the AI.
Because of this, the AI never makes a random or losing move.

4. Implementation Details
UI (HTML)
   -> A 3×3 board is dynamically generated
    ->Each cell is clickable for human moves
    ->Game status is displayed at the top
Game Logic (JavaScript)
    ->Handles user input
    ->Switches turns between Human and AI
    ->Checks for win, lose, or draw
    ->Calls Minimax to decide AI moves
Styling (CSS)
    ->Clean and modern UI
    ->Visual difference between X and O
    ->Smooth hover and transition effects

5. Simulation Features
Human vs AI Gameplay
    ->Human clicks on a cell to play
    ->AI responds automatically after a short delay
    ->Game ends with Win / Lose / Draw message
AI Decision Making
    ->AI evaluates future states using Minimax
    ->The state-space tree is logged
    ->Depth-wise exploration is displayed after game completion
This clearly shows how AI reasons before selecting a move.

6. Optimal Play by AI
->AI always plays optimally
->AI either wins or forces a draw
->Human cannot defeat the AI with correct play
This proves correct implementation of Minimax.


## How to Run the Project

1. Download or clone the repository
2. Open index.html in any modern browser
3. Start playing as X
4. AI automatically plays as O
No external libraries are required.


## Project Structure

Tic-Tac-Toe-Minimax/
│
├── index.html
├── style.css
├── script.js
├── results/
│   └── screenshots
└── README.md
