#ifndef CACHE_H
#define CACHE_H

class Cache{
    Memory pointer;
    int cacheSize;
    int byteSize;
    int blocksPerSet; // set associativity
    int numSets;
    Set* sets;
    AddressDecoder decoder;
public:
    Cache(Memory passPointer, int passCache, int passBlockSize, int passBlocks);
	unsigned char Cache::Read (unsigned long address);
	void Cache::Write (unsigned long address, unsigned char newValue);
	void Cache::Display();
};
#endif