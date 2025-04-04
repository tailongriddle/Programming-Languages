#ifndef BLOCK_H
#define BLOCK_H

#include "Memory.h"
#include <chrono>

class Block {
private:
    int blockSize;
    Memory* memory;
    unsigned char* data;
    unsigned char tag;
    bool valid;
    bool dirty;
    long lastAccessTime;

    std::chrono::high_resolution_clock m_clock;

public:
    Block(int blockSize, Memory* memory);
    ~Block();
    unsigned char read(int offset);
    void write(int offset, unsigned char value);
    void loadFromMemory(Memory* memory, unsigned char tag, int address);
    void saveToMemory(Memory* memory, int address);
    void display();
    unsigned char getTag();
    bool isValid();
    bool isDirty();
    void updateTimestamp();
};

#endif // BLOCK_H
