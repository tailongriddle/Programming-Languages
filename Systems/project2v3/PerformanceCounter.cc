#include "PerformanceCounter.h"
#include <iostream>

PerformanceCounter::PerformanceCounter() {
    hits = 0;
    misses = 0;
    writes = 0;
}

void PerformanceCounter::incrementHits() {
    hits++;
}

void PerformanceCounter::incrementMisses() {
    misses++;
}

void PerformanceCounter::incrementWrites() {
    writes++;
}

int PerformanceCounter::getHits() {
    return hits;
}

int PerformanceCounter::getMisses() {
    return misses;
}

int PerformanceCounter::getWrites() {
    return writes;
}

void PerformanceCounter::display() {
    printf("Hits: %d\n", hits);
    printf("Misses: %d\n", misses);
    printf("Writes: %d\n", writes);
}
