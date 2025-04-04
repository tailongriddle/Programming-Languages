#ifndef ADDRESS_DECODER_H
#define ADDRESS_DECODER_H

#include <cmath>

class AddressDecoder {
private:
    int setIndexBits;
    int blockOffsetBits;

public:
    AddressDecoder(int numSets, int blockSize);
    int getSetIndex(unsigned long address);
    int getBlockOffset(unsigned long address);
    int getTag(unsigned long address);
};

#endif // ADDRESS_DECODER_H
