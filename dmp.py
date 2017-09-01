import argparse

parser = argparse.ArgumentParser(description='Extract strings from a synacor binary.')
parser.add_argument('file', metavar='FILE', type=str, nargs=1, help='The memory of the binary')
args = parser.parse_args()

fileName = args.file[0]
print('Reading from {}'.format(fileName))

def read(fileName):
    with open(fileName, 'rb') as f:
        bytes = f.read(2)
        while bytes:
            n = (bytes[0] << 8) + (bytes[1])
            yield n
            bytes = f.read(2) 

def chunk(stream, sz):
    res = list()
    for i in range(sz):
        v = next(stream, None)
        if v == None:
                break
        res.append(v)
    return res

stream = read(fileName)
addr = 0
WIDTH = 16
while True:
    ch = chunk(stream, WIDTH)
    if len(ch) == 0:
        break
    
    print('0x{0:04x}: '.format(addr), end='')
    for  i in range(len(ch)):
        c = ch[i]
        print('0x{0:04x}'.format(c), end=' ')
    print('')

    addr += WIDTH
