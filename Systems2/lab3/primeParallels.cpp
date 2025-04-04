#include <iostream>
#include <omp.h>

// Prime Finding

/***
 * 
 * Checks if prime
 * 
 * 
 * 
*/
bool isPrime(int num) {
  if (num <= 1) {
    return false;
  }
  if (num == 2) {
    return true;
  }
  if (num % 2 == 0) {
    return false;
  }
  for (int i = 3; i * i <= num; i += 2) {
    if (num % i == 0) {
      return false;
    }
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
  for (int i = num1; i <= num2; i++) {
    if (isPrime(i)) {
      count++;
    }
  }
  return count;
}

// Parallel Partitioning
// Blocking
void blockingPrime(int start, int end, int threads) {
  double total_found = 0;
  double total_time = 0;
  int chunk = (end - start + 1) / threads; // chunk size
  std::cout << "Blocking:" << std::endl;

  #pragma omp parallel num_threads(threads) reduction(+:total_found, total_time)
  {
    int id = omp_get_thread_num(); // get thread id
    double start_time = omp_get_wtime(); // start time
    int numFound = countPrime(start + id * chunk, std::min(start + (id + 1) * chunk - 1, end)); // count prime
    double end_time = omp_get_wtime(); // end time
    double time = end_time - start_time; // time
    total_time += time; // add to total time
    total_found += numFound; // add to total found

    std::cout << "time for " << id << ": " << time << " with " << numFound << " found" << std::endl;
  }
  std::cout << "overall time: " << total_time << " with " << total_found << " found" << std::endl;
}

// Striping
// Break up entire range round robin
void stripingPrime(int start, int end, int threads) {
  double total_found = 0;
  double total_time = 0;
  std::cout << "Striping:" << std::endl;

  #pragma omp parallel num_threads(threads) reduction(+:total_found, total_time)
  {
    int id = omp_get_thread_num(); // get thread id
    double start_time = omp_get_wtime(); // start time
    int numFound = 0; // number of primes found

    #pragma omp for schedule(static) nowait
    for (int i = start; i <= end; ++i) { // Loop incrementing by 1 for each i
        if (isPrime(i)) {
              numFound++;
        }
    }
    double end_time = omp_get_wtime(); // end time
    double time = end_time - start_time; // time
    total_time += time; // add to total time
    total_found += numFound; // add to total found

    #pragma omp critical
    std::cout << "time for " << id << ": " << time << " with " << numFound << " found" << std::endl;
  }
  std::cout << "overall time: " << total_time << " with " << total_found << " found" << std::endl;
}

int main() {
  // TEST
  //std::cout << "10, 100: " << countPrime(10, 100) << std::endl; // test 1
  //std::cout << "1000, 1000000: " << countPrime(1000, 1000000) << std::endl; // test 2

  int start = 1000;
  int end = 1000000;
  int threadCount = 5;

  // Blocking
  blockingPrime(start, end, threadCount);

  // Striping
  stripingPrime(start, end, threadCount);

  return 0;
}