#include <iostream>
#include <vector>
#include <string>
#include <thread>
#include <cmath>

/***
 * 
 * Checks if prime
 * 
 * 
 * 
*/
bool isPrime(int num) {
   int i = 2;
    
    if (num == 2) { // exception for 2
      return true;
    }

    if (num == 1){
      return false; 
    }
    
    while (i * i <= num) { // test numbers from 2 up
      //System.out.println("num is: " + num + ", i is: " + i);
      if (num % i == 0) { // if divisible
        return false; // it is not prime!       
      }
      
      i++;
      
    }
    
    return true;
  }
  
/***
 * 
 * Counts primes in range
 * 
 * 
*/
int countPrime(int num1, int num2) {
    
    int count = 0;
    
    for (int i = num1; i < num2; i++) {    
      if (isPrime(i)) {
        //System.out.println(i);
        count++;
      } 
      
    }
    
    return count;
  }
  
  
 void myRun(int threadNum, int start, int stop, int results[]) {
  //std::cout << n << " " << start << " - " << stop << "\n";
  results[threadNum] = countPrime(start,stop);
  std::string output = "Thread " + std::to_string(threadNum) + " Range: " + std::to_string(start) + " - " +
  std::to_string(stop) + "| Primes: " + std::to_string(results[threadNum]) + "\n" ;
  std::cout << output;


}

int main(){


// START TIME HERE
int num1 = 1000;
int num2 = 1000000;
int stop;
int totalPrimes = 0;

int totalNums = num2 - num1;
// Note that these need to be on the heap in order to pass
// as parameters to threads
int* results = (int*)malloc(totalNums*sizeof(int)); // allocate space for results list 


int numThreads = 2; // number of threads
std::thread* threads[numThreads];  
for (int i=0; i<numThreads; i++) { // for each thread in threads
      int start = num1 + (i * (totalNums / numThreads));
      if (i == numThreads - 1 && (totalNums / numThreads % 1 != 0)) {
        stop = num1 + ((i + 1) * (totalNums / numThreads)) + 2;
      } else {
        stop = num1 + ((i + 1) * (totalNums / numThreads) + 1);
      }
      
std::thread* newThread = new std::thread(myRun, i, start, stop, results);
threads[i] = newThread;
}
for (int i=0; i<numThreads; i++) {
threads[i]->join();
}
for (int i=0; i<numThreads; i++) {
  totalPrimes += results[i];
}

// END TIME HERE

//std::cout << "Total Primes: " << std::to_string(totalPrimes) << "\n";
free(results);

  //test isPrime
  // std::cout << "85: " << std::boolalpha << isPrime(85) << std::endl;
  // std::cout << "7: " << std::boolalpha << isPrime(7) << std::endl;
  // std::cout << "2: " << std::boolalpha << isPrime(2) << std::endl;
  // std::cout << "9: " << std::boolalpha << isPrime(9) << std::endl;
  // std::cout << "1087: " << std::boolalpha << isPrime(1087) << std::endl;
  // std::cout << "733260091: " << std::boolalpha << isPrime(733260091) << std::endl;
  std::cout << "1000, 1000000: " << countPrime(1000,1000000) << std::endl;


  // TO BE TIMED:
 // countPrime(1000,1000);
  //TIME: 
  //One thread: 
// real	0m1.152s
// user	0m0.823s
// sys	0m0.000s

  //Two threads: real	0m0.429s
  // real	0m0.725s
  // user	0m0.838s 
  // sys	0m0.004s


  
}

