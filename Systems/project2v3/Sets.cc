#include "Sets.h"
#include "Block.h"
#include "PerformanceCounter.h"
#include <iostream>
#include <limits.h> // For UINT_MAX

Set::Set(int numBlocks, int blockSize, Memory* memory, AddressDecoder* decoder, PerformanceCounter* counter)
    : numBlocks(numBlocks), blockSize(blockSize), memory(memory), decoder(decoder), counter(counter) {

    blocks = new Block*[numBlocks];
    for (int i = 0; i < numBlocks; ++i) {
        blocks[i] = new Block(blockSize, memory);
    }
}

Set::~Set() {
    for (int i = 0; i < numBlocks; ++i) {
        delete blocks[i];
    }
    delete[] blocks;
}

int Set::getLRU(unsigned char tag, int blockOffset, Memory* memory, unsigned long address) {
    int lru = 0;
    unsigned int minTimestamp = UINT_MAX;
    for (int i = 0; i < numBlocks; ++i) {
        if (blocks[i]->getTimestamp() < minTimestamp) {
            minTimestamp = blocks[i]->getTimestamp();
            lru = i;
        }
    }

    if (blocks[lru]->isDirty()) {
        blocks[lru]->saveToMemory(memory, address);
        counter->incrementWrites(); // Increment writebacks
    }

    blocks[lru]->loadFromMemory(memory, tag, address);
    blocks[lru]->updateTimestamp();
    return lru;
}

unsigned char Set::read(unsigned char tag, int blockOffset, Memory* memory, unsigned long address) {
    for (int i = 0; i < numBlocks; ++i) {
        if (blocks[i]->getTag() == tag && blocks[i]->isValid()) {
            counter->incrementHits(); // increment hits
            printf("Hits: %d\n", counter->getHits());
            blocks[i]->updateTimestamp(); // update timestamp when accessed
            return blocks[i]->read(blockOffset);
        }
    }
    // if miss, load from memory + return value
    counter->incrementMisses(); // increment misses
    printf("Misses: %d\n", counter->getMisses());
    int lruIndex = getLRU(tag, blockOffset, memory, address);
    return blocks[lruIndex]->read(blockOffset);
}

void Set::write(unsigned char tag, int blockOffset, unsigned char value, Memory* memory) {
    for (int i = 0; i < numBlocks; ++i) {
        if (blocks[i]->getTag() == tag && blocks[i]->isValid()) {
            blocks[i]->write(blockOffset, value);
            counter->incrementHits(); // increment hits
            printf("Hits: %d\n", counter->getHits());
            blocks[i]->updateTimestamp(); // update timestamp when accessed
            return;
        }
    }
    // if miss, load from memory + write value
    counter->incrementMisses(); // increment misses
    printf("Misses: %d\n", counter->getMisses());
    int lruIndex = getLRU(tag, blockOffset, memory, blockOffset);
    blocks[lruIndex]->write(blockOffset, value);
}

void Set::display() {
    printf("Blocks:\n");
    for (int i = 0; i < numBlocks; ++i) {
        printf("%d:\n", i);
        blocks[i]->display();
    }
   // counter->display();
}