# short circuit evaluation
# if ((x>=10) && (y<=20)){
#    x = y;
# }
# while ((i<n) && (array[i] != value)) 
#    i++;
#}

# if (i==n){
#    dfsd
#    } else {

#}

li x10, 0x12345678

li x10, 15  # x
li x11, 15  # y

li t5, 10
blt x10, t5, skip

li t5, 20
bge x11, t5, skip

#add x10, x0, x11
mv x10, x11

skip:
nop #end of program

