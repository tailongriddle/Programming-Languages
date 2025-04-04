#include <stdio.h>
#include <stdlib.h>

typedef union floatU {
    unsigned int bits;
    float theFloat;
} floatU;

// Takes a float and displays the 32 bits that represent it
// sign bit, exponent bits, mantissa bits separated by a space
void displayFloatAsBits(float f){
    floatU u; // create a floatU union
    u.theFloat = f; // set the float in the union to the input float
    unsigned int* i = &(u.bits); // cast the float to an unsigned int
    for(int j = 31; j >= 0; j--){ // for each bit in the unsigned int...
        if (j == 30){
             printf(" "); // print a space 
        }
        if (j == 22) {
            printf(" "); // print a space
        }
        int bit = (*i >> j) & 1; // shift the bits to the right by j, then compare the result to 1
        printf("%d", bit); // print the bit
    }
    printf("\n"); // print a newline
}

// Takes a string of bits and returns the float that it represents
float makeFloatFromBits(char* f){
    floatU u; // create a floatU union
    int sign; // initialize sign
    if (*f == '-') { // if the first character is a minus sign...
        sign = -1; // set sign to -1
    } else {
    sign = 1; // otherwise, set sign to 1
    } 
    
    f++; // increment f

    u.theFloat = 0.0f; // set the float in the union to 0
    while (*f != '.') { // while the current character is not a period...
        u.theFloat = u.theFloat * 2 + (*f - '0'); // multiply the float by 2, then add the current character minus '0'
        f++; // increment f
    }

    f++; // increment f

    float fracPart = 0.5f; // set fracPart to 0.5
    while (*f != '\0') { // while the current character is not the null terminator...
        u.theFloat += fracPart * (*f - '0'); // add fracPart times the current character minus '0' to the float
        fracPart = fracPart / 2; // divide fracPart by 2
        f++; // increment f
    }
      
    return u.theFloat * sign; // return the float times the sign

}


// Test the functions
int main(){
    displayFloatAsBits(-5.8125);
    displayFloatAsBits(5);
    printf("%f\n",makeFloatFromBits("+101.1101"));
    printf("%f\n",makeFloatFromBits("-101.1101")); // should equal -5.8125

    return 0;
}