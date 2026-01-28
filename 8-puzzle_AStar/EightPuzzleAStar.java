package EightPuzzle;
import javax.swing.*;
import javax.swing.border.TitledBorder;
import javax.swing.tree.*;
import java.awt.*;
import java.util.*;


public class EightPuzzleAStar extends JFrame {

    JButton[][] buttons = new JButton[3][3];
    JTextArea openArea = new JTextArea();
    JTextArea closedArea = new JTextArea();

    int[][] start = new int[3][3];
    int[][] goal = new int[3][3];

    DefaultMutableTreeNode rootNode;
    DefaultTreeModel treeModel;
    JTree tree;

    // ---------- STATE ----------
    class State {
        int[][] board;
        int g, h;
        State parent;
        DefaultMutableTreeNode treeNode;

        State(int[][] b, int g, State p, DefaultMutableTreeNode t) {
            board = b;
            this.g = g;
            parent = p;
            treeNode = t;
            h = manhattan(b);
        }

        int f() {
            return g + h;
        }
    }

    // ---------- CONSTRUCTOR ----------
    public EightPuzzleAStar() {
        setTitle("8 Puzzle – A* Visual Simulator");
        setSize(1100, 650);
        setLayout(new BorderLayout(10, 10));
        getContentPane().setBackground(new Color(25, 28, 34));

        // -------- PUZZLE GRID --------
        JPanel grid = new JPanel(new GridLayout(3, 3, 8, 8));
        grid.setBackground(new Color(45, 45, 45));
        grid.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));

        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 3; j++) {
                JButton b = new JButton("");
                b.setFont(new Font("Segoe UI", Font.BOLD, 26));
                b.setFocusPainted(false);
                b.setBackground(new Color(80, 80, 80));
                b.setForeground(Color.WHITE);
                b.setBorder(BorderFactory.createCompoundBorder(
                        BorderFactory.createRaisedBevelBorder(),
                        BorderFactory.createLoweredBevelBorder()
                ));
                buttons[i][j] = b;
                grid.add(b);
            }
        }

        // -------- TOP CONTROLS --------
        JButton inputBtn = new JButton("Input State");
        JButton solveBtn = new JButton("Solve A*");

        styleButton(inputBtn);
        styleButton(solveBtn);

        inputBtn.addActionListener(e -> getInput());
        solveBtn.addActionListener(e -> solve());

        JPanel top = new JPanel();
        top.setBackground(new Color(25, 28, 34));
        top.add(inputBtn);
        top.add(solveBtn);

        // -------- OPEN / CLOSED --------
        

        styleText(openArea);
        styleText(closedArea);

        JPanel lists = new JPanel(new GridLayout(1, 2, 8, 8));
        lists.setBackground(new Color(25, 28, 34));
        JScrollPane openScroll = new JScrollPane(openArea);
        openScroll.setBorder(BorderFactory.createTitledBorder(
                BorderFactory.createLineBorder(new Color(120, 120, 120)),
                "OPEN List",
                TitledBorder.LEFT,
                TitledBorder.TOP,
                new Font("Segoe UI", Font.BOLD, 13),
                Color.RED
        ));

        JScrollPane closedScroll = new JScrollPane(closedArea);
        closedScroll.setBorder(BorderFactory.createTitledBorder(
                BorderFactory.createLineBorder(new Color(120, 120, 120)),
                "CLOSED List",
                TitledBorder.LEFT,
                TitledBorder.TOP,
                new Font("Segoe UI", Font.BOLD, 13),
                Color.BLUE
        ));

        lists.add(openScroll);
        lists.add(closedScroll);


        // -------- STATE SPACE TREE --------
        rootNode = new DefaultMutableTreeNode("Start");
        treeModel = new DefaultTreeModel(rootNode);
        tree = new JTree(treeModel);
        JScrollPane treePane = new JScrollPane(tree);
        treePane.setBorder(BorderFactory.createTitledBorder(BorderFactory.createLineBorder(new Color(90, 90, 90)),
                "State Space Tree",
                TitledBorder.LEFT,
                TitledBorder.TOP,
                new Font("Segoe UI", Font.BOLD, 12),
                Color.PINK));

        JPanel right = new JPanel(new BorderLayout(8, 8));
        right.setPreferredSize(new Dimension(360, 0));
        right.setBackground(new Color(25, 28, 34));
        JSplitPane verticalSplit = new JSplitPane(
                JSplitPane.VERTICAL_SPLIT,
                lists,
                treePane
        );
        verticalSplit.setResizeWeight(0.6);
        verticalSplit.setDividerSize(6);
        verticalSplit.setDividerLocation(260);
        verticalSplit.setContinuousLayout(true);
        verticalSplit.setOneTouchExpandable(false);


        right.add(verticalSplit, BorderLayout.CENTER);


        add(top, BorderLayout.NORTH);
        JPanel centerWrapper = new JPanel(new GridBagLayout());
        centerWrapper.setBackground(new Color(25, 28, 34));
        centerWrapper.add(grid);
        grid.setPreferredSize(new Dimension(360, 360));
        JSplitPane mainSplit = new JSplitPane(
                JSplitPane.HORIZONTAL_SPLIT,
                centerWrapper,
                right
        );

        mainSplit.setResizeWeight(0.5);    
        mainSplit.setDividerSize(6);
        mainSplit.setContinuousLayout(true);
        mainSplit.setOneTouchExpandable(false);

        add(mainSplit, BorderLayout.CENTER);


        setDefaultCloseOperation(EXIT_ON_CLOSE);
        pack();                                
        setMinimumSize(new Dimension(1100, 650));
        setLocationRelativeTo(null);          
        setVisible(true);

    }

    // ---------- STYLES ----------
    void styleButton(JButton b) {
        b.setBackground(new Color(70, 130, 180));
        b.setForeground(Color.WHITE);
        b.setFont(new Font("Segoe UI", Font.BOLD, 14));
        b.setFocusPainted(false);
    }

    void styleText(JTextArea t) {
        t.setEditable(false);
        t.setBackground(new Color(20, 20, 20));
        t.setForeground(Color.GREEN);
        t.setFont(new Font("Consolas", Font.PLAIN, 12));
    }

    // ---------- INPUT ----------
    void getInput() {
        fill(start, JOptionPane.showInputDialog("Initial State (0-8):"));
        fill(goal, JOptionPane.showInputDialog("Goal State (0-8):"));
        draw(start);
    }

    void fill(int[][] arr, String s) {
        String[] v = s.split(" ");
        int k = 0;
        for (int i = 0; i < 3; i++)
            for (int j = 0; j < 3; j++)
                arr[i][j] = Integer.parseInt(v[k++]);
    }

    // ---------- A* SOLVER ----------
    void solve() {
        openArea.setText("");
        closedArea.setText("");
        rootNode.removeAllChildren();
        treeModel.reload();

        PriorityQueue<State> open =
                new PriorityQueue<>(Comparator.comparingInt(State::f));
        Set<String> closed = new HashSet<>();

        State startState = new State(start, 0, null, rootNode);
        open.add(startState);

        java.util.List<State> path = null;
        int finalCost = 0;

        while (!open.isEmpty()) {
            State cur = open.poll();
            openArea.append(show(cur));

            if (Arrays.deepEquals(cur.board, goal)) {
                path = buildPath(cur);
                finalCost = cur.g;
                break;
            }

            closed.add(Arrays.deepToString(cur.board));
            closedArea.append(show(cur));

            int[] z = findZero(cur.board);
            int[] dx = {1, -1, 0, 0};
            int[] dy = {0, 0, 1, -1};

            for (int i = 0; i < 4; i++) {
                int nx = z[0] + dx[i];
                int ny = z[1] + dy[i];

                if (nx >= 0 && ny >= 0 && nx < 3 && ny < 3) {
                    int[][] nb = copy(cur.board);
                    nb[z[0]][z[1]] = nb[nx][ny];
                    nb[nx][ny] = 0;

                    if (!closed.contains(Arrays.deepToString(nb))) {
                        DefaultMutableTreeNode child =
                                new DefaultMutableTreeNode(Arrays.deepToString(nb));
                        treeModel.insertNodeInto(child, cur.treeNode, cur.treeNode.getChildCount());

                        open.add(new State(nb, cur.g + 1, cur, child));
                    }
                }
            }
        }

        animate(path, finalCost);
    }

    // ---------- HEURISTIC ----------
    int manhattan(int[][] b) {
        int d = 0;
        for (int i = 0; i < 3; i++)
            for (int j = 0; j < 3; j++)
                if (b[i][j] != 0)
                    for (int x = 0; x < 3; x++)
                        for (int y = 0; y < 3; y++)
                            if (b[i][j] == goal[x][y])
                                d += Math.abs(i - x) + Math.abs(j - y);
        return d;
    }

    // ---------- HELPERS ----------
    String show(State s) {
        return Arrays.deepToString(s.board) +
                " g=" + s.g + " h=" + s.h + " f=" + s.f() + "\n";
    }

    int[][] copy(int[][] b) {
        int[][] n = new int[3][3];
        for (int i = 0; i < 3; i++) n[i] = b[i].clone();
        return n;
    }

    int[] findZero(int[][] b) {
        for (int i = 0; i < 3; i++)
            for (int j = 0; j < 3; j++)
                if (b[i][j] == 0)
                    return new int[]{i, j};
        return null;
    }

    java.util.List<State> buildPath(State g) {
        java.util.List<State> p = new ArrayList<>();
        while (g != null) {
            p.add(g);
            g = g.parent;
        }
        Collections.reverse(p);
        return p;
    }

    // ---------- 3D ANIMATION ----------
    void draw(int[][] b) {
        for (int i = 0; i < 3; i++)
            for (int j = 0; j < 3; j++) {
                buttons[i][j].setText(b[i][j] == 0 ? "" : b[i][j] + "");
                buttons[i][j].setBackground(b[i][j] == 0
                        ? new Color(40, 40, 40)
                        : new Color(100, 100, 100));
            }
    }

    void animate(java.util.List<State> path, int cost) {
        if (path == null) {
            JOptionPane.showMessageDialog(this, "No Solution Found");
            return;
        }

        javax.swing.Timer t = new javax.swing.Timer(600, null);
        t.addActionListener(e -> {
            if (path.isEmpty()) {
                t.stop();
                JOptionPane.showMessageDialog(this,
                        "GOAL ACHIEVED 🎉\nTotal Cost = " + cost);
            } else {
                draw(path.remove(0).board);
            }
        });
        t.start();
    }

    // ---------- MAIN ----------
    public static void main(String[] args) {
        new EightPuzzleAStar();
    }
}
