from flask import Flask, render_template, request, jsonify
from collections import deque

app = Flask(__name__)

RULES = {
    1: "Fill Jug A",
    2: "Fill Jug B",
    3: "Empty Jug A",
    4: "Empty Jug B",
    5: "Pour Jug A → Jug B",
    6: "Pour Jug B → Jug A"
}

def bfs(capA, capB, goal):
    start = (0, 0)
    q = deque([(start, [])])
    visited = set()
    tree = []

    while q:
        (a, b), path = q.popleft()
        tree.append(f"({a},{b})")

        if a == goal:
            return path + [((a, b), 0)], tree

        if (a, b) in visited:
            continue
        visited.add((a, b))

        moves = [
            ((capA, b), 1),
            ((a, capB), 2),
            ((0, b), 3),
            ((a, 0), 4),
            ((max(0, a - (capB - b)), min(capB, b + a)), 5),
            ((min(capA, a + b), max(0, b - (capA - a))), 6)
        ]

        for (na, nb), r in moves:
            if (na, nb) not in visited:
                q.append(((na, nb), path + [((a, b), r)]))
                tree.append(f"  └─ R{r}: {RULES[r]} → ({na},{nb})")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/solve", methods=["POST"])
def solve():
    data = request.json
    capA = int(data["capA"])
    capB = int(data["capB"])
    goal = int(data["goal"])

    steps, tree = bfs(capA, capB, goal)

    return jsonify({
        "steps": [
            {"A": a, "B": b, "rule": RULES.get(r, "GOAL"), "rno": r}
            for (a, b), r in steps
        ],
        "tree": tree,
        "capA": capA,
        "capB": capB
    })

if __name__ == "__main__":
    app.run(debug=True)
