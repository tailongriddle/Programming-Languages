#include <stdio.h>
#include "dumalloc.h"
#include <math.h>
#include <stdlib.h>
#include <string.h>

#define NUM_HEAPS 2 // changed to 3



unsigned char heaps[NUM_HEAPS][HEAP_SIZE];// 2-D list 
memoryBlockHeader* startofFree[NUM_HEAPS];// making an array of 2 things 


int currentHeap = 0;
int allocationStrategy = 0;
int managedlistsize = 0;


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
        startofFree[i] = header;

    }
    
    allocationStrategy = strategy;// set the strategy 



}

void duManagedInitMalloc(int strategy){
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
   
    
    return NULL;

}


void duFree(void* ptr)
{
   // printf("Useraddress: %p\n", ptr);
    unsigned char *p = (unsigned char*)ptr;
    memoryBlockHeader* blockHeader = (memoryBlockHeader *)(p - sizeof(memoryBlockHeader));
    //printf("Beginning of Free: %p, %d\n", blockHeader, blockHeader->size);
    memoryBlockHeader* current = startofFree[currentHeap];
    blockHeader->free = 1;
    if (blockHeader<current){
        blockHeader->next = current;
        startofFree[currentHeap] = blockHeader;
        
        return;
    }
    while (current-> next != NULL && current->next< blockHeader) {
        current = current->next;
    }
    
    blockHeader->next = current->next;
    current->next = blockHeader;
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

void printletters() {
    unsigned char *temp = heaps[currentHeap];
    int number = 0; 
    int number2 = 0; 
    while ((unsigned char*)temp < heaps[currentHeap] + HEAP_SIZE) {
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
void printMemoryBlocks() {
    // Start the loop at the beginning of the heap
    unsigned char *temp = heaps[currentHeap];

    // Traverse through the memory blocks directly without using next pointer
    while ((unsigned char*)temp < heaps[currentHeap] + HEAP_SIZE) {
        memoryBlockHeader *header = (memoryBlockHeader*) temp;
        if (header->free == 0) {
            printf("Used at %p, size %d\n", temp, header->size);
        } else {
            printf("Free at %p, size %d\n", temp, header->size);
        }

        // Move to the next block by adding the size of the current block
        // Don't forget to adjust for header size
    
        temp  += header->size + sizeof(memoryBlockHeader);
        //printf("tempvalue: %lu\n", (header->size + sizeof(memoryBlockHeader)));
    }
}


void minorCollection(){
    startofFree[currentHeap] = (memoryBlockHeader*) heaps[currentHeap];
    currentHeap = (currentHeap + 1)%NUM_HEAPS;
    unsigned char *src = NULL;// pointer or the source 
    unsigned char *dest = (unsigned char*)startofFree[currentHeap];



    for (int i = 0; i< managedlistsize; i ++){
        if (ManagedList[i]!= NULL) {
            unsigned char *dest = (unsigned char*)startofFree[currentHeap];
            src = ((unsigned char*) ManagedList[i])- sizeof(memoryBlockHeader); // the source is the managed lists address which is the content on the heap 
            // printf("pointer: %p\n",((unsigned char*) ManagedList[i]));//(unsigned char*)
            // printf("anotherp: %p\n", heaps[0]);
            // printf("Size of memory to copy: %d\n", ((memoryBlockHeader*)src)->size);
            memcpy(dest, src, sizeof(memoryBlockHeader) + ((memoryBlockHeader*)src)->size);
            ManagedList[i] = (memoryBlockHeader*)((dest) + sizeof(memoryBlockHeader));
            // printf("ManagedList pointer: %p\n", ManagedList[i]);
            // printf("before: %p\n", startofFree[currentHeap]);
            startofFree[currentHeap] = (memoryBlockHeader*) (dest + ((memoryBlockHeader*)src)->size + sizeof(memoryBlockHeader));
            //printf("after: %p\n", startofFree[currentHeap]);

        }

        memoryBlockHeader* newheader = (memoryBlockHeader*) startofFree[currentHeap]; 
        newheader -> size = HEAP_SIZE - (((unsigned char*)startofFree[currentHeap]-heaps[currentHeap])+sizeof(memoryBlockHeader));
        newheader -> free = 1; 
        newheader -> next = NULL; 


    }
    
}



void duMemoryDump(){
    //print out the memory address and 
    //size of all the blocks on the free list
    memoryBlockHeader *temp = startofFree[currentHeap];
    printf("MEMORY DUMP\nCurrent heap (0/1 young): %d\n", currentHeap);
    //printf("MEMORY DUMP\n"); changed by removing 
    printf("Memory Block\n");
    printMemoryBlocks();
    printletters();
    printf("\nFree List\n");
    while (temp != NULL){
        printf("Block at%p, size %d\n", temp, temp->size);
        temp = temp->next;

    }
    printManagedList();



}
