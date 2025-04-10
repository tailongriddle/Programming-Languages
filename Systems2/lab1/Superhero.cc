#include "Superhero.h"
#include <string>

/**
 * Constructor
 * 
 * Creates a new Superhero with the passed in strings
 * 
*/
Superhero::Superhero(std::string* fName, std::string* lName, std::string* hName){ // how to relate the three constructor methods to the signatures in the header
    firstName = new std::string(*fName);
    lastName = new std::string(*lName);
    heroName = new std::string(*hName);
}



/**
 * Copy Constructor
 * 
 * Copies the strings from the passed in Superhero
 * 
*/
Superhero::Superhero(const Superhero& s){ 
    firstName = new std::string (*s.firstName);
    lastName = new std::string (*s.lastName);
    heroName = new std::string (*s.heroName);
}

/**
 * Deconstructor
 * 
 * Deletes the pointers to the strings
 * 
*/
Superhero::~Superhero(){
    delete firstName;
    delete lastName;
    delete heroName;
}

/**
 * Assignment Operator
 * 
 * 
 * Assigns the strings from the passed in Superhero
*/
Superhero& Superhero::operator=(const Superhero& s){
 if (this != &s) { // check for self-assignment
        delete firstName;
        delete lastName;
        delete heroName;

        firstName = new std::string(*s.firstName);
        lastName = new std::string(*s.lastName);
        heroName = new std::string(*s.heroName);
    }
    return *this;
}

/**
 * Comparison Operator
 * 
 * 
*/
bool Superhero::operator==(const Superhero& s) const {
    return ((*firstName == *s.firstName) && (*lastName == *s.lastName));

}

/**
 * Less than Operator
 * 
 * 
*/
bool Superhero::operator<(const Superhero& s) const {
    if (*lastName != *s.lastName) {
        return *lastName < *s.lastName;
    }
    return *firstName < *s.firstName;
}

std::ostream& operator<<(std::ostream& os, const Superhero& s) {
    os << *s.firstName << " " << *s.lastName;
    return os;
}

/**
 * Get Hero Name
 * 
 * Returns the hero name
 * 
*/
std::string Superhero::getHeroName(){
     if (heroName) {
        return *heroName;
    } else {
        std::cerr << "heroName is null!" << std::endl;
        return "";
    }
}