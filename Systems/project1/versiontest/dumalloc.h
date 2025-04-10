#ifndef DUMALLOC_H
#define DUMALLOC_H
#define HEAP_SIZE (128 * 8) 
#define FIRST_FIT 0
#define BEST_FIT 1

typedef struct memoryBlockHeader {
     int free; // 0 - used, 1 = free
     int size; // size of the reserved block
     struct memoryBlockHeader* next;  // the next block in the integrated free list
} memoryBlockHeader;

// The interface for DU malloc and free
void duInitMalloc(int strategy);
void* duMalloc(int size);
void duFree(void* ptr);

void duMemoryDump();

#endif