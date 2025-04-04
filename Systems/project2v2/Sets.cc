#include "Sets.h"
#include "Block.h"
#include <iostream>


Set::Set(int numBlocks, int blockSize, Memory* memory, AddressDecoder* decoder)
    : numBlocks(numBlocks), blockSize(blockSize), memory(memory), decoder(decoder){
    blocks = new Block*[numBlocks];
    for (int i = 0; i < numBlocks; ++i) {
        //printf("Block size: %d\n", blockSize);
        blocks[i] = new Block(blockSize, memory);
    }
}

Set::~Set() {
    for (int i = 0; i < numBlocks; ++i) {
        delete blocks[i]; 
    }
    delete[] blocks;
}

// Read the value from the cache
unsigned char Set::read(unsigned char tag, int blockOffset, Memory* memory) {
    for (int i = 0; i < numBlocks; ++i) {
        if (blocks[i]->getTag() == tag && blocks[i]->isValid()) {
            return blocks[i]->read(blockOffset);
        }
    }
    // If miss, load from memory and return the value
    blocks[0]->loadFromMemory(memory, tag, blockOffset);
    return blocks[0]->read(blockOffset);
}

// Write the value to the cache
void Set::write(unsigned char tag, int blockOffset, unsigned char value, Memory* memory) {
    for (int i = 0; i < numBlocks; ++i) {
        if (blocks[i]->getTag() == tag && blocks[i]->isValid()) {
            blocks[i]->write(blockOffset, value);
            return;
        }
    }
    // If miss, load from memory and write the value
    blocks[0]->loadFromMemory(memory, tag, blockOffset);
    blocks[0]->write(blockOffset, value);
}

void Set::display() {
    printf("Blocks:\n");
    for (int i = 0; i < numBlocks; ++i) {
        printf("%d:\n", i);
        blocks[i]->display();
    }
}
