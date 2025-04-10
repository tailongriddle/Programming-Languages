#include <stdio.h>
#include "cacheMatrix.h" //find it in the same folder

// caching

// displays matrix
// args: M - matrix, n - size of matrix
void displayMatrix(int M[], int n){
for (int i = 0; i < (n * n); i++){
        printf("%d ", M[i]);
        if (M[i] < 10){
            printf(" ");
        }
        if ((i + 1) % n == 0){
            printf("\n");
        }
        
}

}

// multiplies two matrices
// args: A - matrix A, B - matrix B, C - matrix C, n - size of matrix
void matrixMultiply(int A[], int B[], int C[], int n){
    int aMult;
    int bMult;
    int toAdd = 0;

    for (int i = 0; i < n; i++){ // iterate through A 
        for (int j = 0; j < n; j++){  // iterate through B   
            for (int k = 0; k < n; k++){ // iterate through C
                aMult = A[k + (i * n)]; // A[i + j]
                //printf("aMult: %d\n", aMult);
                bMult = B[j + (k * n)]; // B[j + (k * n)]
                //printf("bMult: %d\n", bMult);
                toAdd += (aMult * bMult); // add to toAdd
                //printf("toAdd: %d\n", toAdd);
            }
        C[j + (i * n)] = toAdd; // add to C
        toAdd = 0;
        }
       
    }

}

// flips matrix rows and columns
// args: M - matrix, n - size of matrix
void transposeMatrix(int M[], int n){
int save;

for (int i = 0; i < n; i++){ // iterate through rows
    for (int j = 0; j < n; j++){ // iterate through columns
        if (i < j){
            save = M[j + (i * n)]; // save M[j + (i * n)]
            M[j + (i * n)] = M[i + (j * n)]; // M[j + (i * n)] = M[i + (j * n)]
            M[i + (j * n)] = save; // M[i + (j * n)] = save
        }
    }

}


}

// multiplies transposed matrices
// args: A - matrix A, B - matrix B, C - matrix C, n - size of matrix
void matrixMultiplyTranspose(int A[], int B[], int C[], int n){
    int aMult;
    int bMult;
    int toAdd = 0;

    for (int i = 0; i < n; i++){ // iterate through A 
        for (int j = 0; j < n; j++){  // iterate through B   
            for (int k = 0; k < n; k++){ // iterate through C
                aMult = A[k + (i * n)]; // A[i + j]
                //printf("aMult: %d\n", aMult);
                bMult = B[k + (j * n)]; // B[j + (k * n)]
                //printf("bMult: %d\n", bMult);
                toAdd += (aMult * bMult); // add to toAdd
                //printf("toAdd: %d\n", toAdd);
            }
        C[j + (i * n)] = toAdd; // add to C
        toAdd = 0;
        }

}
}


// creates and populates matrix
int main(){
    int n = 800; // size for matrix
    
    int A[n * n]; // A matrix
    int B[n * n]; // B matrix
    int C[n * n]; // C matrix

    for (int i = 0; i < (n * n); i++){  // populate A and B
            A[i] = i;
            B[i] = i;
    }
    
    //  printf("Matrix A:\n");
    //  displayMatrix(A, n);

    //  printf("Matrix B:\n");
    //  displayMatrix(B, n);

    // printf("Matrix C:\n");
     matrixMultiply(A, B, C, n);
    // displayMatrix(C, n);
    
    
    //printf("Transposed B:\n");
    //transposeMatrix(B, n);
    //displayMatrix(B, n);

    //printf("Matrix C:\n");
    //matrixMultiplyTranspose(A, B, C, n);
    //displayMatrix(C, n);


    return 0;
}

// Original time
//real	0m2.733s
//user	0m2.652s
//sys	0m0.008s

// Transposed time
//real	0m1.718s
//user	0m1.702s
//sys	0m0.012s