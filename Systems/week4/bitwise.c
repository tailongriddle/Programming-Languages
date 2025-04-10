#include <stdio.h>

int main(){

    char x = 126; // signed -> 0-8, unisgned -> 0-7 with 3 bits
    x = x + 2; // 128
    printf("%d\n", x); // 128 is out of bounds, so it wraps around to -128

    int a = 7;
    int b = 5;
    int c = a&b; // bitwise AND - compares bits, if both bits are same, result is 1
    int d = ~a; //bitwise NOT - flips all bits, 1s to 0s, 0s to 1s
    int e = a^b; // bitwise XOR - compares bits, if bits are different, result is 1
    int f = a >> 1; // bitwise right shift - shifts bits to the right by 1
    int g = b << 1; // bitwise left shift - shifts bits to the left by 1
    int h = a | b; // bitwise OR - compares bits, if either bit is 1, result is 1
   
    printf("%d\n", c);
    printf("%d\n", d);
    printf("%d\n", e);
    printf("%d\n", f); // halved a (integer division rounds down)
    printf("%d\n", g); // doubled b

    return 0;
}

// Pixels have alpha value - transparency 
// 2^8 = 255 - 8 bits for each color channel
// pixels are usually packed into an int (4 bytes)
// One byte = 8 bits
//'int p;'
//'p >> 8' does not mutate p, it just shifts the bits to the right by 8
// 'p = p >> 8' will mutate p
// to isolate green: g = (p>>>8) & 255;
// 255 is the same as 11111111
// 255 is a mask that isolates the green channel
// you can also do: g = (p>>>8) & 0xFF;

// lower row of binary arithmetic is a mask 

// +2 or -2 = sign magnitude
// two representations for 0 (positive and negative) 
// 2's complement - 1's complement + 1
// 2's complement is the most common representation for negative numbers
// 1's complement is the bitwise NOT of a number
// how-to: 1. flip all bits 2. add 1
// you want to use unsigned in C most of the time
// with signed, when you shift left, you lose the sign bit
// with unsigned, you don't lose the sign bit

// big/little endian - how to store bytes in memory
// which end of the hard boiled egg do you crack first 
// big endian - most significant byte first
// little endian - least significant byte first
// python stores in little endian

// Floating Point Representation (decimal numbers)
// 5.75 -> 101.11 (binary)
// 101.11 = 1.0111 * 2^2 (we want there be to be one digit in front of the decimal)
// don't need to store the '1' in the front 
// 3 bits to store the exponent (2^3 = 8), 5 bits to store the rest 
// 2^2 - 1 = 3 (exponent - bias)
// after the ., the numbers are 1/2, 1/4, 1/8, 1/16, etc.
// 5.8125 -> 101.1101 (binary)
// can represent 1/3 perfectly in binary, but not 1/5

// when you go to a double, you get more precision
