#include <stdio.h>
#include <stdlib.h>

// GATES

// nand gate using truth table
// logic: returns true if both a and b are false and vice versa
// a, b: input bits
// returns: output bit of nand
int nand(int a, int b) {
    if (a == 1) {
        if (b == 1) {
            return 0;  // return 0 if a and b are 1
        }
    }
    return 1; // return 1 in all other cases
}

// not gate using nand gates
// logic: returns true if a is false and vice versa
// a: input bit because not gates only take one input
// returns: output bit of not
int not(int a){
    int toReturn = nand(a,a); // A NAND A

    return toReturn;
}

// and gate using using nand gates
// logic: returns true if both a and b are true, false otherwise
// a, b: input bits
// returns: output bit of and
int and(int a, int b) {
    int nandPartAB = nand(a,b); // (A NAND B)
    int toReturn = nand(nandPartAB,nandPartAB); // (A NAND B) NAND (A NAND B)

    return toReturn;
}


// or gate using using nand gates
// logice: returns true if either/both a and b are true, false otherwise
// a, b: input bits
// returns: output bit of or
int or(int a, int b) {
    int nandPartA = nand(a,a); // (A NAND A)
    int nandPartB = nand(b,b); // (B NAND B)
    int toReturn = nand(nandPartA,nandPartB); // (A NAND A) NAND (B NAND B)

    return toReturn;
}

// xor gate using using nand gates
// logic: returns true only if either a or b is true, false otherwise
// a, b: input bits
// returns: output bit of or
int xor(int a, int b) {
    int nandPartAB = nand(a,b); // (A NAND B)
    int nandPartA = nand(a,nandPartAB); // (A NAND (A NAND B))
    int nandPartB = nand(b,nandPartAB); // (B NAND (A NAND B))
    int toReturn = nand(nandPartA,nandPartB); // ((A NAND (A NAND B)) NAND (B NAND (A NAND B))

    return toReturn;
}


// ADDERS

// half-adder using NAND gates
// logic: simple addition of two single bit binary numbers
// a, b: input bits
// sum, carry: values to return (passed back as parameters)
// returns: 2-bit number, and a carry 
void half_adder(int a, int b, int* sum, int* carry){

    // sum is similar to xor
    int nandPartAB = nand(a,b); // (A NAND B)
    int nandPartA = nand(a,nandPartAB); // (A NAND (A NAND B))
    int nandPartB = nand(b,nandPartAB); // (B NAND (A NAND B))
    *sum = nand(nandPartA,nandPartB); // (A NAND A) NAND (B NAND B)

    // carry is similar to and 
    int nandPartAB2 = nand(a,b); // (A NAND B)
    *carry = nand(nandPartAB2,nandPartAB2); // (A NAND B) NAND (A NAND B)

}

// full-adder using NAND gates
// logic: simple addition of three single bit binary numbers
// a, b, carry_in: input bits
// sum, carry_out: values to return (passed back as parameters)
// returns: 3-bit number, and carry_out
void full_adder(int a, int b, int carry_in, int* sum, int* carry_out){

    // sum is similar to 4 (3-input) AND gates, 3 NOT gates, and 1 (4-input) OR gate
   
    // 3 NOT gates
    int notA = nand(a,a); // oppposite of a
    int notB = nand(b,b); // opposite of b
    int notC = nand(carry_in, carry_in); // opposite of carry_in

    // 4 (3-input) AND gates
    int and1 = nand(nand(notA,notB), nand(notA,notB)); // (notA AND notB)
    int and10 = nand(nand(and1,carry_in),nand(and1,carry_in)); // (notA AND notB AND c)

    int and2 = nand(nand(notA, b), nand(notA, b)); // (notA AND b)
    int and20 = nand(nand(and2,notC),nand(and2,notC)); // (notA AND b AND notC)

    int and3 = nand(nand(a,notB), nand(a,notB)); // (a AND notB)
    int and30 = nand(nand(and3,notC),nand(and3,notC)); // (a AND notB AND notC)

    int and4 = nand(nand(a,b), nand(a,b)); // (a AND b)
    int and40 = nand(nand(and4, carry_in),nand(and4,carry_in)); // (a AND b AND c)

    // 4-input OR gate
    int or1 = nand(nand(and10,and10), nand(and20,and20)); // (and1 OR and2)
    int or2 = nand(nand(and30,and30), nand(and40,and40)); // (and3 OR and4)
    *sum = nand(nand(or1,or1), nand(or2,or2)); // (or1 OR or2)


    // carry_out is similar to 3 (2-input) AND gates and 1 (3-input) OR gate

    // 3 (2-input) AND gates
    int cand1 = nand(nand(a,b), nand(a,b)); // (a AND b)
    int cand2 = nand(nand(a,carry_in), nand(a,carry_in)); // (a AND c)
    int cand3 = nand(nand(b,carry_in), nand(b,carry_in)); // (b AND c)

    // 3-input OR gate
    int cor = nand(nand(cand1,cand1), nand(cand2,cand2));
    *carry_out = nand(nand(cor,cor),nand(cand3,cand3));

}

// 8-bit adder using NAND gates
// logic: adding multiple bit numbers
// a, b: input bits
// sum: value to return (passed back as parameter)
// returns: sum
void eight_bit_adder(int a[], int b[], int sum[]){

    int carryOut = 0; // initialize carryOut
    int carryIn = 0; // initialize carryOut
    int psum = 0; // initialize partial sum

    // add first in number
    half_adder(b[7], a[7], &psum, &carryOut); 
    sum[7] = psum; 
    psum = 0; // reset partial sum
    carryIn = carryOut;
    carryOut = 0; // reset carryOut

    // add second in number
    full_adder(b[6], a[6], carryIn, &psum, &carryOut); // pass carryIn by value
    sum[6] = psum; 
    psum = 0; // reset partial sum
    carryIn = carryOut;
    carryOut = 0; // reset carryOut

    // add third in number
    full_adder(b[5], a[5], carryIn, &psum, &carryOut); // pass carryIn by value
    sum[5] = psum; 
    psum = 0; // reset partial sum
    carryIn = carryOut;
    carryOut = 0; // reset carryOut

    // add fourth in number
    full_adder(b[4], a[4], carryIn, &psum, &carryOut); // pass carryIn by value
    sum[4] = psum; 
    psum = 0; // reset partial sum
    carryIn = carryOut;
    carryOut = 0; // reset carryOut

    // add fifth in number
    full_adder(b[3], a[3], carryIn, &psum, &carryOut); // pass carryIn by value
    sum[3] = psum; 
    psum = 0; // reset partial sum
    carryIn = carryOut;
    carryOut = 0; // reset carryOut

    // add sixth in number
    full_adder(b[2], a[2], carryIn, &psum, &carryOut); // pass carryIn by value
    sum[2] = psum; 
    psum = 0; // reset partial sum
    carryIn = carryOut;
    carryOut = 0; // reset carryOut

    // add seventh in number
    full_adder(b[1], a[1], carryIn, &psum, &carryOut); // pass carryIn by value
    sum[1] = psum; 
    psum = 0; // reset partial sum
    carryIn = carryOut;
    carryOut = 0; // reset carryOut

    // add eighth in number
    full_adder(b[0], a[0], carryIn, &psum, &carryOut); // pass carryIn by value
    sum[0] = psum; 
    carryIn = carryOut;

}

// creates array of bits from char number
// num: signed char num input
// return: array of bits 
int* getBits(char num) {
    int *toReturn = malloc(8 * sizeof(int)); // allocate memory for the array of 8 bits
    for (int j = 7; j >= 0; j--) { // for each bit in the integer...
        int bit = (num >> j) & 1; // shift the bits to the right by j, then compare the result to 1
        toReturn[7 - j] = bit; // store the bit in the correct position
        printf("%d", bit); // print the bit
    }
    printf("\n"); // print a newline

    return toReturn;
}



// creates decimal char from array of bits
// bits: 8-bit adder array
// return: char in decimal form
char getInt(int* bits){
    int toReturn = 0; // initialize toReturn to 0

    // check if the number is negative (if the most significant bit is 1)
    if (bits[0] == 1) {
        // if negative, convert to two's complement
        for (int i = 0; i < 8; i++) {
            bits[i] = !bits[i]; // invert bits
        }
        for (int i = 7; i >= 0; i--) {
            if (bits[i] == 0) {
                bits[i] = 1;
                break;
            } else {
                bits[i] = 0;
            }
        }
        // convert to decimal without inverting
        for (int i = 0; i < 8; i++){ 
            toReturn = toReturn << 1;
            toReturn |= bits[i];
        }
        toReturn = -toReturn; // Make the result negative
    } else {
        // convert to decimal as usual
        for (int i = 0; i < 8; i++){ 
            toReturn = toReturn << 1;
            toReturn |= bits[i];
        }
    }

   // printf("%d\n", toReturn); // print the result
    return toReturn; // return the result
}



        // main for testing functions
        int main(){

            //TESTING GATE FUNCTIONS:

            //NAND tests
            printf("NAND TESTS\n");
            printf("Test #1 returns: [%d], and should return [1]\n", nand(0, 0)); // should print 1
            printf("Test #2 returns: [%d], and should return [1]\n", nand(0, 1)); // should print 1
            printf("Test #3 returns: [%d], and should return [1]\n", nand(1, 0)); // should print 1
            printf("Test #4 returns: [%d], and should return [0]\n", nand(1, 1)); // should print 0
            printf("\n");

            //NOT tests
            printf("NOT TESTS\n");
            printf("Test #1 returns: [%d], and should return [1]\n", not(0)); // should print 1
            printf("Test #2 returns: [%d], and should return [0]\n", not(1)); // should print 0 
            printf("\n");

            //AND tests
            printf("AND TESTS\n");
            printf("Test #1 returns: [%d], and should return [0]\n", and(0, 0)); // should print 0
            printf("Test #2 returns: [%d], and should return [0]\n", and(0, 1)); // should print 0
            printf("Test #3 returns: [%d], and should return [0]\n", and(1, 0)); // should print 0
            printf("Test #4 returns: [%d], and should return [1]\n", and(1, 1)); // should print 1
            printf("\n");

            //OR tests
            printf("OR TESTS\n");
            printf("Test #1 returns: [%d], and should return [0]\n", or(0, 0)); // should print 0
            printf("Test #2 returns: [%d], and should return [1]\n", or(0, 1)); // should print 1
            printf("Test #3 returns: [%d], and should return [1]\n", or(1, 0)); // should print 1
            printf("Test #4 returns: [%d], and should return [1]\n", or(1, 1)); // should print 1
            printf("\n");

            //XOR tests
            printf("XOR TESTS\n");
            printf("Test #1 returns: [%d], and should return [0]\n", xor(0, 0)); // should print 0
            printf("Test #2 returns: [%d], and should return [1]\n", xor(0, 1)); // should print 1
            printf("Test #3 returns: [%d], and should return [1]\n", xor(1, 0)); // should print 1
            printf("Test #4 returns: [%d], and should return [0]\n", xor(1, 1)); // should print 0
            printf("\n");



            //TESTING ADDERS:

            //HALF-ADDER Tests
            printf("HALF-ADDER TESTS\n");


                // TEST #1
                // declare sum and carry variables
                int sum = 0;
                int carry = 0;
                half_adder(0, 0, &sum, &carry);
                printf("Test #1: sum[%d], carry[%d] and should return sum[0], carry[0]\n", sum, carry); // should print 0,0

                // TEST #2
                // reset sum and carry
                sum = 0;
                carry = 0;
                half_adder(0, 1, &sum, &carry);
                printf("Test #2: sum[%d], carry[%d] and should return sum[1], carry[0]\n", sum, carry); // should print 1,0

                // TEST #3
                // reset sum and carry
                sum = 0;
                carry = 0;
                half_adder(1, 0, &sum, &carry);
                printf("Test #3: sum[%d], carry[%d] and should return sum[1], carry[0]\n", sum, carry); // should print 1,0

                // TEST #4
                // reset sum and carry
                sum = 0;
                carry = 0;
                half_adder(1, 1, &sum, &carry);
                printf("Test #4: sum[%d], carry[%d] and should return sum[0], carry[1]\n", sum, carry); // should print 1,1
               
                printf("\n");

                //FULL-ADDER Tests
                printf("FULL-ADDER TESTS\n");

                // TEST #1
                // reset sum and carry variables
                sum = 0;
                carry = 0;
                full_adder(0, 0, 0, &sum, &carry);
                printf("Test #1: sum[%d], carry[%d] and should return sum[0], carry[0]\n", sum, carry); // should print 0,0

                // TEST #2
                // reset sum and carry variables
                sum = 0;
                carry = 0;
                full_adder(0, 0, 1, &sum, &carry);
                printf("Test #2: sum[%d], carry[%d] and should return sum[1], carry[0]\n", sum, carry); // should print 1,0

                // TEST #3
                // reset sum and carry variables
                sum = 0;
                carry = 0;
                full_adder(0, 1, 0, &sum, &carry);
                printf("Test #3: sum[%d], carry[%d] and should return sum[1], carry[0]\n", sum, carry); // should print 1,0

                // TEST #4
                // reset sum and carry variables
                sum = 0;
                carry = 0;
                full_adder(0, 1, 1, &sum, &carry);
                printf("Test #4: sum[%d], carry[%d] and should return sum[0], carry[1]\n", sum, carry); // should print 0,1

                // TEST #5
                // reset sum and carry variables
                sum = 0;
                carry = 0;
                full_adder(1, 0, 0, &sum, &carry);
                printf("Test #5: sum[%d], carry[%d] and should return sum[1], carry[0]\n", sum, carry); // should print 1,0

                // TEST #6
                // reset sum and carry variables
                sum = 0;
                carry = 0;
                full_adder(1, 0, 1, &sum, &carry);
                printf("Test #6: sum[%d], carry[%d] and should return sum[0], carry[1]\n", sum, carry); // should print 0,1

                // TEST #7
                // reset sum and carry variables
                sum = 0;
                carry = 0;
                full_adder(1, 1, 0, &sum, &carry);
                printf("Test #7: sum[%d], carry[%d] and should return sum[0], carry[1]\n", sum, carry); // should print 0,1

                // TEST #8
                // reset sum and carry variables
                sum = 0;
                carry = 0;
                full_adder(1, 1, 1, &sum, &carry);
                printf("Test #8: sum[%d], carry[%d] and should return sum[1], carry[1]\n", sum, carry); // should print 1,1

               
               
                printf("\n");

            //8-BIT ADDER TESTS
            printf("8-BIT ADDER TESTS\n");

                //INITIAL TEST
                printf("INITIAL TEST\n");

                int asum[] = {0, 0, 0, 0, 0, 0, 0, 0}; // initialize sum
                int a[] = {0, 0, 1, 0, 1, 1, 1, 0}; // test a 
                int b[] = {0, 0, 0, 1, 1, 1, 0, 1}; // test b

                printf("The Result: [");

                eight_bit_adder(a, b, asum); // run addition

                for (int i = 0; i < 7; i++){ // for each bit in sum...
                    printf("%d, ", asum[i]); // print 
                }
                
                printf("%d]\n", asum[7]); // print last bit

        printf("Expected: [0, 1, 0, 0, 1, 0, 1, 1]\n"); 
        printf("\n");
    
        // SIMPLE ADDITION TEST
        printf("SIMPLE ADDITION TESTS\n");
        
        char num1 = 120;
        char num2 = 5;
        
        int asum2[] = {0, 0, 0, 0, 0, 0, 0, 0}; // initialize sum
        int asum3[] = {0, 0, 0, 0, 0, 0, 0, 0}; // initialize sum
        int asum4[] = {0, 0, 0, 0, 0, 0, 0, 0}; // initialize sum



        printf("Test #1: 120 + 5\n");
        eight_bit_adder(getBits(num1), getBits(num2), asum2);
        printf("The Result: [");
        printf("%d", getInt(asum2)); // print result
        printf("]\n");
        printf("Expected: [125]\n");
        printf("\n");
  
        printf("Test #2 (OVERFLOW): 120 + 8\n");
        num2 = 8;
        eight_bit_adder(getBits(num1), getBits(num2), asum3);
        printf("The Result: [");
        printf("%d", getInt(asum3)); // print result
        printf("]\n");
        printf("Expected: [128]\n");
        printf("\n");


        // NEGATIVE ADDITION TESTS
        printf("NEGATIVE ADDITION TESTS\n");

        printf("Test #1: 120 + -5\n");
        num2 = -5;
        eight_bit_adder(getBits(num1), getBits(num2), asum4);
        printf("The Result: [");
        printf("%d", getInt(asum4)); // print result
        printf("]\n");
        printf("Expected: [115]\n");
        printf("\n");

        printf("Test #2(UNDERFLOW): -120 + -9\n");
        num1 = -120;
        num2 = -9;
        eight_bit_adder(getBits(num1), getBits(num2), asum4);
        printf("The Result: [");
        printf("%d", getInt(asum4)); // print result
        printf("]\n");
        printf("Expected: [-129]\n");
        printf("\n");

 
       
        // TEST HELPER METHODS  
        /*
        int test1[] =  {0, 1, 1, 1, 1, 1, 0, 1};
        int test2[] =  {1, 1, 1, 1, 1, 0, 1, 1};
        int test3[] =  {0, 0, 0, 0, 1, 0, 0, 0};


        getInt(test1); //125
        getInt(test2); //-5
        getInt(test3); //8
        */

        return 0;
    }
