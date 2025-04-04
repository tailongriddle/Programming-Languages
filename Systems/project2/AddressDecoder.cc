#include "AddressDecoder.h"
#include "Cache.h"
#include <math.h>

int tag;
int setIndexBits;
int blockOffsetBits;

AddressDecoder::AddressDecoder(int numSets, int blockSize) {

	setIndexBits = log2(numSets);
    blockOffsetBits = log2(blockSize);
    tag = 32 - setIndexBits - blockOffsetBits; // can we assume the address or do we need to pass it in somewhow, and if so, from where?
}

int AddressDecoder::getSetIndex (unsigned long address) {
	     return (address >> blockOffsetBits) & ((1 << setIndexBits) - 1);
}

int AddressDecoder::getBlockOffset(unsigned long address) {

	return address & ((1 << blockOffsetBits) - 1);
}

unsigned char AddressDecoder::getTag(unsigned long address) {
	       return address >> (setIndexBits + blockOffsetBits);
}

