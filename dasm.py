import argparse

parser = argparse.ArgumentParser(description='Disassemble a synacor binary.')
parser.add_argument('file', metavar='FILE', type=str, nargs=1,
                    help='The memory of the binary')
args = parser.parse_args()

fileName = args.file[0]
print('Reading from {}'.format(fileName))

def read():
    with open(fileName, 'rb') as f:
        bytes = f.read(2)
        while bytes:
            n = (bytes[0] << 8) + (bytes[1])
            yield n
            bytes = f.read(2) 


mem_stream = read()
mem = '0x{1:04x}: 0x{0:04x} ({0:c})'
no_op = '0x{1:04x}: {0:4s}'
one_op = '0x{1:04x}: {0:4s} 0x{2:04x}'
one_op_chr = '0x{1:04x}: {0:4s} 0x{2:04x} {2:c}'
two_ops = '0x{1:04x}: {0:4s} 0x{2:04x} 0x{3:04x}'
three_ops = '0x{1:04x}: {0:4s} 0x{2:04x} 0x{3:04x} 0x{3:04x}'

op = next(mem_stream, None)
addr = 0
while op != None:
    if op == 0:
        print(no_op.format('halt', addr))
        addr += 1
    elif op == 1:
        a = next(mem_stream)
        b = next(mem_stream)
        print(two_ops.format('set', addr, a, b))
        addr += 3
    elif op == 2:
        a = next(mem_stream)
        print(one_op.format('push', addr, a))
        addr += 2
    elif op == 3:
        a = next(mem_stream)
        print(one_op.format('pop', addr, a))
        addr += 2
    elif op == 4:
        a = next(mem_stream)
        b = next(mem_stream)
        c = next(mem_stream)
        print(three_ops.format('eq', addr, a, b, c))
        addr += 4
    elif op == 5:
        a = next(mem_stream)
        b = next(mem_stream)
        c = next(mem_stream)
        print(three_ops.format('gt', addr, a, b, c))
        addr += 4 
    elif op == 6:
        a = next(mem_stream)
        print(one_op.format('jmp', addr, a))
        addr += 2
    elif op == 7:
        a = next(mem_stream)
        b = next(mem_stream)
        print(two_ops.format('jt', addr, a, b))
        addr += 3
    elif op == 8:
        a = next(mem_stream)
        b = next(mem_stream)
        print(two_ops.format('jf', addr, a, b))
        addr += 3
    elif op == 9:
        a = next(mem_stream)
        b = next(mem_stream)
        c = next(mem_stream)
        print(three_ops.format('add', addr, a, b, c))
        addr += 4
    elif op == 10:
        a = next(mem_stream)
        b = next(mem_stream)
        c = next(mem_stream)
        print(three_ops.format('mult', addr, a, b, c))
        addr += 4
    elif op == 11:
        a = next(mem_stream)
        b = next(mem_stream)
        c = next(mem_stream)
        print(three_ops.format('mod', addr, a, b, c))
        addr += 4
    elif op == 12:
        a = next(mem_stream)
        b = next(mem_stream)
        c = next(mem_stream)
        print(three_ops.format('and', addr, a, b, c))
        addr += 4
    elif op == 13:
        a = next(mem_stream)
        b = next(mem_stream)
        c = next(mem_stream)
        print(three_ops.format('or', addr, a, b, c))
        addr += 4
    elif op == 14:
        a = next(mem_stream)
        b = next(mem_stream)
        print(two_ops.format('not', addr, a, b))
        addr += 3
    elif op == 15:
        a = next(mem_stream)
        b = next(mem_stream)
        print(two_ops.format('rmem', addr, a, b))
        addr += 3
    elif op == 16:
        a = next(mem_stream)
        b = next(mem_stream)
        print(two_ops.format('wmem', addr, a, b))
        addr += 3
    elif op == 17:
        a = next(mem_stream)
        print(one_op.format('call', addr, a))
        addr += 2
    elif op == 18:
        print(no_op.format('ret', addr))
        addr += 1
    elif op == 19:
        a = next(mem_stream)
        print(one_op_chr.format('out', addr, a))
        addr += 2
    elif op == 20:
        a = next(mem_stream)
        print(one_op.format('in', addr, a))
        addr += 2
    elif op == 21:
        print(no_op.format('noop', addr))
        addr += 1
    else:
        print(mem.format(op, addr))
        addr += 1 
        
    op = next(mem_stream, None)

