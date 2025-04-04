#ifndef SUPERHERO_H
#define SUPERHERO_H
#include <iostream>


// defines the rational class + methods it can do 
class Superhero {
    private:
         std::string* firstName;
         std::string* lastName;
         std::string* heroName;
     
    public:
        Superhero(std::string* fName, std::string* lName, std::string* hName);
        Superhero(const Superhero& s);
        
        ~Superhero(); // deleter

        Superhero& operator=(const Superhero& s); // assignment operator
        bool operator==(const Superhero& s)const; // comparison operator
        bool operator<(const Superhero& other) const; // less than operator
        friend std::ostream& operator<<(std::ostream& os, const Superhero&); // output operator

        std::string getHeroName(); // get hero name operator

        

};
    
#endif