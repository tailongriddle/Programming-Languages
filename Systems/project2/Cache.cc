#include "Cache.h"
#include "Memory.h"
#include "Set.h"
#include "AddressDecoder.h"


Memory pointer;
int cacheSize;
int blockSize; // size of blocks in bytes
int blocksPerSet; // set associativity
int numSets;
Set* sets;
AddressDecoder decoder;

Cache::Cache(Memory passPointer, int passCache, int passBlockSize, int passBlocks){
    pointer = passPointer;
    cacheSize = passCache;
	blockSize = passBlockSize;
	blocksPerSet = passBlocks;

	numSets = cacheSize/ blockSize * blocksPerSet;
	sets = new Set*[numSets]; //allocate array of Set pointers
	decoder = AddressDecoder(numSets, blockSize);

    for (int i = 0; i < numSets; i++){
        sets[i] = Set(blockSize, blocksPerSet, pointer, decoder);	// Allocate each Set
	}

};

unsigned char Cache::Read (unsigned long address){
    int setIndex = decoder.getSetIndex(address); // goes in set 
    int blockOffset = decoder.getBlockOffset(address); // goes in set
    unsigned char tag = decoder.getTag(address); // goes in set
	return sets[setIndex].Read(address);
} 
    
void Cache::Write (unsigned long address, unsigned char newValue){
    int setIndex = decoder.getSetIndex(address); // goes in set 
    int blockOffset = decoder.getBlockOffset(address); // goes in set
    unsigned char tag = decoder.getTag(address); // goes in set
    return sets[setIndex].Write(address, newValue); 
} 

void Cache::Display (){
	for (int i = 0; i <numSets; i++){
		sets[i].Display();
}

} 



