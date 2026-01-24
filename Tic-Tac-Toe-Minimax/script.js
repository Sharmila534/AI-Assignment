const HUMAN = "X";
const AI = "O";

let board = Array(9).fill(null);
let gameOver = false;
let stateTreeLog = "";

const boardEl = document.getElementById("board");
const statusEl = document.getElementById("status");
const treeOutput = document.getElementById("treeOutput");

function init() {
  boardEl.innerHTML = "";
  board.forEach((_, i) => {
    const cell = document.createElement("div");
    cell.className = "cell";
    cell.onclick = () => handleMove(i);
    boardEl.appendChild(cell);
  });
}
init();

function handleMove(index) {
  if (board[index] || gameOver) return;

  placeMove(index, HUMAN);
  if (!gameOver) {
    statusEl.textContent = "AI thinking...";
    setTimeout(aiMove, 500);
  }
}

function placeMove(index, player) {
  board[index] = player;
  const cell = boardEl.children[index];
  cell.textContent = player;
  cell.classList.add(player);

  const result = checkWinner(board);
  if (result) finishGame(result);
}

function aiMove() {
  stateTreeLog = "";
  const best = minimax(board, AI, 0);
  placeMove(best.index, AI);
  if (!gameOver) statusEl.textContent = "Your turn (X)";
}

function checkWinner(b) {
  const wins = [
    [0,1,2],[3,4,5],[6,7,8],
    [0,3,6],[1,4,7],[2,5,8],
    [0,4,8],[2,4,6]
  ];

  for (let [a,b1,c] of wins) {
    if (b[a] && b[a] === b[b1] && b[a] === b[c]) return b[a];
  }
  return b.includes(null) ? null : "draw";
}

function finishGame(result) {
  gameOver = true;
  statusEl.textContent =
    result === "draw" ? "Draw 🤝" :
    result === HUMAN ? "You Win 🎉" :
    "AI Wins 🤖";

  treeOutput.textContent = stateTreeLog;
}

function minimax(state, player, depth) {
  const winner = checkWinner(state);

  if (winner === HUMAN) return { score: -10 + depth };
  if (winner === AI) return { score: 10 - depth };
  if (winner === "draw") return { score: 0 };

  const moves = [];

  state.forEach((cell, i) => {
    if (!cell) {
      const newState = [...state];
      newState[i] = player;

      stateTreeLog += `${" ".repeat(depth * 4)}↳ [Depth ${depth}] ${player} plays at ${i}\n`;
      stateTreeLog += `${" ".repeat(depth * 4)}│\n`;

      const result = minimax(
        newState,
        player === AI ? HUMAN : AI,
        depth + 1
      );

      moves.push({ index: i, score: result.score });
    }
  });

  return player === AI
    ? moves.reduce((a,b) => a.score > b.score ? a : b)
    : moves.reduce((a,b) => a.score < b.score ? a : b);
}

function resetGame() {
  board = Array(9).fill(null);
  gameOver = false;
  stateTreeLog = "";
  treeOutput.textContent = "";
  statusEl.textContent = "Your turn (X)";
  init();
}
