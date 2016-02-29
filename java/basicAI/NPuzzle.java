import java.io.*;
import java.util.*;

public class NPuzzle {
    
    private class Board implements Comparable<Board> {
        public final int cost;
        public final int heur;
        public final int zeropos;
        public final Board parent;
        public final int[] arr;
        public final String action;
        
        //standard constructor
        public Board(int turn, int zpos, int[] board, Board parent, String act) {
            zeropos = zpos;
            cost = turn;
            this.parent = parent;
            arr = Arrays.copyOf(board, board.length);
            heur = boardEval(arr);
            action = act;
        }
        
        //copy constructor
        //swaps the given two entries
        public Board(Board old, int swap1, int swap2, String act) {
            cost = old.cost+1;
            if (old.arr[swap1] == 0) {
                zeropos = swap2;
            } else if (old.arr[swap2] == 0) {
                zeropos = swap1;
            } else {
                zeropos = old.zeropos;
            }
            this.parent = old;
            
            int[] tmpArr = Arrays.copyOf(old.arr, old.arr.length);
            int tmp = tmpArr[swap1];
            tmpArr[swap1] = tmpArr[swap2];
            tmpArr[swap2] = tmp;
            arr = tmpArr;
            heur = boardEval(arr);
            action = act;
        }
        
        public int getFinalCostEstimate() {
            return cost + heur;
        }
        
        //print the actions to get from the start to this board
        public void printActions() {
            if(parent == null) return;
            parent.printActions();
            System.out.println(action);
        }
        
        public int compareTo(Board b) {
            return (cost + heur - b.cost - b.heur);
        }
        
        public boolean equals(Object o) {
            if (o instanceof Board) {
                Board b = (Board) o;
                
                //Just checks that the board order is identical right now
                if (arr.length != b.arr.length) return false;
                for (int i = 0; i < arr.length; i++) {
                    if ( arr[i] != b.arr[i] ) return false;
                }
                return true;
            }
            return false;
        }
        
        public int hashCode() {
            return Arrays.hashCode(arr);
        }
        
        private int boardEval(int[] arr) { //heuristic uses L1 distance
            int score = 0;
            for (int i = 0; i < arr.length; i++) {
                score += Math.abs(i-arr[i]);
            }
            return score;
        }
    }

    public static void main(String[] args) {
        //workaround for inner class:
        Solution sol = new Solution();
        
        Scanner s = new Scanner(System.in);
        int k = s.nextInt();
        int[] arr = new int[k*k];
        int zpos = -1;
        for (int i = 0; i < arr.length; i++) {
            arr[i] = s.nextInt();
            if (arr[i] == 0) zpos = i;
        }
        
        //now we have the initial board and the zero position
        
        
        Board solvedBoard = null;
        int solvedCost = Integer.MAX_VALUE;
        
        PriorityQueue<Board> pq = new PriorityQueue<Board>(); //Stores the list of nodes to be searched
        HashSet<Board> old = new HashSet<Board>(); //Stores the list of nodes already searched
        pq.add(sol.new Board(0, zpos, arr, null, null));
        while(pq.size() > 0 && pq.peek().getFinalCostEstimate() < solvedCost) {
            //continue searching
            Board tmp = pq.poll();
            Board tmp2;
            
            if (tmp.heur == 0) {
                //we have a solution
                if (tmp.getFinalCostEstimate() < solvedCost) {
                    solvedBoard = tmp;
                    solvedCost = tmp.getFinalCostEstimate();
                }
            } else {
                //insert neighbors if they are not in the old set
                if (tmp.zeropos - k >= 0) {
                    //insert "UP"
                    tmp2 = sol.new Board(tmp, tmp.zeropos, tmp.zeropos-k, "UP");
                    if (!old.contains(tmp2)) pq.add(tmp2);
                }
                if (tmp.zeropos + k < k*k) {
                    //insert "DOWN"
                    tmp2 = sol.new Board(tmp, tmp.zeropos, tmp.zeropos+k, "DOWN");
                    if (!old.contains(tmp2)) pq.add(tmp2);
                }
                if (tmp.zeropos % k < k-1) {
                    //insert "RIGHT"
                    tmp2 = sol.new Board(tmp, tmp.zeropos, tmp.zeropos+1, "RIGHT");
                    if (!old.contains(tmp2)) pq.add(tmp2);
                }
                if (tmp.zeropos % k > 0) {
                    //insert "LEFT"
                    tmp2 = sol.new Board(tmp, tmp.zeropos, tmp.zeropos-1, "LEFT");
                    if (!old.contains(tmp2)) pq.add(tmp2);
                }
            }
            
            //we have searched this board
            old.add(tmp);
        }
        
        //At this point, either no solution was found, or the best solution is stored as solvedBoard
        if(solvedBoard != null) {
            System.out.println(solvedBoard.getFinalCostEstimate());
            solvedBoard.printActions();
        } else {
            System.out.println("ERROR!!!");
        }
        
    }
}
