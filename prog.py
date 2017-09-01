

max = False
a = 4
b = 1

h = 2 ** 15 if max else 0

s = []
while a != 0:
    if b == 0:
        a = 2 * a
        b = h
    else:
        s.append(a)
        b = 2 * b

a == 2 * b    
print('a={:}, b={:}'.format(a,b))
