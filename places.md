## Instructions
East off the bridge to get lantern

Bottom of ladder: West South North


blue:     9
red:      2
shiny:    5
concave:  7
corroded: 3
9    2    5      7     3
 _ + _ * \_^2 + \_^3 - _ = 399


Rig teleporter

>0x1566=0x6
>0x1567=0x157a

izXrYkkltRim

# Orb

22 on pedestal
east has -
east has 9 (13)
east has x
north has 18 (234)

22 on pedestal 
north has +
north has 4 (26)
south has +
north has 4 (30)
east has (*)
north has (*)

30 on vault


##Codes

In arch-spec:       tZuCObbDMEMN
Start of challenge: EJjxSEujhzMW
Self test complete: JhlqOSfLPgMQ
On tablet:          eSaTzvAsQVhd
Get Oil:            fjYMgZJpmWWb
Teleporter:         ODApGLANaLcx
Post teleport:      izXrYkkltRim


Bad code:           Teleporter: WHjPkYYZRtWS, Mirror: WdIowXAddbYH

## Memory of use
0x17f2 - code decrypting buffer

0x6577 to 0x6596 - in buffer

0x657b - Inventory?? - unlikely



## Assmebly to optimise
A = 4
B = 1
H = ?

Double B until it wraps, pushing A each time
Double A, and set B to H
Double B until it wraps, pushing A each time




## Functions

0x05b2 - print out contents of r2?


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



