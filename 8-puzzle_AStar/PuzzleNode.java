package EightPuzzleAStar;

import java.util.*;

public class PuzzleNode {
    int[][] state;
    int g,h,f;
    PuzzleNode parent;
    String move;
    static int[][] GOAL;

    PuzzleNode(int[][] s,int g,PuzzleNode p,String m){
        state=s;
        this.g=g;
        parent=p;
        move=m;
        h=manhattan();
        f=g+h;
    }

    int manhattan(){
        int d=0;
        for(int i=0;i<3;i++)
            for(int j=0;j<3;j++)
                if(state[i][j]!=0)
                    for(int r=0;r<3;r++)
                        for(int c=0;c<3;c++)
                            if(GOAL[r][c]==state[i][j])
                                d+=Math.abs(i-r)+Math.abs(j-c);
        return d;
    }

    boolean isGoal(){
        return Arrays.deepEquals(state,GOAL);
    }

    List<PuzzleNode> expand(){
        List<PuzzleNode> kids = new ArrayList<>();
        int x=0,y=0;

        for(int i=0;i<3;i++)
            for(int j=0;j<3;j++)
                if(state[i][j]==0){ x=i; y=j; }

        int[][] d={{-1,0},{1,0},{0,-1},{0,1}};
        String[] lbl={"Up","Down","Left","Right"};

        for(int k=0;k<4;k++){
            int nx=x+d[k][0], ny=y+d[k][1];
            if(nx>=0&&nx<3&&ny>=0&&ny<3){
                int[][] ns=new int[3][3];
                for(int i=0;i<3;i++) ns[i]=state[i].clone();
                ns[x][y]=ns[nx][ny];
                ns[nx][ny]=0;
                kids.add(new PuzzleNode(ns,g+1,this,lbl[k]));
            }
        }
        return kids;
    }

    public boolean equals(Object o){
        return o instanceof PuzzleNode &&
               Arrays.deepEquals(state,((PuzzleNode)o).state);
    }

    public int hashCode(){
        return Arrays.deepHashCode(state);
    }
}
