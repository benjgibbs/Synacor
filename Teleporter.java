
import java.util.Map;
import java.util.List;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Deque;
import java.util.ArrayDeque;

class Teleporter {

  private final static int BASE = 32768;
  
  private final Map<Integer, Map<Integer, List<Integer>>> cache = new HashMap<>();

  private final Deque<Integer> stack = new ArrayDeque<>();
  
  private final int r7;

  private Teleporter(int x, int y, int r7) {
    this.x = x;
    this.y = y;
    this.r7 = r7;
  }

  private int x;

  private int y;

  void call() {
    if (x == 0) {
      x = add(y,y);
      return;
    }
    if (y == 0) {
      x = add(x,x);
      y = r7;
      call();
      return;
    } 
    if (has()) {
      reset();
      return;
    }
    int x1 = x;
    int y1 = y;
    call2();
    store(x1,y1);
  }
  
  void call2() {
    stack.addFirst(x);
    y = add(y,y);
    call();
    y = x;
    x = stack.removeFirst();
    x = add(x,x);
    call();
  }

  static int add(int a, int b) {
    return (a + b) % BASE;
  }
  
  void store(int x1, int y1) {
    if (!cache.containsKey(x1)) {
      cache.put(x1, new HashMap<>());
    }
    List<Integer> points = new ArrayList<>();
    points.add(x);
    points.add(y);
    cache.get(x1).put(y1, points);
  }

  void reset() {
    List<Integer> hist = cache.get(x).get(y);
    x = hist.get(0);
    y = hist.get(1);
  }

  boolean has() {
    if (cache.containsKey(x)) {
      return cache.get(x).containsKey(y);
    }
    return false;
  }

  public static void main(String[] args) {
    assert add(32758, 15) == 5;

    for (int i = 0; i < BASE; i++) {
      Teleporter t = new Teleporter(4, 1, i);
      t.call();
      if (t.x != 0 || t.y != 0) {
        System.out.println("\n" + i + ": x=" + t.x + ", y=" + t.y);
      } else {
        if ( i % 250  == 0 ) {
          System.out.print(".");
        }
      }
    }
    System.out.println();
  }
}
