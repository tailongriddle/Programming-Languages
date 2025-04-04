#include <stdio.h>
#include <stdlib.h>
#include <stddef.h>
#include <string.h>

#define HEAP_SIZE 1024
#define FIRST_FIT 0
#define BEST_FIT 1

unsigned char heap[HEAP_SIZE];

typedef struct memoryBlockHeader {
    int status; // 1 = used, 0 = free
    int size; // size of the reserved block
    int managedIndex; // the unchangable index of the managed array
    struct memoryBlockHeader* next; 
} memoryBlockHeader;

memoryBlockHeader* freeListHead;
int fit;
void* managedList[HEAP_SIZE / 8];
int managedListSize = 0;

void duManagedInitMalloc(int searchType);
void** duManagedMalloc(int size);
void duManagedFree(void** mptr);
void duInitMalloc();
void* duMalloc(int size);
void duFree(void* ptr);
void duMemoryDump();
void duMemoryBlockPrint();
void duFreeListPrint();



// client managed memory 

// calls original duInitMalloc, initializes slots of the managed list, and initial size
void duManagedInitMalloc(int searchType){
    duInitMalloc(searchType); // call original duInitMalloc
    for (int i = 0; i < HEAP_SIZE / 8; i++){ // for each slot in the managed list...
        managedList[i] = 0; // set the slot to 0
    }
    managedListSize = 0; // set managedListSize to 0

}

// calls original duMalloc (to create the correct size memory on the heap)
// add an entry into the managed list for this heap block
// set the managed index in the heap block itself
// return the pointer to the managed list slot
void** duManagedMalloc(int size){
    duMalloc(size); 
    managedList[managedListSize] = (void*)(freeListHead + 1); // set the managed list slot to the block
    freeListHead->managedIndex = managedListSize; // set the managed index in the block
    managedListSize++; // increment managedListSize
    return &managedList[freeListHead->managedIndex]; // return the address of the slot in the managed list}
}
// calls original duFree function to remove used block from the heap
// null out the address at the slot in the managed list being freed
void duManagedFree(void** mptr){
    duFree(mptr); // call original duFree
    managedList[freeListHead->managedIndex] = 0; // set the slot in the managed list to 0

}

void duManagedListPrint(){
    printf("ManagedList\n");
    for (int i = 0; i < HEAP_SIZE / 8; i++){ // for each slot in the managed list...
        printf("ManagedList[%d]: %p\n", i, managedList[i]); // print out the slot and the address
    }


}


// initializing method
void duInitMalloc(int givenFit){

    fit = givenFit; // set fit to the given fit
    for (int i = 0; i < HEAP_SIZE; i++) {
        heap[i] = 0; // initializes all memory in heap to 0
    } 

    memoryBlockHeader* currentBlock = (memoryBlockHeader*)heap; // cast the heap to a memory block header
    currentBlock->size = HEAP_SIZE - sizeof(memoryBlockHeader); // set the size of the block to the size of the heap minus the size of the header
    currentBlock->next = NULL; // initialize next pointer to NULL
    currentBlock->status = 0; // initialize 'used' to free
    freeListHead = currentBlock;  // set freeListHead to point to block header
}

// print memory block (addresses and graphical string)
// runs through memory directly (not the free list)
void duMemoryBlockPrint(){
    char upperLetters[] = {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '\0'};
    char lowerLetters[] = {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', '\0'};
    char toAdd[50000] = "";
    char toPrint[50000] = "";

    printf("Memory Block\n");
    memoryBlockHeader* currentBlock = (memoryBlockHeader*)heap; // set currentBlock to the head of the heap
    while(currentBlock != NULL){ // while the current block is not null
        if (currentBlock->status == 1){
            printf("Used block at %p, size %d\n", currentBlock, currentBlock->size); // print out address and size
            for (int i = 0; i < (currentBlock->size+16) / 8; i++){
                toAdd[i] = upperLetters[0]; // set the character to the corresponding letter
            }
            
            // remove used letter and move all other letters up
            for (int i = 0; i < 25; i++){
                upperLetters[i] = upperLetters[i+1];
            }
            strcat(toPrint, toAdd); // add the string to the print string
            memset(toAdd, 0, sizeof(toAdd)); // reset toAdd variable
        } else if(currentBlock->status == 0){
            printf("Free block at %p, size %d\n", currentBlock, currentBlock->size); // print out address and size
            for (int i = 0; i < (currentBlock->size+16)/8; i++){
                toAdd[i] = lowerLetters[0]; // set the character to the corresponding letter
            }
            // remove used letter and move all other letters up
            for (int i = 0; i < 25; i++){
                lowerLetters[i] = lowerLetters[i+1];
            }
            strcat(toPrint, toAdd); // add the string to the print string
            memset(toAdd, 0, sizeof(toAdd)); // reset toAdd variable
        }
        currentBlock = currentBlock->next; // set currentBlock to next
    }

    printf("%s\n", toPrint); // print out the string

    
}

// print free list
void duFreeListPrint(){
    printf("Free List\n");
    memoryBlockHeader* currentBlock = freeListHead; // set currentBlock to the head of the free list
    while(currentBlock != NULL){ // while the current block is not null
        printf("Block at %p, size %d\n", currentBlock, currentBlock->size); // print out address and size
        currentBlock = currentBlock->next; // set currentBlock to next
    }
}

// method to print out the memory dump
void duMemoryDump(){
    printf("MEMORY DUMP\n");
    duMemoryBlockPrint();
    duFreeListPrint();
    duManagedListPrint();

}

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
    memoryBlockHeader* bestBlock = currentBlock; // create bestBlock
    
    if (fit == FIRST_FIT){ // if first fit...
        while (currentBlock != NULL && currentBlock->size < blockSize){
            previousBlock = currentBlock; // set previous block to current
            currentBlock = currentBlock->next; // set currentBlock to next
            bestBlock = currentBlock; // set usedBlock to currentBlock
        }
    } else if (fit == BEST_FIT){ // if best fit...
        int bestFit = HEAP_SIZE; // set bestFit to the size of the heap
        bestBlock = currentBlock; // set usedBlock to currentBlock
        while (currentBlock->next != NULL){
            printf("currentBlock size: %d\n", currentBlock->size); // print out the size of the current block
            if (currentBlock->size >= blockSize && (currentBlock->size - blockSize) <= bestFit){
                bestFit = (currentBlock->size - blockSize); // set bestFit to the size of the current block
                previousBlock = currentBlock; // set previous block to current
                bestBlock = currentBlock; // set usedBlock to currentBlock
            }
            currentBlock = currentBlock->next; // set currentBlock to next
        }

    }

    printf("Current block size: %d\n", currentBlock->size); // print out the size of the current block
  
    memoryBlockHeader* usedBlock = bestBlock; // set usedBlock to currentBlock
    currentBlock = (memoryBlockHeader*)((unsigned char*)currentBlock + blockSize); // move currentBlock pointer by blockSize
   
    currentBlock->size = usedBlock->size - blockSize; // set the size of the next block to the remaining size - sizeof(memoryBlockHeader)
    currentBlock->next = usedBlock->next; // set the next pointer of the next block to the next pointer of the used block
    currentBlock->status = 0; // set 'status' to 'free'

    usedBlock->size = blockSize - sizeof(memoryBlockHeader);  // adjust size of usedBlock
    usedBlock->next = currentBlock; // set the next pointer of the used block to the current block
    usedBlock->status = 1; // set 'status' to 'used'

    if (previousBlock == NULL) {
        freeListHead = currentBlock;
    } else {
        previousBlock->next = currentBlock;
    }
    return (void*)(usedBlock + 1); // return the usedBlock + 1 (the start of the block)
       
}  

// method that frees memory
void duFree(void* ptr){
    memoryBlockHeader* currentBlock = (memoryBlockHeader*)((unsigned char*)ptr - sizeof(memoryBlockHeader)); // set currentBlock to the block header
    currentBlock->status = 0; // set 'status' to 'free'
    memoryBlockHeader* nextBlock = currentBlock->next; // set nextBlock to the next block
    memoryBlockHeader* previousBlock = NULL; // create previousBlock
    memoryBlockHeader* tempBlock = freeListHead; // set tempBlock to the head of the free list

    while (tempBlock != NULL && tempBlock < currentBlock){
        previousBlock = tempBlock; // set previous block to current
        tempBlock = tempBlock->next; // set tempBlock to next
    }

    if (previousBlock == NULL){ // if at the beginning of the list...
        freeListHead = currentBlock; // set the head of the free list to the current block
    } else { // if not at the beginning of the list...
        previousBlock->next = currentBlock; // set the next pointer of the previous block to the current block
    }

    currentBlock->next = nextBlock; // set the next pointer of the current block to the next block
    if (nextBlock != NULL && (unsigned char*)currentBlock + currentBlock->size == (unsigned char*)nextBlock){
        currentBlock->size += nextBlock->size; // combine the two blocks
        currentBlock->next = nextBlock->next; // set the next pointer of the current block to the next pointer of the next block
    }
}

