#include <stdio.h>
#include "Memory.h"

int memSize;
unsigned char* bytePointer;

Memory::Memory(int size){
    memSize = size;
    bytePointer = new unsigned char[size]; 

    for (int i = 0; i < size; i++){
	    bytePointer[i] = i%255; // this will initialize the memory to some pattern
    }


};

unsigned char Memory::getByte(unsigned long address){

    if (address < memSize) {
        return bytePointer[address]; // this will return a byte from the specified memory address}
    } else {
        printf("Out of Bounds\n");
        return 0;
    }

}

void Memory::setByte(unsigned long address, unsigned char toSet){
    if (address < memSize){
        bytePointer[address] = toSet;
    } 
    else {
    printf("Out of Bounds\n");
    }
}

int Memory::getMemSize(){
    return memSize;
}

void Memory::display(){

    for (int i = 0; i < memSize; i++){
        printf("%02x ", bytePointer[i]);
        if (i % 16 == 15){
            printf("\n");
        }
    }
}


int main(){
    Memory* m = new Memory(32);

    m->display(); // this will print out the memory contents
    printf("%d\n", m->getMemSize());
    printf("%c\n", m->getByte(1));
    m->setByte(1, 2);
    printf("%c\n", m->getByte(1));
    m->display();
    printf("%d\n", m->getMemSize());

    return 0;
}


    