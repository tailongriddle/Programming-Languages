#include <stdio.h>
#include <math.h>

// define a bitSet type
typedef unsigned short bitSet; // 16 bits

// functions



#include <stdio.h>

typedef unsigned short bitSet; // 16 bits

bitSet makeBitSet() {
    return 0;
}

void displayBitSet(bitSet bs) {
    printf("Bitset: ");
    for (int i = 15; i >= 0; i--) {
        int bit = (bs >> i) & 1;
        printf("%d", bit);
    }
    printf("\n");
}

void setBit(bitSet* bs, int index) {
    *bs |= (1 << index); // set the bit at index to 1
    // shifts binary number 1 (0001) to the left by index
    // example: if index is 3, 0001 becomes 1000
    // this is a bit mask, where the only bit that is 1 is at the index
    // then we use the bitwise OR operator (|) to set (=) the bits
    // if either bit is 1, the corresponding bit of the result is set to 1
    
}

void clearBit(bitSet* bs, int index) {
    *bs &= ~(1 << index); // set the bit at index to 0    
    
}

int bitValue(bitSet bs, int index) {
    return (bs >> index) & 1; // get the value of the bit at index
}

int main() {
    bitSet test = makeBitSet(); // 0000000000000000
    displayBitSet(test); // 0000000000000000

    setBit(&test, 1); // 0000000000000001
    displayBitSet(test); // 0000000000000001

    clearBit(&test, 0); // 0000000000000000
    displayBitSet(test); // 0000000000000000

    return 0;
}
