#include <iostream>
#include "Rational.h"

/*
void foo(Rational* r){
    r->display(); //dereference with r-> 
}*/

void foo(Rational& r){ //pass by refernce (vs value)
    r.display(); 
}

int main(){
    int x = 5;
    int y = 8;

    //cout is a stream object that is used to output strings or data to the console
    //reach into the standard package and pull out the cout object (std::cout)
    std::cout << "Hello World\n"; // print to the console   
    std::cout << "value of x is " << x << " and y is " << y << "\n";

    Rational* r1 = new Rational(5,2); // "new" creates memory on the heap
    //Rational* clarifies that r1 is a pointer  
    Rational r2(9,4); //creates the rational on the runtime stack, which you cannot do in Java 
    foo(r2); // taking a Rational, not a Rational pointer
    //foo(*r1); // taking a Rational pointer

    Rational r3(1,2);
    Rational* r5 = r2.mult(r3);
    Rational* r4 = new Rational(r2);


    r1->display(); //same as (*r1).display();
    r2.display(); // is already on the stack so you don't need a pointer

}