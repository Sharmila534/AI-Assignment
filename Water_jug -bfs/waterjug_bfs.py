from collections import deque
import time
import os

def clear():
    os.system("cls" if os.name == "nt" else "clear")

print("\nWATER JUG PROBLEM USING PRODUCTION RULES\n")
A = int(input("Enter capacity of Jug A: "))
B = int(input("Enter capacity of Jug B: "))
goal = int(input("Enter target amount in Jug A: "))

start = (0, 0)
rules = {1: "Fill Jug A",2: "Fill Jug B",3: "Empty Jug A",4: "Empty Jug B",
    5: "Pour from Jug B to Jug A until Jug A is full",6: "Pour from Jug A to Jug B until Jug B is full",
    7: "Pour all water from Jug B into Jug A",8: "Pour all water from Jug A into Jug B"}

def goal_test(s):
    return s[0] == goal

def successors(s):
    x, y = s
    out = []
    if x < A:
        out.append(((A, y), 1))
    if y < B:
        out.append(((x, B), 2))
    if x > 0:
        out.append(((0, y), 3))
    if y > 0:
        out.append(((x, 0), 4))
    if y > 0 and x + y >= A:
        out.append(((A, y - (A - x)), 5))
    if x > 0 and x + y >= B:
        out.append(((x - (B - y), B), 6))
    if y > 0 and x + y <= A:
        out.append(((x + y, 0), 7))
    if x > 0 and x + y <= B:
        out.append(((0, x + y), 8))
    return out

queue = deque([start])
visited = {start}
parent = {}
rule_used = {}
tree = {start: []}
goal_state = None

while queue:
    cur = queue.popleft()
    if goal_test(cur):
        goal_state = cur
        break
    for nxt, r in successors(cur):
        if nxt not in visited:
            visited.add(nxt)
            parent[nxt] = cur
            rule_used[nxt] = r
            tree.setdefault(cur, []).append(nxt)
            tree.setdefault(nxt, [])
            queue.append(nxt)


path = []
applied = []
t = goal_state
while t != start:
    path.append(t)
    applied.append(rule_used[t])
    t = parent[t]

path.append(start)
applied.append("-")

path.reverse()
applied.reverse()

def show_tree(node, depth):
    print("   " * depth + str(node))
    for c in tree[node]:
        show_tree(c, depth + 1)

clear()
print("STATE SPACE TREE\n")
show_tree(start, 0)


def draw_jugs(a, b):
    print("\nJug A            Jug B")
    print("-----            -----")
    h = max(A, B)
    for i in range(h, 0, -1):
        la = "█" if a >= i else " "
        lb = "█" if b >= i else " "
        print(f"  {la}                {lb}")
    print("-----            -----")
    print(f" {a}L               {b}L\n")

def animate(from_a, from_b, to_a, to_b):
    steps = max(abs(from_a - to_a), abs(from_b - to_b), 1)
    for i in range(1, steps + 1):
        a = from_a + (to_a - from_a) * i // steps
        b = from_b + (to_b - from_b) * i // steps
        clear()
        draw_jugs(a, b)
        time.sleep(344)


clear()
print("PRODUCTION RULES\n")
print("Rule No   Action")
for k in rules:
    print(f"{k:^7}   {rules[k]}")
time.sleep(3)

for i in range(len(path)):
    clear()
    print("One Solution to the Water Jug Problem\n")
    print("Jug A Capacity   Jug B Capacity   Condition        Rule Applied")
    print(f"{path[i][0]:^16}{path[i][1]:^18}{'(A='+str(path[i][0])+', B='+str(path[i][1])+')':^18}{applied[i]}")
    if i > 0:
        animate(path[i-1][0], path[i-1][1], path[i][0], path[i][1])
        print(f"Rule {applied[i]} Applied: {rules[applied[i]]}")
    else:
        draw_jugs(path[i][0], path[i][1])
    time.sleep(1)

print("\nGoal reached successfully\n")
