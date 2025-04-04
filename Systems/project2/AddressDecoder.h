class AddressDecoder{
	int tag;
    int setIndex;
    int blockOffset;
public:
	AddressDecoder(int numSets, int blockSize);
    int getSetIndex(unsigned long address);
  	int getBlockOffset(unsigned long address);
    unsigned char getTag(unsigned long address);
};
