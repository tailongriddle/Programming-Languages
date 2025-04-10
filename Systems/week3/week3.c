
//preprocessor step, happens FIRST, finds C file on device and pastes text here
#include <stdio.h> 
#include "double.h" //find it in the same folder


// function prototype / signature
// this goes right at the top (C reads top to bottom)
// REMOVE FROM THIS FILE: int doubleIt(int x); 

// main method 
// incremental compilation
int main(){

    int x2 = doubleIt(5);
    printf("%d\n", x2); // print statement
    return 0; // return 0

}

// NOTES:
//target: depends_on 
    //rules

//gcc week3.c -MM
//use -MM to tell you rules and dependencies


// end of file

