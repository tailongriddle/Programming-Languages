#ifndef RATIONAL_H
#define RATIONAL_H
#include <iostream>


// defines the rational class + methods it can do 
class Rational {
    private:
        int num;
        int dem;

    public:
        Rational(); // add three constructors (different types)
        Rational(int n);
        Rational(int n, int d);
        ~Rational();
      
        Rational(const Rational& r);
        
        Rational* mult(const Rational& r) const;
        void display() const;

};

#endif