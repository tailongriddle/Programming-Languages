// g++ heroMain.cc Superhero.cc -std=c++11 -o hero
// The c++11 is to switch to the 2011 defns so we can use "auto"

#include <iostream>
#include <vector>
#include <string>
#include <algorithm> // necessary for linux sorting
#include "Superhero.h"


int main() {

std::cout << "\n---- Make two new heros on the heap ----\n";
// Strings created on the heap
std::string* s1fn = new std::string("Johnny");
std::string* s1ln = new std::string("Storm");
std::string* s1hn = new std::string("HumanTorch");
Superhero* s1 = new Superhero(s1fn, s1ln, s1hn);
delete(s1fn);
delete(s1ln);
delete(s1hn);

// Strings created on the runtime stack
std::string s2fn = "Peter";
std::string s2ln = "Parker";
std::string s2hn = "Spiderman";
Superhero* s2 = new Superhero(&s2fn, &s2ln, &s2hn);
std::cout << *s1 << " is " << s1->getHeroName() << "\n"; // Johnny Storm
std::cout << *s2 << " is " << s2->getHeroName() << "\n"; // Peter Parker


std::cout << "\n---- Make a copy of s1 ----\n";
Superhero* s3 = new Superhero(*s1);
std::cout << *s1 << " is " << s1->getHeroName() << "\n"; // Johnny Storm
std::cout << *s2 << " is " << s2->getHeroName() << "\n"; // Peter Parker
std::cout << *s3 << " is " << s3->getHeroName() << "\n"; // Johnny Storm

std::cout << "\n---- Reassign s3 to s4 ----\n";
// Make strings on the runtime stack
std::string s3fn = "Susan";
std::string s3ln = "Storm";
std::string s3hn = "InvisibleWoman";
Superhero* s4 = new Superhero(&s3fn, &s3ln, &s3hn);
*s3 = *s4;
std::cout << *s1 << " is " << s1->getHeroName() << "\n"; // Johnny Storm
std::cout << *s2 << " is " << s2->getHeroName() << "\n"; // Peter Parker
std::cout << *s3 << " is " << s3->getHeroName() << "\n"; // Susan Storm
std::cout << *s4 << " is " << s4->getHeroName() << "\n"; // Susan Storm


std::cout << "\n---- Check for equality ----\n";
if (*s1 == *s3) {
    std::cout << "1 equal 3\n";
} else {
    std::cout << "1 NOT equal 3\n"; // NOT equal
}
// Strings created on the heap
std::string* s5fn = new std::string("Peter");
std::string* s5ln = new std::string("Parker");
std::string* s5hn = new std::string("Spiderman");
Superhero* s5 = new Superhero(s5fn, s5ln, s5hn);
delete s5fn;
delete s5ln;
delete s5hn;
if (*s2 == *s5) {
    std::cout << "2 equal 5\n"; // equal
} else {
    std::cout << "2 NOT equal 5\n";
}

std::cout << "\n---- Make a list of Superheros ----\n";

// Make strings on the runtime stack
std::string s6fn = "Tony";
std::string s6ln = "Stark";
std::string s6hn = "Ironman";
Superhero* s6 = new Superhero(&s6fn, &s6ln, &s6hn);
std::vector<Superhero> theSuperheros;
theSuperheros.push_back(*s1); // Johnny Storm
theSuperheros.push_back(*s2); // Peter Parker
theSuperheros.push_back(*s3); // Susan Storm
theSuperheros.push_back(*s4); // Susan Storm
theSuperheros.push_back(*s5); // Peter Parker
theSuperheros.push_back(*s6); // Tony Stark

// Normal for loop example
for (int i=0; i<theSuperheros.size(); i++) {
    std::cout << theSuperheros[i] << " at address " << &(theSuperheros[i]) << "\n";
}

// Soring example
std::cout << "\n---- Sort the list of Superheros ----\n";
std::sort(theSuperheros.begin(), theSuperheros.end());

// Peter Parker
// Peter Parker
// Tony Stark
// Johnny Storm
// Susan Storm
// Susan Storm

// Iterators rather than for loop example
for (auto i=theSuperheros.begin(); i!=theSuperheros.end(); i++) {
    std::cout << *i << "\n";
}


std::cout << "\n---- Deleting the Superheros ----\n";
delete(s1);
delete(s2);
delete(s3);
delete(s4);
delete(s5);
delete(s6);
}