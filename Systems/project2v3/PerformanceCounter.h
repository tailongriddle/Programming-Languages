#ifndef PERFORMANCE_COUNTER_H
#define PERFORMANCE_COUNTER_H

#include <cmath>

class PerformanceCounter {
private:
    int hits;
    int misses;
    int writes;

public:
    PerformanceCounter();
    void incrementHits();
    void incrementMisses();
    void incrementWrites();
    int getHits();
    int getMisses();
    int getWrites();
    void display();
};
#endif 