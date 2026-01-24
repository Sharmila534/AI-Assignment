import java.util.*;

public class EightPuzzleAStar {
    static int[] goal = {1,2,3,4,5,6,7,8,0};
    static class State {
        int[] b; 
        int g; 
        State parent;
        State(int[] b, int g, State p) {
            this.b = b; this.g = g; parent = p;
        }
    }
    static int h(int[] b) {
        int d = 0;
        for(int i=0;i<9;i++){
            if(b[i]==0) continue;
            int pos = b[i]-1;
            d += Math.abs(i/3 - pos/3) + Math.abs(i%3 - pos%3);
        }
        return d;
    }
    static List<int[]> moves(int[] b){
        List<int[]> list = new ArrayList<>();
        int z=0; for(int i=0;i<9;i++) if(b[i]==0) z=i;
        int r=z/3,c=z%3;
        int[][] m={{-1,0},{1,0},{0,-1},{0,1}};
        for(int[] mm:m){
            int nr=r+mm[0],nc=c+mm[1];
            if(nr>=0 && nr<3 && nc>=0 && nc<3){
                int ni=nr*3+nc;
                int[] nb=b.clone(); nb[z]=nb[ni]; nb[ni]=0;
                list.add(nb);
            }
        }
        return list;
    }
    static void solve(int[] start){
        PriorityQueue<State> q=new PriorityQueue<>(Comparator.comparingInt(s->s.g+h(s.b)));
        Set<String> seen=new HashSet<>();
        State s=new State(start,0,null); q.add(s);

        while(!q.isEmpty()){
            State cur=q.poll();
            if(Arrays.equals(cur.b,goal)){
                printPath(cur); return;
            }
            seen.add(Arrays.toString(cur.b));
            for(int[] n:moves(cur.b)){
                if(!seen.contains(Arrays.toString(n))){
                    q.add(new State(n,cur.g+1,cur));
                }
            }
        }
    }
    static void printPath(State s){
        List<State> path=new ArrayList<>();
        while(s!=null){ path.add(s); s=s.parent; }
        Collections.reverse(path);
        System.out.println("\nsolution steps:\n");
        for(State st:path){
            System.out.println(Arrays.toString(st.b)+" g="+st.g+" h="+h(st.b)+" f="+(st.g+h(st.b)));
        }
        tree.print(path);
    }
    public static void main(String[] args){
        int[] start={1,2,3,4,0,6,7,5,8};
        solve(start);
    }
}
