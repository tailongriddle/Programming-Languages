#ifndef SET_H
#define SET_H

#include "Block.h"
#include "Memory.h"
#include "AddressDecoder.h"
#include "PerformanceCounter.h"

class Set {
private:
    int numBlocks;
    int blockSize;
    Block** blocks;
    Memory* memory;
    AddressDecoder* decoder;
    PerformanceCounter* counter;

public:
    Set(int numBlocks, int blockSize, Memory* memory, AddressDecoder* decoder, PerformanceCounter* counter);
    ~Set();
    int getLRU(unsigned char tag, int blockOffset, Memory* memory, unsigned long address);
    unsigned char read(unsigned char tag, int blockOffset, Memory* memory, unsigned long address);
    void write(unsigned char tag, int blockOffset, unsigned char value, Memory* memory);
    void display();
};

#endif // SET_H
