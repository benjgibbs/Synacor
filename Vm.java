import java.io.*;
import java.nio.*;
import java.nio.file.*;
import java.util.*;

class Vm {
  int pc = 0;
  final int[] reg = new int[8];
  final Deque<Integer> stack = new LinkedList<>();
  final int [] bin;
  static final int MAX = 32768;
   
  Vm(int[] bin) {
    this.bin = bin;
  }
  
  int res(int i) {
    if (i >= MAX) {
      return reg[i - MAX];
    }
    return i;
  }

  int reg(int r) {
    return r - MAX;
  }

  void run() {
    System.out.println("Starting");
    StringBuilder out = new StringBuilder();
    while (pc < bin.length) {
      System.out.println("pc: " + pc + " " + 
          Arrays.toString(Arrays.copyOfRange(bin, pc, pc + 4)) + "\treg:" + 
          Arrays.toString(reg) + "\tstack: " + stack);
      int a = pc + 1 < bin.length ?  bin[pc + 1] : 0;
      int b = pc + 2 < bin.length ?  bin[pc + 2] : 0;
      int c = pc + 3 < bin.length ?  bin[pc + 3] : 0;
      switch (bin[pc]) { 
        case 0: // halt: 0
          pc = Integer.MAX_VALUE;
          break;

        case 1: // set: 1 a b
          reg[reg(a)] = res(b);
          pc += 3;
          break;

        case 2: // push: 2 a
          stack.addFirst(res(a));
          pc += 2;
          break;
        
        case 3: // pop: 2 a
          reg[reg(a)] = stack.pollFirst();
          pc += 2;
          break;

        case 4: // eq: 4 a b c
          reg[reg(a)] = (res(b) == res(c) ? 1 : 0);
          pc += 4; 
          break;
        
        case 5: // gt: 5 a b c
          reg[reg(a)] = (res(b) >  res(c) ? 1 : 0);
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
          reg[reg(a)] = (b + c) % MAX;
          pc += 4; 
          break;

        case 10: // mult: 10 a b c
          reg[reg(a)] = (b * c) % MAX;
          pc += 4; 
          break;
        
        case 11: // mod: 11 a b c
          reg[reg(a)] = b % c;
          pc += 4; 
          break;

        case 12: // and: 12 a b c
          reg[reg(a)] = res(b) & res(c);
          pc += 4;
          break;
        
        case 13: // or: 13 a b c
          reg[reg(a)] = res(b) | res(c);
          pc += 4;
          break;
        
        case 14: // not: 14 a b
          reg[reg(a)] = (0x7FFF & ~res(b));
          pc += 3;
          break;
        
        case 15: // rmem: 15 a b
          if 
          bin[a] = bin[b];
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
          out.append(Character.toString((char)res(a)));
          pc += 2;
          break;

        case 21:// noop: 21
          pc++;
          break;

        default:
          pc++;
          System.out.println("Unknown instruction");

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

