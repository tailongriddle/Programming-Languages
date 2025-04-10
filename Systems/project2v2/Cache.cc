#include "Cache.h"
#include <iostream>


Cache::Cache(Memory* passPointer, int passCache, int passBlockSize, int passBlocks)
   {
    pointer = passPointer;
    cacheSize = passCache; // size of cache in bytes
    blockSize = passBlockSize; // size of blocks in bytes
    blocksPerSet = passBlocks; // set associativity

    numSets = cacheSize / (blockSize * blocksPerSet);
    sets = new Set*[numSets]; // Allocate array of Set pointers
    //printf("Number of sets: %d\n", numSets);
    for (int i = 0; i < numSets; i++) {
        //printf("Block size: %d\n", blockSize);
        //printf("Blocks per set: %d\n", blocksPerSet);
        sets[i] = new Set(blocksPerSet, blockSize, pointer, decoder); // Allocate each Set
    }
    decoder = new AddressDecoder(numSets, blockSize);
}

Cache::~Cache() {
    for (int i = 0; i < numSets; i++) {
        delete sets[i];// Delete each Set object
    }
    delete[] sets;// Delete the array of Set pointers
    delete decoder;// Delete the AddressDecoder object
}

// Read the value from the cache
unsigned char Cache::read(unsigned long address) {
    int setIndex = decoder->getSetIndex(address);
    int blockOffset = decoder->getBlockOffset(address);
    unsigned char tag = decoder->getTag(address);
    return sets[setIndex]->read(tag, blockOffset, pointer); // Read the value from the Set
}

void Cache::write(unsigned long address, unsigned char newValue) {
    int setIndex = decoder->getSetIndex(address);
    int blockOffset = decoder->getBlockOffset(address);
    unsigned char tag = decoder->getTag(address);
    sets[setIndex]->write(tag, blockOffset, newValue, pointer);
}

void Cache::display() {
    printf("CACHE:\n");
    for (int i = 0; i < numSets; i++) {
        printf("Set %d\n", i);
        sets[i]->display();
    }
}
