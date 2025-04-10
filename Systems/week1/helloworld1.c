#include <stdio.h>

//how c glues things together 
struct coord{
    int x; // like public instance variables
    int y;
    int z;

};

//swap two integers
void swap(int* x, int* y){
    int temp = *x;
    *x = *y;
    *y = temp;
    printf("%d %d\n", *x, *y);
}

int sum(int x, int y){
        x = 15;
        return x + y;
    }

void foo(int* a){
    a[4] = 32;
}

int main(){

    struct coord c1; // struct coord (bad name) is the type
    c1.x = 8; 



    int a = 3;
    int b = 8;




   int* pa; // variable declaraiton - pointer to an integer
   pa = &a;

   int c = *pa; // dereference

   // & - address of
   printf("%p\n", &a);
   printf("%p\n", &b);
   printf("%d\n", c);

   // create array of 5 ints
   int ar[5]; 
   // ar[2] = 53;

    swap(&a,&b);
    double z = 5.2;
   // char c = 'a';

  

    //d% int
    // %f float
    // %lf (long float) double

    printf("values are: %d %d %lf\n", a, b, z);

    if (a == 3){
    printf("Hello World\n");
    return 0;
    }
}