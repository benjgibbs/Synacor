import java.io.*;
import java.lang.*;
import java.nio.*;
import java.nio.file.*;
import java.util.*;

class List {
  static final int MAX = 32768;
  final int [] mem = new int[MAX + 8];
   
  List(int[] bin) {
    assert bin.length < MAX;
    System.arraycopy(bin, 0, mem, 0, bin.length);
  }

  int res(int a) {
    if (a < MAX) {
      return a;
    }
    return mem[a];
  }

  void print(int i, String op, int a, int b, int c) {
    String fmt = String.format("%8d: %5s %8d %8d %8d", i, op, a, b, c);
    System.out.println(fmt);
  }
  
  void print(int i, String op, int a, int b) {
    String fmt = String.format("%8d: %5s %8d %8d", i, op, a, b);
    System.out.println(fmt);
  }
  
  void print(int i, String op, int a) {
    String fmt = String.format("%8d: %5s %8d", i, op, a);
    System.out.println(fmt);
  }
  
  void print(int i, String op, int a, String s) {
    String fmt = String.format("%8d: %5s %8d %8s", i, op, a, s);
    System.out.println(fmt);
  }
  
  void print(int i, String op) {
    String fmt = String.format("%8d: %5s", i, op);
    System.out.println(fmt);
  }

  void run() throws IOException {
    for (int i = 0; i < mem.length; ) {
      int a = i + 1 < mem.length ?  mem[i + 1] : 0;
      int b = i + 2 < mem.length ?  mem[i + 2] : 0;
      int c = i + 3 < mem.length ?  mem[i + 3] : 0;
      switch (mem[i]) { 
        case 0: // halt: 0
          print(i, "halt");
          i += 1;
          break;

        case 1: // set: 1 a b
          print(i, "set", a, b);
          i += 3;
          break;

        case 2: // push: 2 a
          print(i, "push", a);
          i += 2;
          break;
        
        case 3: // pop: 2 a
          print(i, "pop", a);
          i += 2;
          break;

        case 4: // eq: 4 a b c
          print(i, "eq", a, b, c);
          i += 4; 
          break;
        
        case 5: // gt: 5 a b c
          print(i, "gt", a, b, c);
          i += 4; 
          break;

        case 6: // jmp: 6 a
          print(i, "jmp", a);
          i += 2;
          break;

        case 7: // jt: 7 a b
          print(i, "jt", a, b);
          i += 3;
          break;
        
        case 8: // jf: 8 a b
          print(i, "jf", a, b);
          i += 3;
          break;
        
        case 9: // add: 9 a b c
          print(i, "add", a, b, c);
          i += 4; 
          break;

        case 10: // mult: 10 a b c
          print(i, "mult", a, b, c);
          i += 4; 
          break;
        
        case 11: // mod: 11 a b c
          print(i, "mod", a, b, c);
          i += 4; 
          break;

        case 12: // and: 12 a b c
          print(i, "and", a, b, c);
          i += 4;
          break;
        
        case 13: // or: 13 a b c
          print(i, "or", a, b, c);
          i += 4;
          break;
        
        case 14: // not: 14 a b
          print(i, "not", a, b);
          i += 3;
          break;
        
        case 15: // rmem: 15 a b
          print(i, "rmem", a, b);
          i += 3;
          break;
        
        case 16: // wmem: 16 a b
          print(i, "wmem", a, b);
          i += 3;
          break;

        case 17: // call: 17 a
          print(i, "call", a);
          i += 2;
          break;

        case 18: // ret: 18
          print(i, "ret");
          i += 1;
          break;

        case 19: // out: 19 a
          print(i, "out", a, Character.toString((char)a));
          i += 2;
          break;

        case 20: // in: 20 a 
          print(i, "in", a);
          i += 2;
          break;

        case 21:// noop: 21
          print(i, "noop");
          i += 1;
          break;

        default:
          print(i, "<mem>", mem[i]);
          i++;
      }
    }
  }
  
  public static void main(String[] args) throws IOException {
    byte[] bytes = Files.readAllBytes(Paths.get(args[0]));
    
    ByteBuffer leBuf = ByteBuffer.wrap(bytes).order(ByteOrder.LITTLE_ENDIAN);
    int[] bin = new int[bytes.length/2];
    for (int i = 0; i < bin.length; i++) {
      int b = Short.toUnsignedInt(leBuf.getShort(i*2));
      assert b >= 0 && b < 32776;
      bin[i] = b;
    }
    new List(bin).run();
  }
  
}

