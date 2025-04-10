//Compile: g++ dPhil.cc -std=c++20 -pthread -o dPhil
// Note we want the 2020 standard to use this version of semaphores
// This is an implementation of the Dining Philsophers problem
// It uses threads to run the philsophers
// It uses binary semaphores to control access to the chopsticks
// There is an array that tells which sticks (none, left, or both)
// that each phil currently holds. This array is not used in any
// way to control the running - simply to show deadlock at all hold left
#include <chrono>
#include <iostream>
#include <vector>
#include <semaphore>
#include <thread>
#include <cmath>

using namespace std;
int numPhil;
int thinkingMax = 10;
int eatingMax = 100;
binary_semaphore* screenLock;
binary_semaphore** chopstickLocks; // Will be an array of these
// Helper to more easily print who is holding which stick
char* stickHolding;

int numRes;
int numProc;
int** resourceGraph; 

// function prototypes
void displayResGraph();
bool processDFS(int process, bool* marked, bool* inStack);
bool resourceDFS(int resource, bool* marked, bool* inStack);


/***
 * 
 * Display the resource graph
 * 
*/
void displayResGraph(){
    cout << "Resource Graph\n"; 
    for (int i=0; i<numProc-1; i++) {
        cout << "P" << i << " ";
        for (int j=0; j<numRes; j++) {
            cout << resourceGraph[i][j] << " ";
        }
        cout << "\n";
    }
}

/***
 * 
 * Depth-first search on the process graph
 * 
*/
bool processDFS(int process, bool* marked, bool* inStack){
      if (!marked[process]) {
        marked[process] = true;
        inStack[process] = true;

        for (int j = 0; j < numRes; j++) {
            if (resourceGraph[process][j] == -1) {
                if (resourceDFS(j, marked, inStack)) {
                    return true;
                }
            } else if (resourceGraph[process][j] == 1) {
                if (inStack[process]){
                    return true;
                }
                
            }
        }
    }
    inStack[process] = false;
    return false;
}

/***
 * 
 * Depth-first search on the resource graph
 * 
*/
bool resourceDFS(int resource, bool* marked, bool* inStack){
    // look for all possible links be going down each resource column
    for (int i = 0; i < numProc; i++) {
        if (resourceGraph[i][resource] == -1) {
            if (!marked[i]) {
                if (processDFS(i, marked, inStack)) {
                    return true;
                }
            } else if (inStack[i]) {
                return true;
            }
        }
    }
    return false;
}
/***
 * 
 * Deadlock check
 * 
*/
int deadlockCheck(){
    
    // arrays for marked and visited nodes
    bool* marked = new bool[numProc]();
    bool* inStack = new bool[numProc]();
 

    // run depth-first search on each process node
    for (int i = 0; i < numProc; i++) {
        if (!marked[i]) {
            if (processDFS(i, marked, inStack)) {
                delete[] marked; 
                delete[] inStack;
                return 1;
            }
        }
    }

    // free memory
    delete[] marked; 
    delete[] inStack;

    return 0;

}

// hardcode the resource graph
void deadlockTester() {

    numProc = 7;
    numRes = 6;

    // First make a resource graph that has a cycle
    // Use the one from the slides
    // Init the resource Graph
    // It has 7 processes (A-G) and 6 resources (R-W)
    //   but we will call the processes 0-6 and the resources 0-5
    // Arcs out of process node are +1, into process node are -1
    resourceGraph = new int*[numProc];
    for (int i=0; i<numProc; i++) {
        resourceGraph[i] = new int[numRes];
        for (int j=0; j<numRes; j++) {
            resourceGraph[i][j] = 0;
        }
    }

    // Hard code the graph from the slides
    resourceGraph[0][0] = -1;  // R->A
    resourceGraph[0][1] = +1;  // A->S

    resourceGraph[1][2] = +1;  // B->T

    resourceGraph[2][1] = +1;  // C->S

    resourceGraph[3][1] = +1;  // D->S
    resourceGraph[3][2] = +1;  // D->T
    resourceGraph[3][3] = -1;  // U->D

    resourceGraph[4][2] = -1;  // T->E
    resourceGraph[4][4] = +1;  // E->V

    resourceGraph[5][1] = +1;  // F->S
    resourceGraph[5][5] = -1;  // W->F

    resourceGraph[6][3] = +1;  // G->U
    resourceGraph[6][4] = -1;  // V->G

    displayResGraph();

    // Check for cycle
    int deadlock = deadlockCheck();
    if (deadlock == 1) {
        std::cout << "Deadlock detected\n";
    } else {
        std::cout << "No deadlock detected\n";
    }
    

}

/***
 * 
 * Function to acquire a chopstick
 * 
*/
void rgAcquire(int phil, int chop) {
    resourceGraph[phil][chop] = 1; // trying to acquire
    if (deadlockCheck() == 1) {
        cout << "Deadlock detected by " << phil << " attempting to acquire chopstick" << endl; // deadlock was created by this acquire
    }
    chopstickLocks[chop]->acquire();  // acquire the chopstick

    resourceGraph[phil][chop] = -1; // acquired (update graph)

}

/***
 * 
 * Function to release a chopstick
 * 
*/
void rgRelease(int phil, int chop) {
    chopstickLocks[chop]->release(); // release the chopstick
    resourceGraph[phil][chop] = 0; // released (update graph)
}


// Helper methods to find the chopstick to the left and right of a philosopher
// Note that the right one is the same number as the philosopher
// and the left one is the number after the philosopher (wrapping around)

int left(int philNum) {
    return (philNum+1)%numPhil;
}
int right(int philNum) {
    return philNum;
}


void displaySticks() {
    screenLock->acquire(); // locking the screen
    cout << "[ ";
    for (int i=0; i<numPhil; i++) {
        cout << stickHolding[i] << " ";
    }
    cout << " ]\n";
    screenLock->release();
}


void think(int philNum) {
    int duration = (rand()%thinkingMax)+1; // time to think in ms
    screenLock->acquire(); // locking the screen
    cout << philNum << " is thinking for " << duration << "ms\n";
    screenLock->release();
    // Think...
    this_thread::sleep_for(chrono::milliseconds(rand()%duration));
}


void eat(int philNum) {
    int duration = (rand()%eatingMax)+1; // time to eat in ms
    screenLock->acquire(); // locking the screen
    cout << "" << philNum << " is EATING for " << duration << "ms\n";
    screenLock->release();
// Eat...
this_thread::sleep_for(chrono::milliseconds(rand()%duration));
}


void takeLeftStick(int philNum) {
    int left = philNum;
    rgAcquire(philNum, left);
    displaySticks();
}


void takeRightStick(int philNum) {
    int right = (philNum+1)%numPhil;
    rgAcquire(philNum, right);
    displaySticks();
}


void putSticks(int philNum) {
    // Return the chopsticks to the table
    screenLock->acquire(); // locking the screen
    cout << " " << philNum << " returning chopsticks\n";
    screenLock->release();
    // Display who is holding what now - do it while we still have it acquired
    stickHolding[philNum] = '-';
    displaySticks();
    displayResGraph();
    int left = philNum;
    int right = (philNum+1)%numPhil;
    rgRelease(philNum, left);
    rgRelease(philNum, right);
}


void philosopher(int philNum) {
    while (true) {
        think(philNum); // philosopher thinking
        takeLeftStick(philNum); // acquire left chopstick
        takeRightStick(philNum); // acquire right chopstick
        eat(philNum); // eat rice
        putSticks(philNum); // put both sticks back on table
    }
} 
int main() {
    // run deadlock tester
    //deadlockTester();
    //exit(0);
    numPhil = 5; // number of philosophers
    numProc = numPhil; // number of processes
    numRes = numPhil; // number of resources
    

    srand(0); // each run will be the same - good for testing
    // Create the screenLock
    screenLock = new binary_semaphore(1); // make it available
    numPhil = 5; // number of philosophers
    // Create the locks on the chopsticks - one for each
    chopstickLocks = new binary_semaphore*[numPhil];
    for (int i=0; i<numPhil; i++) {
        chopstickLocks[i] = new binary_semaphore(1); // chopstick is available
    }
    // Create the helper to identify who is holding what (just for printing)
    stickHolding = new char[numPhil];
    for (int i=0; i<numPhil; i++) {
        stickHolding[i] = '-'; // None
    }

    // initialize resource graph
    resourceGraph = new int*[numProc];
    for (int i = 0; i < numProc; ++i) {
        resourceGraph[i] = new int[numRes]();
    }


    // Start the philosophers in threads
    thread* ths[numPhil];
    for (int i=0; i<numPhil; i++) {
        thread* thPhil = new thread(philosopher, i);
        ths[i] = thPhil;
    }
    // Wait for them all to stop
    for (int i=0; i<numPhil; i++) {
        ths[i]->join();
    }
   // Free dynamically allocated memory
    for (int i = 0; i < numPhil; i++) {
        delete chopstickLocks[i]; // Free each chopstick lock
    }
    delete[] chopstickLocks; // Free the chopstickLocks array
    delete[] stickHolding; // Free stickHolding array


    // free resource graph memory
    for (int i = 0; i < numProc; ++i) {
        delete[] resourceGraph[i];
    }

    delete[] resourceGraph;
    return 0;
}
