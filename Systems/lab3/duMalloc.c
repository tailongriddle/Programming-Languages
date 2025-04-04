#include <stdio.h>
#include <stdlib.h>
#include <stddef.h>

#include "duMalloc.h" //find it in the same folder

#define HEAP_SIZE 128*8

unsigned char heap[HEAP_SIZE]; // makes size of the heap 1024 bytes

typedef struct memoryBlockHeader{ // struct to represent the header of a memory block
    int size; // size of the reserved block
    struct memoryBlockHeader* next;// the next block in the integreated free list
} memoryBlockHeader; 

memoryBlockHeader* freeListHead; // second global variable to act as the head of the free list
// this is a pointer to the first free memory block header in the heap

// duInitMalloc
// initializing method
void duInitMalloc(){
     for (int i = 0; i < HEAP_SIZE; ++i) {
        heap[i] = 0; // initializes all memory in heap to 0
    } 
    memoryBlockHeader* currentBlock = (memoryBlockHeader*)heap; // cast the heap to a memory block header
    // -> is struct notation, can also use . but need to dereference because we are editing it
    currentBlock->size = HEAP_SIZE - sizeof(memoryBlockHeader); // set the size of the block to the size of the heap minus the size of the header
    currentBlock->next = NULL; // initialize next pointer to NULL
    freeListHead = currentBlock;  // set freeListHead to point to block header
}

// duMemoryDump
// method to print out the memory dump
void duMemoryDump(){
    printf("MEMORY DUMP\nFree List\n");
    memoryBlockHeader* currentBlock = freeListHead; // set currentBlock to the head of the free list
    while(currentBlock != NULL){ // while the current block is not null
        printf("Block at %p, size %d\n", currentBlock, currentBlock->size); // print out address and size
        currentBlock = currentBlock->next; // set currentBlock to next
    }
}
/*// duMalloc
// method to allocate space
void* duMalloc(int bytes){
    int blockSize;
    
    // round up the size to the nearest multiple of 8
    if ((bytes % 8) != 0){ // if not divisible by 8...
        blockSize = (bytes + 7) & ~7; // round up to next multiple of 8
    } else { // if divisible by 8...
        blockSize = bytes; // use the original size if already divisible by 8
    }

    memoryBlockHeader* currentBlock = freeListHead; // set currentBlock to the head of the free list
    memoryBlockHeader* previousBlock = NULL; // create previousBlock
    
    // find a free block that can accommodate the requested size
    while (currentBlock != NULL && currentBlock->size < blockSize + sizeof(memoryBlockHeader)){
        previousBlock = currentBlock; // set previous block to current
        currentBlock = currentBlock->next; // set currentBlock to next
    }

    // if no block can accommodate the request, return NULL
    if (currentBlock == NULL){
        return NULL;
    }

    // if the found block can be split into two
    if (currentBlock->size >= blockSize + sizeof(memoryBlockHeader) + 1) { // if the size of the block is greater than the size of the block plus the size of the header plus 1
        memoryBlockHeader* newBlock = (memoryBlockHeader*)((unsigned char*)currentBlock + sizeof(memoryBlockHeader) + blockSize); // create a new block
        newBlock->size = currentBlock->size - sizeof(memoryBlockHeader) - blockSize; // set the size of the new block to the size of the current block minus the size of the header and the size of the block
        newBlock->next = currentBlock->next; // set the next of the new block to the next of the current block

        if (previousBlock != NULL) { // if previousBlock is not null...
            previousBlock->next = newBlock; // set the next of previousBlock to newBlock
        } else { // if previousBlock is null...
            freeListHead = newBlock; // set freeListHead to newBlock
        }

        currentBlock->size = blockSize; // set the size of the current block to blockSize
    } else { // the block is a perfect fit... // could just add 8 to the size of the block 
        if (previousBlock != NULL) { // if previousBlock is not null...
            previousBlock->next = currentBlock->next; // set the next of previousBlock to the next of currentBlock
        } else { // if previousBlock is null...
            freeListHead = currentBlock->next; // set freeListHead to the next of currentBlock
        }
    }

    // return a pointer to the memory region after the header
    return (void*)((unsigned char*)currentBlock + sizeof(memoryBlockHeader));
}


*/
// duMalloc
// method to allocate space

void* duMalloc(int bytes){
    int blockSize;
    
    if ((bytes % 8) != 0){ // if not divisible by 8...
        blockSize = bytes + (8 - (bytes % 8)); // round up to next multiple of 8
        printf("Rounded up to %d\n", blockSize); // print out the rounded up number
    } else {
        blockSize = bytes; // use the original size if already divisible by 8
    }

    blockSize += sizeof(memoryBlockHeader); // calculate the size of the memory block

    memoryBlockHeader* currentBlock = freeListHead; // set currentBlock to the head of the free list
    memoryBlockHeader* previousBlock = NULL; // create previousBlock
    
    while (currentBlock != NULL && currentBlock->size < blockSize){
        previousBlock = currentBlock; // set previous block to current
        currentBlock = currentBlock->next; // set currentBlock to next
    }

    if (currentBlock == NULL){ // if at end of list...
        return NULL; // return null
    }
    

    memoryBlockHeader* usedBlock = currentBlock; // set usedBlock to currentBlock
    currentBlock = (memoryBlockHeader*)((unsigned char*)currentBlock + blockSize); // move currentBlock pointer by blockSize
   
    currentBlock->size = usedBlock->size - blockSize; // set the size of the next block to the remaining size - sizeof(memoryBlockHeader)
    currentBlock->next = usedBlock->next; // set the next pointer of the next block to the next pointer of the used block
    
    usedBlock->size = blockSize - sizeof(memoryBlockHeader);  // adjust size of usedBlock
    usedBlock->next = NULL; // initialize next pointer to NULL

    if (previousBlock == NULL) {
        freeListHead = currentBlock;
    } else {
        previousBlock->next = currentBlock;
    }
   
    return (void*)(usedBlock + 1); // return the usedBlock + 1 (the start of the block)
       
}  



// duFree
// method that frees memory
void duFree(void* ptr){
    memoryBlockHeader* blockHeader = (memoryBlockHeader*)((unsigned char*)ptr - sizeof(memoryBlockHeader)); // calculate the start of the block header
    
    // find the correct location to splice the block back into the freeList
    memoryBlockHeader* currentBlock = freeListHead; // set currentBlock to the head of the free list
    memoryBlockHeader* previousBlock = NULL; // set previousBlock to null
    
    while (currentBlock != NULL && currentBlock < blockHeader) { // while currentBlock is not null and currentBlock is less than blockHeader
        previousBlock = currentBlock; // set previousBlock to currentBlock
        currentBlock = currentBlock->next; // set currentBlock to next
    }
    
    // splice the block back into the freeList
    if (previousBlock == NULL) {
        // the block should be the new head of the freeList
     //   blockHeader->next = freeListHead; // set next of blockHeader to freeListHead
        freeListHead = blockHeader; // set freeListHead to blockHeader
    } else {
        // insert the block between previousBlock and currentBlock
        previousBlock->next = blockHeader; // set next of previousBlock to blockHeader
    }
    blockHeader->next = currentBlock; // set next of blockHeader to currentBlock

}



