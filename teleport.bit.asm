
0x178b: jt   0x8000 0x1793
0x178e: add  0x8000 0x8001 0x8001
0x1792: ret 
0x1793: jt   0x8001 0x17a0
0x1796: add  0x8000 0x8000 0x8000
0x179a: set  0x8001 0x8007
0x179d: call 0x178b
0x179f: ret 
0x17a0: push 0x8000
0x17a2: add  0x8001 0x8001 0x8001
0x17a6: call 0x178b
0x17a8: set  0x8001 0x8000
0x17ab: pop  0x8000
0x17ad: add  0x8000 0x8000 0x8000
0x17b1: call 0x178b
0x17b3: ret 