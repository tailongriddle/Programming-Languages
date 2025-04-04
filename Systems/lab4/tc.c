#include <stdio.h>

// Display an integer as a series of bits
void displayIntAsBits(int i){
    for(int j = 31; j >= 0; j--){ // for each bit in the integer...
        if (j % 4 == 3) printf(" "); // print a space every 4 bits 
        int bit = (i >> j) & 1; // shift the bits to the right by j, then compare the result to 1
        printf("%d", bit); // print the bit
    }
    printf("\n"); // print a newline
    
}

// Make an integer from a series of bits of any length, either positive or negative integers
int makeIntFromBits(char* i){
    int result = 0; // initialize the result to 0

    for(int j = 0; i[j] != '\0'; j++){ // for each bit in the integer...
        result = result << 1; // shift the result to the left by 1
        if(i[j] == '1') result = result | 1; // if the bit is 1, set the rightmost bit of the result to 1
    }

    if (i[0] == '-') result = ~result + 1; // if the integer is negative, flip all the bits and add 1
    
    printf("%d\n", result); // print the result
    return result; // return the result
}

int main(){
    displayIntAsBits(5);
    displayIntAsBits(-9);

    makeIntFromBits("+101");
    makeIntFromBits("-1001");
    return 0;
}