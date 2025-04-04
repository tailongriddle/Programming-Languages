#ifndef DUMALLOC_H
#define DUMALLOC_H

#define Managed(p) (*p)
#define Managed_t(t) t*


// The interface for DU malloc and free
void duManagedInitMalloc(int searchType);
void** duManagedMalloc(int size);
void duManagedFree(void** mptr);
void duManagedListPrint();
void duInitMalloc();
void* duMalloc(int size);
void duFree(void* ptr);
void duMemoryDump();
void duMemoryBlockPrint();
void duFreeListPrint();



//


#endif