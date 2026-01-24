import java.util.*;
public class tree {
    static int maxDepth = 2;
    static void print(List<EightPuzzleAStar.State> path) {
        System.out.println("\nstate space tree (limited depth):\n");
        for (int i = 0; i < path.size() && i <= maxDepth; i++) {
            EightPuzzleAStar.State s = path.get(i);
            for (int k = 0; k < i; k++)
                System.out.print("    ");
            System.out.println(Arrays.toString(s.b));
            if (i == maxDepth) continue;
            List<int[]> next = getMoves(s.b);
            for (int j = 0; j < next.size(); j++) {
                for (int k = 0; k < i + 1; k++)
                    System.out.print("    ");
                System.out.println("\\-- " + Arrays.toString(next.get(j)));
            }
            System.out.println();
        }
    }
    static List<int[]> getMoves(int[] b) {
        List<int[]> list = new ArrayList<>();
        int z = 0;
        for (int i = 0; i < 9; i++)
            if (b[i] == 0) z = i;
        int r = z / 3, c = z % 3;
        int[][] m = {{-1,0},{1,0},{0,-1},{0,1}};
        for (int[] d : m) {
            int nr = r + d[0], nc = c + d[1];
            if (nr >= 0 && nr < 3 && nc >= 0 && nc < 3) {
                int ni = nr * 3 + nc;
                int[] nb = b.clone();
                nb[z] = nb[ni];
                nb[ni] = 0;
                list.add(nb);
            }
        }
        return list;
    }
    public static void main(String[] args) {
        System.out.println("run EightPuzzleAStar to see the state space tree");
    }
}
