#include <riscv.h>
# lab6

# The a0 register code needed to turn on an LED is 0x100
# The a1 register sets the (x,y) location in the grid to turn on
# The a2 register sets the color of the LED
# Red is in bits 23-16, g in bits 15-8, and b in bits 7-0
# li is a pseudo instruction that loads the immediate value into the register

# la: loads the address of the label into the register
# li: loads the immediate value into the register
# lw: loads the value at the address in the register into the register
# bq: branch if equal, jumps to the label if the two registers are equal
# beqz: branch if equal to zero, jumps to the label if the register is zero


# li a0, 0x100
# li a1, 0x00050012 # (5, 18) because 5*32 + 18 = 178
# li a2, 0x00FF0000

# ecall

# nop


.data
grid:
 .word 0xFFFFFC00
 .word 0xFFFFFE00
 .word 0xFFFFFF00
 .word 0x3FFFFF00

 .word 0x3F003F00
 .word 0x3F003F00
 .word 0x3F3F3F3F
 .word 0x3F3F3F3F

 .word 0x3F3F3F3F
 .word 0x3F3F3F3F
 .word 0x3F3F3F3F
 .word 0x3F3F3F3F

 .word 0x3F3F3F3F
 .word 0x3F3F3F3F
 .word 0x3F3F3F3F
 .word 0x3F3F3F3F

 .word 0x3F3F3F3F
 .word 0x3F3F3F3F
 .word 0x3F003F3F
 .word 0x3F003F3F

 .word 0x3FFFFF3F
 .word 0xFFFFFF3F
 .word 0xFFFFFE3F
 .word 0xFFFFFC3F

 .word 0x0000007F
 .word 0x000000FF
 .word 0x003FFFFF
 .word 0x003FFFFF

 .word 0x001FFFFE
 .word 0x000FFFFC

.text
main:
    la x2, grid # load the address of the grid (x0 = grid address)
    li x9, 1 # load constant(x0 = 1)
    li x1, 0 # load row incrementer (x1 = 0)
    li x6, 30 # load row terminator (x2 = 30)
    li x5, 0 # load column incrementer (x5 = 0)
    li x7, 32 # load column terminator (x7 = 32)
    

read_row1:
    beq x1, x6, end # if row incrementer = row terminator, jump to end
   
    lw x3, 0(x2) # load the value at the address in x0 into x3

    li x5, 0 # load column incrementer (x5 = 0)
    j read_columns # jump to read_columns

read_rows:
    addi x1, x1, 1 # increment the row incrementer
    addi x2, x2, 4 # increment the grid address by 4
    j read_row1 # jump to read_row1

read_columns:
    beq x5, x7, read_rows # if column incrementer = column terminator, jump to read_rows 
    srli x8, x3, 31 # shift the value in x3 right by 31 bits and store in x8

    beqz x8, gold # if x8 = 0, jump to gold
    beq x8, x9, red # if x8 = 1, jump to red


red: #LED crimson (0xBA0C2F) 
    li x10, 0x100 # load the LED code into x10
    li x11, 0 # load the (x,y) location into x11
    slli x11, x5, 16 # shift the value in x5 left by 16 bits and store in x11
    or x11, x11, x1 # bitwise OR the value in x1 with the value in x11 and store in x11
    li x12, 0xBA0C2F # load the color of the LED into x12

    mv a0, x10 # load the LED code into a0
    mv a1, x11 # load the (x,y) location into a1
    mv a2, x12 # load the color of the LED into a2

    addi x5, x5, 1 # increment the column incrementer
    slli x3, x3, 1 # shift the value in x3 left by 1 bit and store in x3
    #nop

    ecall # turn on the LED
    j read_columns # jump to read_columns
   
gold: #LED gold (0xA89968)
    li x10, 0x100 # load the LED code into x10
    li x11, 0 # load the (x,y) location into x11
    slli x11, x5, 16 # shift the value in x5 left by 16 bits and store in x11
    or x11, x11, x1 # bitwise OR the value in x1 with the value in x11 and store in x11
    li x12, 0xA89968 # load the color of the LED into x12

    mv a0, x10 # load the LED code into a0
    mv a1, x11 # load the (x,y) location into a1
    mv a2, x12 # load the color of the LED into a2

    addi x5, x5, 1 # increment the column incrementer
    slli x3, x3, 1 # shift the value in x3 left by 1 bit and store in x3
    #nop

    ecall # turn on the LED
    j read_columns # jump to read_columns
   


end:
    # li a7, 10 # load the exit code into a7
    nop



