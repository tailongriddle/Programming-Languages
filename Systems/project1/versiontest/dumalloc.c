#include <stdio.h>
#include "dumalloc.h"
#include <math.h>



unsigned char heap[HEAP_SIZE];

int allocationStrategy = 0;

//better convention
memoryBlockHeader * startofFree = (memoryBlockHeader*) heap;

void duInitMalloc(int strategy){
    for (int i = 0; i <= HEAP_SIZE; i++){
        heap[i] = 0; 
    }
// this is all created on the stack 
    memoryBlockHeader* header = (memoryBlockHeader*)heap;
// header -> size is the ame as (*header).size
    header->size = HEAP_SIZE - 16;
    header->next = NULL;
    header->free = 1; // Set the 'free' flag of the first header to 1
    allocationStrategy = strategy;// set the strategy 


// this will put the struct at the start of the array/heap as its value
//memoryBlockHeader * startofFree = (memoryBlockHeader*) heap;
//

}
void* duMalloc(int size){
    int truesize = (ceil(size/8.0) * 8);
    memoryBlockHeader *temp = startofFree;
    memoryBlockHeader *beforetemp = startofFree;
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
        if (temp == startofFree){
            startofFree = newheader;
    }
        // printf("EndofMalloc: %p, %d\n", temp, temp->size);
        // printf("Useraddresstemp: %p\n", temp+16);
        return temp+16;// we should be casting here (explicit abt returning a pointer)
        
    }
   
    
    return NULL;

}


void duFree(void* ptr)
{
   // printf("Useraddress: %p\n", ptr);
    memoryBlockHeader* blockHeader = ((memoryBlockHeader*)ptr) - sizeof(memoryBlockHeader);
    //printf("Beginning of Free: %p, %d\n", blockHeader, blockHeader->size);
    memoryBlockHeader* current = startofFree;
    blockHeader->free = 1;
    if (blockHeader<current){
        blockHeader->next = current;
        startofFree = blockHeader;
        
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
    int numChars = ((block->size)+16)/8; 
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
    unsigned char *temp = heap;
    int number = 0; 
    int number2 = 0; 
    while ((unsigned char*)temp < heap + HEAP_SIZE) {
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
    unsigned char *temp = heap;

    // Traverse through the memory blocks directly without using next pointer
    while ((unsigned char*)temp < heap + HEAP_SIZE) {
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

void duMemoryDump(){
    //print out the memory address and 
    //size of all the blocks on the free list
    memoryBlockHeader *temp = startofFree;
    printf("MEMORY DUMP\n");
    printf("Memory Block\n");
    printMemoryBlocks();
    printletters();
    printf("\nFree List\n");
    while (temp != NULL){
        printf("Block at%p, size %d\n", temp, temp->size);
        temp = temp->next;

    }


}
