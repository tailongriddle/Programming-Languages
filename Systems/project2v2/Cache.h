#ifndef CACHE_H
#define CACHE_H

#include "Memory.h"
#include "Sets.h"
#include "AddressDecoder.h"

class Cache {
private:
    Memory* pointer;
    int cacheSize;
    int blockSize; // size of blocks in bytes
    int blocksPerSet; // set associativity
    int numSets;
    Set** sets;
    AddressDecoder* decoder;

public:
    Cache(Memory* passPointer, int passCache, int passBlockSize, int passBlocks);
    ~Cache();
    unsigned char read(unsigned long address);
    void write(unsigned long address, unsigned char newValue);
    void display();
};

#endif // CACHE_H
