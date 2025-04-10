#include "Rational.h"


Rational::Rational(){ // how to relate the three constructor methods to the signatures in the header
    num = 1;
    dem = 1;
}

Rational::Rational(int n){
    num = n;
    dem = 1;
    
}

Rational::Rational(int num, int d){
    this->num = num; // "this->" dereferences the pointer like in Java
    dem = d;
}

//destructor
Rational::~Rational(){
    
}

//copy constructor
Rational::Rational(const Rational& r){ 
    num = r.num;
    dem = r.dem;

}

Rational* Rational::mult(const Rational& r) const{
    Rational* nr = new Rational();

    nr.num = num * r.num;
    nr.dem = dem * r.dem;

    return nr;
}

void Rational::display() const{
    std::cout << this->num << "/" << this->dem << "\n";
}