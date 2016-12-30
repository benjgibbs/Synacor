import java.io.*;
import java.lang.*;
import java.nio.*;
import java.nio.file.*;
import java.util.*;

class Vm {
  static final int MAX = 32768;
  int pc = 0;
  final Deque<Integer> stack = new LinkedList<>();
  final int [] mem = new int[MAX + 8];
  boolean debug = false;
   
  Vm(int[] bin) {
    assert bin.length < MAX;
    System.arraycopy(bin, 0, mem, 0, bin.length);
  }

  int res(int a) {
    if (a < MAX) {
      return a;
    }
    return mem[a];
  }

  void run() throws IOException {
    System.out.println("Starting");
    StringBuilder out = new StringBuilder();
    while (pc < mem.length) {
      if (debug) {
        System.out.println("pc: " + pc + " ins:" + 
            Arrays.toString(Arrays.copyOfRange(mem, pc, pc + 4)) + "\tregisters:" + 
            Arrays.toString(Arrays.copyOfRange(mem,MAX, MAX + 8)) + "\tstack: " + stack);
      }
      int a = pc + 1 < mem.length ?  mem[pc + 1] : 0;
      int b = pc + 2 < mem.length ?  mem[pc + 2] : 0;
      int c = pc + 3 < mem.length ?  mem[pc + 3] : 0;
      switch (mem[pc]) { 
        case 0: // halt: 0
          pc = Integer.MAX_VALUE;
          break;

        case 1: // set: 1 a b
          mem[a] = res(b);
          pc += 3;
          break;

        case 2: // push: 2 a
          stack.addFirst(res(a));
          pc += 2;
          break;
        
        case 3: // pop: 2 a
          mem[a] = stack.pollFirst();
          pc += 2;
          break;

        case 4: // eq: 4 a b c
          mem[a] = (res(b) == res(c) ? 1 : 0);
          pc += 4; 
          break;
        
        case 5: // gt: 5 a b c
          mem[a] = (res(b) >  res(c) ? 1 : 0);
          pc += 4; 
          break;

        case 6: // jmp: 6 a
          pc = res(a);
          break;

        case 7: // jt: 7 a b
          if (res(a) == 0) {
            pc += 3;
          } else {
            pc = res(b);
          }
          break;
        
        case 8: // jf: 8 a b
          if (res(a) == 0) {
            pc = res(b);
          } else {
            pc += 3;
          }
          break;
        
        case 9: // add: 9 a b c
          mem[a] = (res(b) + res(c)) % MAX;
          pc += 4; 
          break;

        case 10: // mult: 10 a b c
          mem[a] = (res(b) * res(c)) % MAX;
          pc += 4; 
          break;
        
        case 11: // mod: 11 a b c
          mem[a] = res(b) % res(c);
          pc += 4; 
          break;

        case 12: // and: 12 a b c
          mem[a] = res(b) & res(c);
          pc += 4;
          break;
        
        case 13: // or: 13 a b c
          mem[a] = res(b) | res(c);
          pc += 4;
          break;
        
        case 14: // not: 14 a b
          mem[a] = (0x7FFF & ~res(b));
          pc += 3;
          break;
        
        case 15: // rmem: 15 a b
          // read memory at address <b> and write it to <a>
          mem[a] = mem[res(b)];
          pc += 3;
          break;
        
        case 16: // wmem: 16 a b
          // write the value from <b> into memory at address <a>
          mem[res(a)] = res(b);
          pc += 3;
          break;

        case 17: // call: 17 a
          stack.addFirst(pc+2);
          pc = res(a);
          break;

        case 18: // ret: 18
          pc = stack.isEmpty() ? Integer.MAX_VALUE : stack.pollFirst(); 
          break;

        case 19: // out: 19 a
          String str = Character.toString((char)res(a));
          if (debug) {
            out.append(str);
          } else {
            System.out.print(str);
          }
          pc += 2;
          break;

        case 20: // in: 20 a 
          mem[a] = System.in.read();
          pc += 2;
          break;

        case 21:// noop: 21
          pc++;
          break;

        default:
          System.out.println("Unknown instruction: " + mem[pc]);
          pc++;
      }
    }
    System.out.println(out.toString());
  }
  
  public static void main(String[] args) throws IOException {
    byte[] bytes = Files.readAllBytes(Paths.get(args[0]));
    
    ByteBuffer leBuf = ByteBuffer.wrap(bytes).order(ByteOrder.LITTLE_ENDIAN);
    int[] bin = new int[bytes.length/2];
    for (int i = 0; i < bin.length; i++) {
      int b = Short.toUnsignedInt(leBuf.getShort(i*2));
      System.out.println(i + ": " + b);
      assert b >= 0 && b < 32776;
      bin[i] = b;
    }
    new Vm(bin).run();
  }
  
}

