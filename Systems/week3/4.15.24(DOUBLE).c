//preprocessor step, happens FIRST, finds C file on device and pastes text here
#include <stdio.h> 
#include "4.15.24(DOUBLE).h" //find it in the same folder


// doubles a number and returns it
// if you remove this but keep the prototype, you get a 'linking error'
int doubleIt(int x){
    return 2*x; // return two times the parameter x
} 
