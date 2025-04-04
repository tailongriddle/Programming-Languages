
#ifndef DUMALLOC_H
#define DUMALLOC_H
#define HEAP_SIZE (128 * 8) 
#define FIRST_FIT 0
#define BEST_FIT 1 
#define Managed(p) (*p)
#define Managed_t(t) t*


typedef struct memoryBlockHeader {
     int free; // 0 - used, 1 = free
     int size; // size of the reserved block
     int managedIndex; // the unchanging index in the managed array
     int survivalAmt; // the number of times the block has moved between young heaps
     struct memoryBlockHeader* next;  // the next block in the integrated free list
} memoryBlockHeader;

// The interface for DU malloc and free
void duInitMalloc(int strategy);
void* duMalloc(int size);
void duFree(void* ptr);
void duMemoryDump();
//Version2 
void duManagedInitMalloc(int searchType);
void** duManagedMalloc(int size);
void duManagedFree(void** mptr);

void minorCollection();
void majorCollection();


#endif