#include <stdio.h>
#include "AddressDecoder.h"

AddressDecoder::AddressDecoder(int numSets, int blockSize) {
    setIndexBits = std::log2(numSets);
    blockOffsetBits = std::log2(blockSize);
    
}

int AddressDecoder::getSetIndex(unsigned long address) {
    printf("Set Index Bits: %d\n", setIndexBits);
    return (address >> blockOffsetBits) & ((1 << setIndexBits) - 1);
}

int AddressDecoder::getBlockOffset(unsigned long address) {
    printf("Block Offset Bits: %d\n", blockOffsetBits);
    return address & ((1 << blockOffsetBits) - 1);
}

int AddressDecoder::getTag(unsigned long address) {
    printf("Tag: %lu\n", address >> (setIndexBits + blockOffsetBits));
    return address >> (setIndexBits + blockOffsetBits);
}


