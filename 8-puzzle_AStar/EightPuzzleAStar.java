package EightPuzzleAStar;

import javax.swing.*;
import java.awt.*;
import java.util.List;
import java.util.*;

public class EightPuzzleSimulator extends JFrame {
    JButton[][] tiles = new JButton[3][3];
    JTextArea log = new JTextArea();
    JLabel info = new JLabel("Status: Ready", JLabel.CENTER);
    List<PuzzleNode> sol;
    int step = 0;

    public EightPuzzleSimulator() {
        setTitle("8-Puzzle A*");
        setSize(1000,650);
        setLayout(null);
        setDefaultCloseOperation(EXIT_ON_CLOSE);

        JPanel grid = new JPanel(new GridLayout(3,3,5,5));
        grid.setBounds(20,20,400,400);

        for(int i=0;i<3;i++)
            for(int j=0;j<3;j++){
                tiles[i][j]=new JButton();
                tiles[i][j].setFont(new Font("Arial",Font.BOLD,40));
                grid.add(tiles[i][j]);
            }

        add(grid);

        info.setBounds(20,430,400,30);
        add(info);

        log.setEditable(false);
        log.setFont(new Font("Consolas",0,12));
        JScrollPane sp = new JScrollPane(log);
        sp.setBounds(450,20,500,440);
        add(sp);

        solve();
        animate();
        setVisible(true);
    }

    int[][] input(String title){
        while(true){
            String s = JOptionPane.showInputDialog(
                    this,"Enter 9 numbers (0 to 8) space-separated",title,1);
            if(s==null) System.exit(0);

            String[] a = s.trim().split("\\s+");
            if(a.length!=9) continue;

            int[][] m = new int[3][3];
            boolean[] seen = new boolean[9];

            try{
                for(int i=0;i<9;i++){
                    int n = Integer.parseInt(a[i]);
                    if(n<0||n>8||seen[n]) throw new Exception();
                    seen[n]=true;
                    m[i/3][i%3]=n;
                }
                return m;
            }catch(Exception e){
                JOptionPane.showMessageDialog(this,"Invalid Input!");
            }
        }
    }

    void solve(){
        int[][] start = input("Start State");
        PuzzleNode.GOAL = input("Goal State");

        PriorityQueue<PuzzleNode> open =
                new PriorityQueue<>(Comparator.comparingInt(n->n.f));
        HashSet<PuzzleNode> closed = new HashSet<>();

        open.add(new PuzzleNode(start,0,null,"Initial"));

        while(!open.isEmpty()){
            PuzzleNode cur = open.poll();

            log.append("\nEXPAND: "+cur.move+
                       " g="+cur.g+" h="+cur.h+" f="+cur.f+"\n");

            if(cur.isGoal()){
                sol = new ArrayList<>();
                while(cur!=null){
                    sol.add(cur);
                    cur = cur.parent;
                }
                Collections.reverse(sol);
                return;
            }

            closed.add(cur);
            for(PuzzleNode c : cur.expand())
                if(!closed.contains(c)) open.add(c);
        }

        JOptionPane.showMessageDialog(this,"No Solution Found!");
    }

    void animate(){
        if(sol==null || step>=sol.size()) return;

        PuzzleNode n = sol.get(step++);
        for(int i=0;i<3;i++)
            for(int j=0;j<3;j++){
                tiles[i][j].setText(""+n.state[i][j]);
                tiles[i][j].setBackground(
                        n.state[i][j]==0 ? Color.LIGHT_GRAY : Color.WHITE);
            }

        info.setText("Step: "+(step-1)+" | g="+n.g+" | h="+n.h+" | f="+n.f);

        new javax.swing.Timer(1500,e->animate()).start();
    }

    public static void main(String[] args){
        SwingUtilities.invokeLater(EightPuzzleSimulator::new);
    }
}
