#ifndef MEMORY_H
#define MEMORY_H


class Memory{
   int memSize;
   unsigned char* bytePointer;
public:
   Memory(int size);
   unsigned char getByte(unsigned long address);
   void setByte(unsigned long address, unsigned char toSet);
   int getMemSize();
   void display();
};


int main();


#endif

