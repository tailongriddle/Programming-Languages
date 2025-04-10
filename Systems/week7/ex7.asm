.text # .text means that the following code is in the text section
main:
    li a0, 5
    li a1, 8
    li a2, 10

    addi sp, sp, -12
    sw a0, 0(sp)
    sw a1, 4(sp)
    sw a2, 8(sp)

    jal ra, addThree #jump and link
    # jal addThree
    nop

    # restore 
    lw a0, 0(sp)
    lw a1, 4(sp)
    lw a2, 8(sp)
    addi sp, sp, 12 # reset the stack pointer to where it was before

    beq zero, zero, exit

addThree:
# assume a0, a1, and a2 hold arguments
# return result in a0
    add a0, a0, a1
    add a0, a0, a2
    jalr zero, 0(ra)
    # ret 

exit:
    nop 