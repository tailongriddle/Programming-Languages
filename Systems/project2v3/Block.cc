#include "Block.h"
#include <iostream>

Block::Block(int blockSize, Memory* memory) : blockSize(blockSize), memory(memory), tag(0), valid(false), dirty(false){
    data = new unsigned char[blockSize];
    lastAccessTime = 0;
}

Block::~Block() {
    delete[] data;
}

unsigned char Block::read(int offset) {
    updateTimestamp();
    return data[offset];
}

void Block::write(int offset, unsigned char value) {
    data[offset] = value;
    dirty = true;
    updateTimestamp();
}

void Block::loadFromMemory(Memory* memory, unsigned char newTag, unsigned long address) {
    tag = newTag;
    valid = true;
    dirty = false; 
    address &= (~(unsigned long)0<<2);
    for (int i = 0; i < blockSize; ++i) {
        data[i] = memory->getByte(address + i);
    }
    updateTimestamp();
}

void Block::saveToMemory(Memory* memory, int address) {
    if (dirty) {
        for (int i = 0; i < blockSize; ++i) {
            memory->setByte(address + i, data[i]);
        }
    }
    dirty = false;
}

//prints hex values with two digits of the block
void Block::display() {
    std::cout << "valid: " << valid << "    tag: " << (int)tag << "    dirty: " << dirty << "    timestamp: " << lastAccessTime << std::endl;
    for (int i = 0; i < blockSize; ++i) {
        printf("%02x ", data[i]);
    }
    std::cout << std::endl;
}

unsigned char Block::getTag() {
    return tag;
}

bool Block::isValid() {
    return valid;
}

bool Block::isDirty() {
    return dirty;
}

void Block::updateTimestamp() {
    lastAccessTime = std::chrono::duration_cast<std::chrono::nanoseconds>(m_clock.now().time_since_epoch()).count();
}

long Block::getTimestamp(){
    return lastAccessTime;
}
