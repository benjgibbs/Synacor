from sys import stdout
from sys import stdin
import struct
import io
import readline

MAX = 2 ** 15

def load():
    with open('challenge.bin', 'rb') as f:
        while True:
            b = f.read(2)
            if b:
                n = b[0] + (b[1] << 8)
                yield n
            else:
                break

class Vm:
    def __init__(self, prog, mem):
        self.trace = False
        self.reg = 8 * [0]
        
        self.mem = mem

        for i in range(2**15):
            self.write_mem(i,0)
        
        i = 0
        for p in prog:
            self.write_mem(i, p)
            i += 1

        self.stack = list()
        self.pc = 0  

    # halt: 0
    def halt(self,tr):
        print ('End')
        tr.write('halt' )
        self.pc = MAX

    # set: 1 a b
    def set(self, tr):
        a, b = self.reg_addr(1), self.read(2)
        tr.write('set:       R%d, 0x%04x' % (a, b) )
        self.reg[a] = b
        self.pc += 3
    
    # push: 2 a
    def push(self, tr):
        a = self.read(1)
        tr.write('push:  0x%04x' % a )
        self.stack.append(a)
        self.pc += 2
    
    # pop: 3 a
    def pop(self, tr):
        a = self.reg_addr(1)
        p = self.stack.pop()
        tr.write('pop:       R%d (0x%04x)' % (a, p) )
        self.reg[a] = p
        self.pc += 2

    # eq: 4 a b c
    def eq(self, tr):
        a, b, c = self.reg_addr(1), self.read(2), self.read(3)
        tr.write('eq:        R%d, 0x%04x, 0x%04x' % (a, b, c) )
        self.reg[a] = 1 if b == c else 0
        self.pc += 4
        
    # gt: 5 a b c
    def gt(self, tr):
        a, b, c = self.reg_addr(1), self.read(2), self.read(3)
        tr.write('gt:        R%d, 0x%04x, 0x%04x' % (a, b, c))
        self.reg[a] = 1 if b > c else 0
        self.pc += 4
    
    # jmp: 6 a
    def jmp(self, tr):
        a = self.read(1)
        tr.write('jmp:   0x%04x' % (a))
        self.pc = a

    # jt: 7 a b
    def jt(self, tr):
        a, b = self.read(1), self.read(2)
        tr.write('jt:    0x%04x, 0x%04x' % (a, b))
        if a != 0:
            self.pc = b            
        else:
            self.pc += 3
            
    # jf: 8 a b
    def jf(self, tr):
        a, b = self.read(1), self.read(2)
        tr.write('jf:    0x%04x, 0x%04x' % (a, b))
        if a == 0:
            self.pc = b            
        else:
            self.pc += 3
    
    # add: 9 a b c
    # assign into <a> the sum of <b> and <c> (modulo 32768)
    def add(self, tr):
        a, b, c = self.reg_addr(1), self.read(2), self.read(3)
        tr.write('add:       R%d, 0x%04x, 0x%04x' % (a, b, c) )
        self.reg[a] = (b+c) % MAX
        self.pc += 4

    # mult: 10 a b c
    # store into <a> the product of <b> and <c> (modulo 32768)
    def mult(self,tr):
        a, b, c = self.reg_addr(1), self.read(2), self.read(3)
        tr.write('mult:      R%d, 0x%04x, 0x%04x' % (a, b, c) )
        self.reg[a] = (b * c) % MAX
        self.pc += 4

    # mod: 11 a b c
    # store into <a> the remainder of <b> divided by <c>
    def mod(self,tr):
        a, b, c = self.reg_addr(1), self.read(2), self.read(3)
        tr.write('mod:       R%d, 0x%04x, 0x%04x' % (a, b, c) )
        self.reg[a] = b % c
        self.pc += 4

    # and: 12 a b c
    # stores into <a> the bitwise and of <b> and <c>
    def andfn(self, tr): 
        a, b, c = self.reg_addr(1), self.read(2), self.read(3)
        tr.write('add:       R%d, 0x%04x, 0x%04x' % (a, b, c) )
        self.reg[a] = b & c
        self.pc += 4

    # or: 13 a b c
    # stores into <a> the bitwise or of <b> and <c>
    def orfn(self, tr): 
        a, b, c = self.reg_addr(1), self.read(2), self.read(3)
        tr.write('or:        R%d, 0x%04x, 0x%04x' % (a, b, c) )
        self.reg[a] = b | c
        self.pc += 4

    # not: 14 a b
    # stores 15-bit bitwise inverse of <b> in <a>
    # '{0:b}'.format(~int("1010",2) & 32767) -> '111111111110101'
    def notfn(self, tr): 
        a, b = self.reg_addr(1), self.read(2)
        tr.write('not:       R%d, 0x%04x' % (a, b) )
        self.reg[a] = ~b & (2**15-1)
        self.pc += 3
    
    # rmem: 15 a b
    # read memory at address <b> and write it to <a>  (mod 32768)
    def rmem(self, tr): 
        a, b = self.read_mem(self.pc + 1), self.read_mem(self.pc + 2)
        tr.write('rmem:  0x%04x, 0x%04x' % (a, b))

        v = self.read_mem(b) if b < MAX else self.read_mem(self.reg[b % MAX]) 
        self.reg[a % MAX] = v
        self.pc += 3

    # wmem: 16 a b
    # write the value from <b> into memory at address <a>
    def wmem(self, tr): 
        a, b = self.read_mem(self.pc + 1), self.read_mem(self.pc + 2)
        tr.write('wmem:  0x%04x, 0x%04x' % (a, b))
        v = b if b < MAX else self.reg[b % MAX]

        if a < MAX:
            self.write_mem(a, v)
        else:
            self.write_mem(self.reg[a % MAX], v)

        self.pc += 3

    # call: 17 a
    # write the address of the next instruction to the stack and jump to <a>
    def call(self, tr):
        a = self.read(1)
        tr.write('call:  0x%04x' % (a) )
        self.stack.append(self.pc+2)
        self.pc = a

    # ret: 18
    # remove the top element from the stack and jump to it; empty stack = halt
    def ret(self, tr):
        self.pc = self.stack.pop()
        tr.write('ret:   0x%04x' % (self.pc) )
    
    # out: 19 a
    def out(self, tr):
        a = self.read(1)
        c = chr(a)

        if c == '\n':
            c = '\\n'

        tr.write('out:   0x%04x (%s)' % (a, c) )
        stdout.write('%c' % chr(a))
        self.pc += 2

     # in: 20 a
     #   read a character from the terminal and write its ascii code to <a>; 
     #   it can be assumed that once input starts, it will continue until a 
     #   newline is encountered; this means that you can safely read whole 
     # lines from the keyboard and trust that they will be fully read
    def readin(self, tr):
        a = self.reg_addr(1)
        c = stdin.read(1)

        if c == '*':
            print(self.reg[7])
            self.reg[7] = 32766 #2 ** 15
            print(self.reg[7])
        elif c == '!':
            self.trace = not self.trace
            print('trace={:b}'.format(self.trace))
        elif c == '#':
            print('pc:\t0x{:x}'.format(self.pc))
            print('reg:\t{:s}'.format(print_arr(self.reg)))
            print('stack:\t{:s}'.format(print_arr(self.stack)))

        elif c == '>':
            ln = stdin.readline()
            ps = [int(x, 16) for x in ln.strip().split('=')]
            m = ps[0]
            v = ps[1]
            print('Setting 0x{:x} to 0x{:x}'.format(m, v))
            self.write_mem(m, v)

        tr.write('in:        R%d (%3d,%c)' % (a, ord(c), c) )
        self.reg[a] = ord(c)
        self.pc += 2
    
    # noop: 21
    def noop(self, tr):
        tr.write('noop')
        self.pc += 1
  
    
    #############################################################
    
    def read(self, offset):
        a = self.read_mem(self.pc + offset)
        if a < MAX:
            return a
        return self.reg[a % MAX]
    
    def reg_addr(self, offset):
        return self.read_mem(self.pc + offset) % MAX
    
    
    def write_mem(self, addr, val):
        # All numbers are 15 bit so we read/write 2 bytes
        # print('Writing %d to %d' % (val, addr))
        addr = 2 * addr
        self.mem.seek(addr, 0)
        self.mem.write(struct.pack('>I', val)[2:])
        self.mem.seek(addr, 0)
        # print('Check %s' % self.mem.read(2))
    
    def read_mem(self, addr):
        addr = 2 * addr
        self.mem.seek(addr, 0)
        b = self.mem.read(2) 
        r = struct.unpack('>I',  2 * b'\x00' + b)[0]
        # print('Read %s =>  %d from %d' % (b, r, addr))
        return r
    
    
    #############################################################
    def run(self):
        fn_table = [
                self.halt,
                self.set,
                self.push,
                self.pop,
                self.eq,
                self.gt,
                self.jmp,
                self.jt,
                self.jf,
                self.add,
                self.mult,
                self.mod,
                self.andfn,
                self.orfn,
                self.notfn,
                self.rmem,
                self.wmem,
                self.call,
                self.ret,
                self.out,
                self.readin,
                self.noop ]

        self.write_mem(0x657b, 0xd) 

        with open('./trace', 'w') as tr:
            while self.pc < MAX:
                i = self.read_mem(self.pc)
                pc2 = self.pc
                
                buf = io.StringIO()
                if  i < len(fn_table):
                    fn_table[i](buf)
                    if self.trace:
                        buf.seek(0)
                        instr = buf.readline()
                        reg_str = print_arr(self.reg)
                        stack_str = print_arr(self.stack)
                        tr.write('[Ox{:04x}] {:2d}={:30s} {:s} {:s}\n'.format(pc2, i, instr, reg_str, stack_str))
                else:
                    self.pc = MAX
                    print('Unknown op code: ' + str(i))

def print_arr(arr):
    return str(['0x{:04x}'.format(x) for x in arr])

prog = load()

with open('/Volumes/RAMDisk/mem', 'w+b', buffering=0) as mem:
    vm = Vm(prog, mem)
    vm.run()
