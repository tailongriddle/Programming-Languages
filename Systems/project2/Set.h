#ifndef SET_H
#define SET_H

class Set{

public:
    Set(int numBlocks, int blockSize, Memory pointer, AddressDecoder decoder);
	unsigned char Set::Read (unsigned long address);
	void Set::Write (unsigned long address, unsigned char newValue);
	void Set::Display();
};
#endif