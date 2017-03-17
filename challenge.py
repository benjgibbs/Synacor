from sys import stdout
from sys import stdin

MAX = 32768

def add(a,b):
    return (a+b) % MAX

def sub(a,b):
    return (a - b) % MAX

def mult(a,b):
    return (a * b) % MAX

def div(a,b):
    return (a / b) % MAX

assert add(32758,15) == 5

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
    def __init__(self, prog):
        self.reg = 8 * [0]
        self.mem = list(prog) #= [0] * 2**15
        self.stack = list()
        self.pc = 0  
    
    # halt: 0
    def halt(self,tr):
        print ('End')
        tr.write('halt\n' )
        self.pc = MAX
        
    # set: 1 a b
    def set(self, tr):
        a, b = self.reg_addr(1), self.read(2)
        tr.write('set: %d, %d\n' % (a, b) )
        self.reg[a] = b
        self.pc += 3
    
    # push: 2 a
    def push(self, tr):
        a = self.read(1)
        tr.write('push: %d\n' % a )
        self.stack.append(a)
        self.pc += 2
    
    # pop: 3 a
    def pop(self, tr):
        a = self.reg_addr(1)
        p = self.stack.pop()
        tr.write('pop: %d (%d)\n' % (a, p) )
        self.reg[a] = p
        self.pc += 2

    # eq: 4 a b c
    def eq(self, tr):
        a, b, c = self.reg_addr(1), self.read(2), self.read(3)
        tr.write('eq: %d, %d, %d\n' % (a, b, c) )
        self.reg[a] = 1 if b == c else 0
        self.pc += 4
        
    # gt: 5 a b c
    def gt(self, tr):
        a, b, c = self.reg_addr(1), self.read(2), self.read(3)
        tr.write('gt: %d, %d, %d\n' % (a, b, c))
        self.reg[a] = 1 if b > c else 0
        self.pc += 4
    
    # jmp: 6 a
    def jmp(self, tr):
        a = self.read(1)
        tr.write('jmp: %d\n' % (a))
        self.pc = a

    # jt: 7 a b
    def jt(self, tr):
        a, b = self.read(1), self.read(2)
        tr.write('jt: %d %d\n' % (a, b))
        if a != 0:
            self.pc = b            
        else:
            self.pc += 3
            
    # jf: 8 a b
    def jf(self, tr):
        a, b = self.read(1), self.read(2)
        tr.write('jf: %d %d\n' % (a, b))
        if a == 0:
            self.pc = b            
        else:
            self.pc += 3
    
    # add: 9 a b c
    # assign into <a> the sum of <b> and <c> (modulo 32768)
    def add(self, tr):
        a, b, c = self.reg_addr(1), self.read(2), self.read(3)
        tr.write('add: %d, %d, %d\n' % (a, b, c) )
        self.reg[a] = add(b,c)
        self.pc += 4

    # mult: 10 a b c
    # store into <a> the product of <b> and <c> (modulo 32768)
    def mult(self,tr):
        a, b, c = self.reg_addr(1), self.read(2), self.read(3)
        tr.write('mult: %d, %d, %d\n' % (a, b, c) )
        self.reg[a] = mult(b,c)
        self.pc += 4

    # mod: 11 a b c
    # store into <a> the remainder of <b> divided by <c>
    def mod(self,tr):
        a, b, c = self.reg_addr(1), self.read(2), self.read(3)
        tr.write('mod: %d, %d, %d\n' % (a, b, c) )
        self.reg[a] = b % c
        self.pc += 4

    # and: 12 a b c
    # stores into <a> the bitwise and of <b> and <c>
    def andfn(self, tr): 
        a, b, c = self.reg_addr(1), self.read(2), self.read(3)
        tr.write('add: %d, %d, %d\n' % (a, b, c) )
        self.reg[a] = b & c
        self.pc += 4

    # or: 13 a b c
    # stores into <a> the bitwise or of <b> and <c>
    def orfn(self, tr): 
        a, b, c = self.reg_addr(1), self.read(2), self.read(3)
        tr.write('or: %d, %d, %d\n' % (a, b, c) )
        self.reg[a] = b | c
        self.pc += 4

    # not: 14 a b
    # stores 15-bit bitwise inverse of <b> in <a>
    # '{0:b}'.format(~int("1010",2) & 32767) -> '111111111110101'
    def notfn(self, tr): 
        a, b = self.reg_addr(1), self.read(2)
        tr.write('not: %d, %d\n' % (a, b) )
        self.reg[a] = ~b & (2**15-1)
        self.pc += 3
    
    # rmem: 15 a b
    # read memory at address <b> and write it to <a>  (mod 32768)
    def rmem(self, tr): 
        a, b = self.mem[self.pc + 1], self.mem[self.pc + 2]
        tr.write('rmem: %d, %d\n' % (a, b))
        self.reg[a % MAX] = \
            self.mem[b] if b < MAX else self.mem[self.reg[b % MAX]]
        self.pc += 3

    # wmem: 16 a b
    # write the value from <b> into memory at address <a>
    def wmem(self, tr): 
        a, b = self.mem[self.pc + 1], self.mem[self.pc + 2]
        tr.write('wmem: %d, %d\n' % (a, b))
        v = b if b < MAX else self.reg[b % MAX]

        if a < MAX:
            self.mem[a] = v
        else:
            self.mem[self.reg[a % MAX]] = v

        self.pc += 3

    # call: 17 a
    # write the address of the next instruction to the stack and jump to <a>
    def call(self, tr):
        a = self.read(1)
        tr.write('call: %d\n' % (a) )
        self.stack.append(self.pc+2)
        self.pc = a

    # ret: 18
    # remove the top element from the stack and jump to it; empty stack = halt
    def ret(self, tr):
        self.pc = self.stack.pop()
        tr.write('ret: %d\n' % (self.pc) )
    
    # out: 19 a
    def out(self, tr):
        a = self.read(1)
        tr.write('out: %d\t%c\n' % (a, a) )
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
        self.reg[a] = ord(c)
        self.pc += 2
    
    # noop: 21
    def noop(self, tr):
        tr.write('noop\n')
        self.pc += 1
    
    
  
    
    #############################################################
    
    def read(self, offset):
        a = self.mem[self.pc + offset]
        if a < MAX:
            return a
        return self.reg[a % MAX]
    
    def reg_addr(self, offset):
        return self.mem[self.pc + offset] % MAX
    
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

        with open('trace', 'w') as tr:
            while self.pc < MAX:
                i = self.mem[self.pc]
                tr.write('reg: %32s [%d] %d=' % (self.reg, self.pc, i))
                if  i < len(fn_table):
                    fn_table[i](tr)
                else:
                    self.pc = MAX
                    print('Unknown op code: ' + str(i))
    
    
# prog = [9,32768,32769,4,19,32768]
# prog = [1,0,2,1,1,32768,0]
prog = load()
vm = Vm(prog)
vm.run()
