## Memory of use
3167 - There are / is exits
6143 - Foothills          [20100] 
6351 - South Foothills
6442 - Dark cave          [23300, 28810]
6598 - Dark cave 2
6712 - Dark cave 3

16707 = Number on moss floor
16792 - Vault antechamber - number here


## Functions

Loop ? 
  Call Contents of R1 - 0x8001 
  0x05b2 - Set R0 to R6, R5 to R1
           Read from R0 and write to R4
           set R1 = 0
           :start
           R3 = 1 + 1
           R0 = R3 > R3
           if R0 jump to end
           R3 = R3 + R3
           R0 = R3
           Call R5
           R1 = R1 + R1
           if R1 !=0 jump to :start
           :end

  Used with
    0x05f8 = Out R0


read input
  call 0x06e7 with 0x0020 and 0x6576 (size and location?)

0x0634 - 

0x0645 - some kind of comparision

inventoy
call 0x0623 with 0x6576 0x0020
call 0x0607 



## Trace Events



