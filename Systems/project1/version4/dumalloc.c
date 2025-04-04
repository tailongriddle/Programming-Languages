#include <stdio.h>
#include "dumalloc.h"
#include <math.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

#define NUM_HEAPS 3 // changed to 3
void* ManagedList[HEAP_SIZE / 8]; // Managed List array



unsigned char heaps[NUM_HEAPS][HEAP_SIZE];// 2-D list 
memoryBlockHeader* startofFree[NUM_HEAPS];// making an array of 2 things 


int currentHeap = 0;
int oldHeap = 2; //defines old heap as 2
int allocationStrategy = 0;
int managedlistsize = 0;
int mallocState = 0; // 0 for young, 1 for old 


//memoryBlockHeader * startofFree = (memoryBlockHeader*) heap;

void duInitMalloc(int strategy){
    for (int i = 0; i<NUM_HEAPS ; i++){
        memset(heaps[i], 0, HEAP_SIZE); 

    }
    
    // this is all created on the stack 
    for (int i = 0; i < NUM_HEAPS; i++){
        memoryBlockHeader* header = (memoryBlockHeader*)heaps[i];
        // header -> size is the ame as (*header).size
        header->size = HEAP_SIZE - sizeof(memoryBlockHeader);
        header->next = NULL;
        header->free = 1; // Set the 'free' flag of the first header to 1
        header->survivalAmt = 0; // Set the survival amount to 0
        startofFree[i] = header;

    }
    
    allocationStrategy = strategy;// set the strategy 



}

void duManagedInitMalloc(int strategy){
    mallocState = 0; // set malloc state to young
    duInitMalloc(strategy); // Call the original initialization function
    

    // Initialize managed list
    for (int i = 0; i < (HEAP_SIZE / 8); i++) {
        ManagedList[i] = NULL;
    }
}

void** duManagedMalloc(int size) {
    //managed list is an array of pointers to the heap 
    //you want pointers to the index of the managed list 
    // you want to return the pointer to the managed list 
    mallocState = 0; // set malloc state to young
    ManagedList[managedlistsize] = (void*)duMalloc(size); // Call the original malloc function (pointer to the heap)
    if (ManagedList[managedlistsize] == NULL){
        return NULL; // Allocation failed
    } 
    
    // Find an empty slot in the managed list
    // Set the managed index in the heap block itself
   // *(int*)managedPtr -> managedIndex = managedlistsize; //cast to int pointer and then dereference 
    managedlistsize++;
    

    return (void**)&ManagedList[managedlistsize-1];
    //return &managedPtr;
}


void duManagedFree(void** mptr) {
    if (mptr == NULL || *mptr == NULL) return; // Invalid or already freed pointer
    
    int managedIndex = ((memoryBlockHeader*)(*mptr - sizeof(memoryBlockHeader)))->managedIndex;
    
    duFree(*mptr); // Call the original free function
    ManagedList[managedIndex] = NULL; // Nullify the managed pointer
    *mptr = NULL; // Nullify the pointer

}

void printManagedList() {
    printf("\nManagedList\n");
    for (int i = 0; i < managedlistsize; i++) {
        if (ManagedList[i] == NULL){
            printf("ManagedList[%d] = nil\n", i);
        }
        else{
            printf("ManagedList[%d] = %p\n", i, ManagedList[i]);
        }
    }
}


void* duMalloc(int size){
    //printf("address: %p\n", startofFree[currentHeap]);
    if (mallocState == 0){
         int truesize = (ceil(size/8.0) * 8);
    memoryBlockHeader *temp = startofFree[currentHeap];
    memoryBlockHeader *beforetemp = startofFree[currentHeap];
    if (allocationStrategy == FIRST_FIT) {
        while (temp != NULL && temp->size < truesize+sizeof(memoryBlockHeader) ){
            //printf("advancing because %d smaller than %lu\n", temp->size, truesize+sizeof(memoryBlockHeader));
            beforetemp = temp;
            temp = temp->next;

        }
    } else if (allocationStrategy == BEST_FIT) {
        int mindiff = HEAP_SIZE+1;
        memoryBlockHeader *reference = NULL;
        while (temp != NULL){ 
            int s = (temp->size) - (truesize + sizeof(memoryBlockHeader));
            if (s < mindiff && s>0 ){
                mindiff = s; 
                reference = temp; 
            }
            temp = temp->next; 
        }
        temp = reference;
    }
    if (temp == NULL){
        return NULL;
    }
    if (temp->size > truesize){
        // Allocate the top part to the user
        temp->free = 0;
        temp->survivalAmt = 0; // Reset the survival amount to 0

        //printf("value: %lu\n", truesize+sizeof(memoryBlockHeader));  
        memoryBlockHeader *newheader = (memoryBlockHeader*) (((unsigned char*)temp)+truesize+sizeof(memoryBlockHeader));
        newheader->size = (temp->size)-truesize-sizeof(memoryBlockHeader);
        newheader->next = temp->next;
        newheader->free = 1; // Set the 'free' flag of the new header to 1 (indicating free)
        beforetemp->next = newheader;// this should in an else after startofFree
        
        temp->size = truesize;
        temp->next = NULL; 
        if (temp == startofFree[currentHeap]){
            startofFree[currentHeap] = newheader;
        }
        // printf("EndofMalloc: %p, %d\n", temp, temp->size);
        // printf("EndofMalloc: %lu\n", sizeof(memoryBlockHeader));
        // printf("EndofMalloc: %p, \n", ((unsigned char*)temp)+sizeof(memoryBlockHeader));

        // printf("Useraddresstemp: %p\n", temp+16);

        return ((unsigned char*)temp)+sizeof(memoryBlockHeader);// we should be casting here (explicit abt returning a pointer)
        
    }
    
    } else {
         int truesize = (ceil(size/8.0) * 8);
    memoryBlockHeader *temp = startofFree[oldHeap]; // Update to iterate over the old heap
   // printf("OldHeap: %p\n", startofFree[currentHeap]);
    memoryBlockHeader *beforetemp = startofFree[oldHeap]; // Update to iterate over the old heap
    if (allocationStrategy == FIRST_FIT) {
        while (temp != NULL && temp->size < truesize+sizeof(memoryBlockHeader) ){
            //printf("advancing because %d smaller than %lu\n", temp->size, truesize+sizeof(memoryBlockHeader));
            beforetemp = temp;
            temp = temp->next;
           // printf("temp: %p\n", temp);

        }
    } else if (allocationStrategy == BEST_FIT) {
        int mindiff = HEAP_SIZE+1;
        memoryBlockHeader *reference = NULL;
        while (temp != NULL){ 
            int s = (temp->size) - (truesize + sizeof(memoryBlockHeader));
            if (s < mindiff && s>0 ){
                mindiff = s; 
                reference = temp; 
            }
            temp = temp->next; 
        }
        temp = reference;
    }
    if (temp == NULL){
        return NULL;
    }
    if (temp->size > truesize){
        // Allocate the top part to the user
        temp->free = 0;
        temp->survivalAmt = 0; // Reset the survival amount to 0
         
        //printf("value: %lu\n", truesize+sizeof(memoryBlockHeader));  
        memoryBlockHeader *newheader = (memoryBlockHeader*) (((unsigned char*)temp)+truesize+sizeof(memoryBlockHeader));
        newheader->size = (temp->size)-truesize-sizeof(memoryBlockHeader);
        newheader->next = temp->next;
        newheader->free = 1; // Set the 'free' flag of the new header to 1 (indicating free)

        beforetemp->next = newheader;// this should in an else after startofFree
        
        temp->size = truesize;
        temp->next = NULL; 
        if (temp == startofFree[oldHeap]){
            startofFree[oldHeap] = newheader;
        }
        // printf("EndofMalloc: %p, %d\n", temp, temp->size);
        // printf("EndofMalloc: %lu\n", sizeof(memoryBlockHeader));
        // printf("EndofMalloc: %p, \n", ((unsigned char*)temp)+sizeof(memoryBlockHeader));

        // printf("Useraddresstemp: %p\n", temp+16);

        return ((unsigned char*)temp)+sizeof(memoryBlockHeader);// we should be casting here (explicit abt returning a pointer)
        
    }
   
    }
   
    
    return NULL;

}


void duFree(void* ptr)
{
   // printf("Useraddress: %p\n", ptr);
    unsigned char *p = (unsigned char*)ptr;
    memoryBlockHeader* blockHeader = (memoryBlockHeader *)(p - sizeof(memoryBlockHeader));
    memoryBlockHeader* current; 

    // start the loop at the beginning of the heap
    unsigned char *oldTemp = heaps[oldHeap]; //set to old heap
    unsigned char *newTemp = heaps[currentHeap]; //set to new heap

    // check to see if pointer is on old or new heap
    while ((unsigned char*)oldTemp < heaps[oldHeap] + HEAP_SIZE) { // iterate through the old heap
        memoryBlockHeader *header = (memoryBlockHeader*) oldTemp; // cast to memoryBlockHeader
        if ((memoryBlockHeader*)blockHeader == (memoryBlockHeader*)oldTemp){ // check if the blockHeader is the same as the oldTemp
            current = startofFree[oldHeap]; // set the current to the start of the free list for the old heap
            break; // break out of the loop
        }
        oldTemp += header->size + sizeof(memoryBlockHeader); // move to the next block
    }

    while ((unsigned char*)newTemp < heaps[oldHeap] + HEAP_SIZE) { // iterate through the new heap
        memoryBlockHeader *header = (memoryBlockHeader*) newTemp; // cast to memoryBlockHeader 
        if ((memoryBlockHeader*)blockHeader == (memoryBlockHeader*)newTemp){ // check if the blockHeader is the same as the newTemp
            current = startofFree[currentHeap]; // set the current to the start of the free list for the new heap
            break; // break out of the loop
        } 
        newTemp += header->size + sizeof(memoryBlockHeader); // move to the next block
    }

    //printf("Beginning of Free: %p, %d\n", blockHeader, blockHeader->size);
    //memoryBlockHeader* current = startofFree[currentHeap]; 

    blockHeader->free = 1; // Set the 'free' flag of the block to 1
    blockHeader->survivalAmt = 0; // Reset the survival amount to 0

    if (blockHeader < current){
        blockHeader->next = current;
        startofFree[currentHeap] = blockHeader;
        
        return;
    }
    while (current->next != NULL && current->next < blockHeader) {
        current = current->next;
    }
    
    blockHeader->next = current->next;
    current->next = blockHeader;
    printf("Survival amount: %d\n", blockHeader->survivalAmt); //print to test
}


 
// void printMemoryBlock(memoryBlockHeader *block){
//     printf("%s at %p, size %d \n", (block->free == 0 ? "Used" : "Free"), block, block-> size);
// }

void printGraphicalRepresentation(memoryBlockHeader *block, int i, int k){
    int numChars = ((block->size)+sizeof(memoryBlockHeader))/8; 
    for (int j = 0; j<=numChars+1; j++){
        if (block->free == 0) {
            printf("%c", 'A' + i);// why cant i increment i here? 
        } else {
            printf("%c", 'a' + k);
        }
        //printf("%c",(block->free == 0 ? 'A'+i : 'a'+i));
    }
}

// void printfreelist(void ){
//     printf("Free List\n");
//     while (temp != NULL){
//         printf("Block at%p, size %d\n", temp, temp->size);
//         temp = temp->next;

// }

void printletters(int heapNum) {
    unsigned char *temp = heaps[heapNum];
    int number = 0; 
    int number2 = 0; 
    while ((unsigned char*)temp < heaps[heapNum] + HEAP_SIZE) {
        memoryBlockHeader *header = (memoryBlockHeader*) temp;
        printGraphicalRepresentation(header, number, number2);
        if (header->free == 0) {// why do I have to increment i here? 
            number++;
        } else {
            number2++;
        }
        temp += header->size + sizeof(memoryBlockHeader);
    }



}
void printMemoryBlocks(int heapNum) {
    // Start the loop at the beginning of the heap
    unsigned char *temp = heaps[heapNum];

    // Traverse through the memory blocks directly without using next pointer
    while ((unsigned char*)temp < heaps[heapNum] + HEAP_SIZE) {
        memoryBlockHeader *header = (memoryBlockHeader*) temp;
        
        if (header->free == 0) {
            printf("Used at %p, size %d, surv: %d\n", temp, header->size, header->survivalAmt);
        } else {
            printf("Free at %p, size %d, surv: %d\n", temp, header->size, header->survivalAmt);
        }

        // Move to the next block by adding the size of the current block
        // Don't forget to adjust for header size
    
        temp  += header->size + sizeof(memoryBlockHeader);
        //printf("tempvalue: %lu\n", (header->size + sizeof(memoryBlockHeader)));
    }
}

void minorCollection(){
    mallocState = 1; // set malloc state to old
    startofFree[currentHeap] = (memoryBlockHeader*) heaps[currentHeap];
    unsigned char *src = NULL;// pointer or the source 
    currentHeap = (currentHeap + 1)%2; // switch current heap to other young heap (changed from NUM_HEAPS)

    //unsigned char *dest = (unsigned char*)startofFree[currentHeap];
    for (int i = 0; i< managedlistsize; i ++){
        if (ManagedList[i]!= NULL) {
            unsigned char *dest = (unsigned char*)startofFree[currentHeap];
            // the source is the managed lists address which is the content on the heap 
            src = ((unsigned char*) ManagedList[i])- sizeof(memoryBlockHeader); 
            memoryBlockHeader *header = (memoryBlockHeader*) src;
            header->survivalAmt += 1; // increment survival count
            printf("Survival amount: %d\n", header->survivalAmt); //print to test
            
            // if the survival amount reaches the threshold (3), move the block to the old heap
            if (header->survivalAmt >= 3) { 

                header->survivalAmt = 0; // reset survival amount
                // allocate space for the block on the old heap using duMalloc
               // duMemoryDump(); //to test old heap free space
                unsigned char *oldHeapPtr = duMalloc(header->size);
                //printf("Old Heap Pointer: %p\n", oldHeapPtr); //print to test
                //memcpy the contents of the memory block over once we have our pointer from duMalloc              
                memoryBlockHeader* temp = (memoryBlockHeader*) src;
                memcpy(oldHeapPtr, src, temp->size);
                //update the managed list to point to the new location of the block
                ManagedList[i] = (memoryBlockHeader*)((oldHeapPtr)); 
                //update the start of the free list for the old heap
                startofFree[oldHeap] = (memoryBlockHeader*) (oldHeapPtr + header->size);               
                
            } else {
                // if the block is not moved to the old heap, copy the block to the new heap
                memcpy(dest, src, sizeof(memoryBlockHeader) + ((memoryBlockHeader*)src)->size);
                // update the managed list to point to the new location of the block
                ManagedList[i] = (memoryBlockHeader*)((dest) + sizeof(memoryBlockHeader));
                // update the start of the free list for the new heap
                startofFree[currentHeap] = (memoryBlockHeader*) (dest + ((memoryBlockHeader*)src)->size + sizeof(memoryBlockHeader));
            }
        }
        
        
        memoryBlockHeader* newheader = (memoryBlockHeader*) startofFree[currentHeap]; 
        newheader -> size = HEAP_SIZE - (((unsigned char*)startofFree[currentHeap]-heaps[currentHeap])+sizeof(memoryBlockHeader));
        newheader -> free = 1; 
        newheader -> next = NULL; 
    }

}

void majorCollection() {
    unsigned char *heapStart = heaps[oldHeap];
    unsigned char *heapEnd = heapStart + HEAP_SIZE;
    memoryBlockHeader *current = (memoryBlockHeader *)heapStart;
    memoryBlockHeader *lastFreeBlock = NULL;

    // traverse old heap
    while ((unsigned char *)current < heapEnd) {
        // if  block is free
        if (current->free) {
            // if we have a last free block, coalesce
            if (lastFreeBlock) {
                lastFreeBlock->size += current->size + sizeof(memoryBlockHeader);
                lastFreeBlock->next = current->next;
            } else {
                // set this block as the last free block
                lastFreeBlock = current;
            }
        } else {
            // if the block is used and there is a last free block, move it
            if (lastFreeBlock) {
                // calculate new location for the used block
                unsigned char *newLocation = (unsigned char *)lastFreeBlock;
                unsigned char *oldLocation = (unsigned char *)current;

                // move the used block
                memmove(newLocation, oldLocation, current->size + sizeof(memoryBlockHeader));

                // update the managed list to point to the new location
                for (int i = 0; i < managedlistsize; i++) {
                    if (ManagedList[i] == (memoryBlockHeader *)(oldLocation + sizeof(memoryBlockHeader))) {
                        ManagedList[i] = (memoryBlockHeader *)(newLocation + sizeof(memoryBlockHeader));
                    }
                }

                // update the last free block
                lastFreeBlock = (memoryBlockHeader *)(newLocation + current->size + sizeof(memoryBlockHeader));
                lastFreeBlock->size = heapEnd - (unsigned char *)lastFreeBlock - sizeof(memoryBlockHeader);
                lastFreeBlock->free = 1;
                lastFreeBlock->next = NULL;
            }
        }

        // move to the next block
        current = (memoryBlockHeader *)((unsigned char *)current + current->size + sizeof(memoryBlockHeader));
    }

    // set last free block's next pointer 
    if (lastFreeBlock) {
        lastFreeBlock->next = NULL;
    }

    // rebuild  free list
    startofFree[oldHeap] = lastFreeBlock;
}





void duMemoryDump(){
    //print out the memory address and 
    //size of all the blocks on the free list
    memoryBlockHeader *temp = startofFree[currentHeap];
    printf("MEMORY DUMP\nCurrent heap (0/1 young): %d\n", currentHeap);
    printf("Memory Block\n");
    printMemoryBlocks(currentHeap);
    printletters(currentHeap);
    printf("\nFree List\n");
    while (temp != NULL){
        printf("Block at%p, size %d\n", temp, temp->size);
        temp = temp->next;

    }
    //Old Heap
    memoryBlockHeader *newTemp = startofFree[oldHeap]; //set to old heap
    printf("Old Heap\n");
    printf("Memory Block\n");
    printMemoryBlocks(oldHeap);
    printletters(oldHeap);
    printf("\nFree List\n");
    while (newTemp != NULL){
        printf("Block at%p, size %d\n", newTemp, newTemp->size);
        newTemp = newTemp->next;

    }
    printManagedList();



}
