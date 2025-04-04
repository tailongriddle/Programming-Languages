#include <iostream>
#include <vector>
using namespace std;

int numRes;
int numProc;
int **resourceGraph;

// Display function for the resource graph
void displayResGraph() {
    for (int i = 0; i < numProc; i++) {
        for (int j = 0; j < numRes; j++) {
            cout << resourceGraph[i][j] << " ";
        }
        cout << endl;
    }
}

// DFS function for cycle detection in deadlock checking
bool dfs(int node, vector<bool>& visited, vector<bool>& recStack, bool isProcess) {
    visited[node] = true;
    recStack[node] = true;
    
    if (isProcess) { // Process to Resource (Philosopher to Chopstick)
        for (int j = 0; j < numRes; j++) {
            if (resourceGraph[node][j] == 1) { // Only consider requests (1) as part of circular wait
                if (!visited[j + numProc] && dfs(j + numProc, visited, recStack, false)) {
                    return true;
                } else if (recStack[j + numProc]) {
                    return true;
                }
            }
        }
    } else { // Resource to Process (Chopstick to Philosopher)
        for (int i = 0; i < numProc; i++) {
            // Only proceed if the philosopher is both holding (-1) and requesting another (1)
            if (resourceGraph[i][node - numProc] == -1) { 
                // Check if this philosopher is making a request for any other resource
                bool hasRequest = false;
                for (int j = 0; j < numRes; j++) {
                    if (resourceGraph[i][j] == 1) { // Check for an active request
                        hasRequest = true;
                        break;
                    }
                }
                
                // Continue DFS only if the philosopher is in a circular wait (holding and requesting)
                if (hasRequest) {
                    if (!visited[i] && dfs(i, visited, recStack, true)) {
                        return true;
                    } else if (recStack[i]) {
                        return true;
                    }
                }
            }
        }
    }
    
    recStack[node] = false;
    return false;
}



// Deadlock check that initiates DFS from each process
bool deadlockCheck() {
    vector<bool> visited(numProc + numRes, false);
    vector<bool> recStack(numProc + numRes, false);
    
    for (int i = 0; i < numProc; i++) {
        if (!visited[i]) {
            if (dfs(i, visited, recStack, true)) {
                return true;
            }
        }
    }
    return false;
}

// Deadlock tester function for hard-coded example graph
void deadlockTester() {
    numProc = 7;
    numRes = 6;
    
    // Initialize the resource graph
    resourceGraph = new int*[numProc];
    for (int i = 0; i < numProc; i++) {
        resourceGraph[i] = new int[numRes];
        for (int j = 0; j < numRes; j++) {
            resourceGraph[i][j] = 0;
        }
    }

    // Hard code the graph with provided relationships
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

    cout << "Resource Graph:" << endl;
    displayResGraph();

    // Run deadlock detection
    if (deadlockCheck()) {
        cout << "Deadlock detected\n";
    } else {
        cout << "No deadlock detected\n";
    }
}

// Resource acquisition function with deadlock check (simulating semaphore acquire)
void rgAcquire(int philosopher, int resource) {
    // Step 1: Set the request state in the resourceGraph (simulate request)
    resourceGraph[philosopher][resource] = 1;

    // Step 2: Check for deadlock after request is made
    if (deadlockCheck()) {
        cout << "Deadlock detected when philosopher " << philosopher 
             << " tries to acquire resource " << resource << endl;
        // Step 3: Revert request if deadlock is detected
        resourceGraph[philosopher][resource] = 0;
    } else {
        // Step 3: Set the acquired state if no deadlock is detected (simulate acquire)
        resourceGraph[philosopher][resource] = -1;
    }
}

// Resource release function (simulating semaphore release)
void rgRelease(int philosopher, int resource) {
    // Reset the state in resourceGraph to indicate resource release
    resourceGraph[philosopher][resource] = 0;
}

// Function for philosopher to take left chopstick
void takeLeftStick(int philosopher) {
    int leftChopstick = philosopher;
    rgAcquire(philosopher, leftChopstick);
}

// Function for philosopher to take right chopstick
void takeRightStick(int philosopher) {
    int rightChopstick = (philosopher + 1) % numRes;
    rgAcquire(philosopher, rightChopstick);
}

// Dining philosophers test scenario
void diningPhilosophersTest() {
    numProc = 5; // Number of philosophers
    numRes = 5;  // Number of chopsticks

    resourceGraph = new int*[numProc];
    for (int i = 0; i < numProc; i++) {
        resourceGraph[i] = new int[numRes];
        for (int j = 0; j < numRes; j++) {
            resourceGraph[i][j] = 0;
        }
    }

    // Step 1: Each philosopher acquires their left chopstick
    for (int i = 0; i < numProc; i++) {
        resourceGraph[i][i] = -1; // Mark as held by Philosopher i
    }

    cout << "Resource Graph after all philosophers acquire their left chopstick:" << endl;
    displayResGraph();

    // Step 2: Check for deadlock after left chopstick acquisition
    if (deadlockCheck()) {
        cout << "Deadlock detected after left chopstick acquisition\n";
        return; // Exit the test if deadlock is detected at this stage
    } else {
        cout << "No deadlock detected after left chopstick acquisition\n";
    }

    // Step 3: Each philosopher requests the chopstick to their right
    for (int i = 0; i < numProc; i++) {
        resourceGraph[i][(i + 1) % numRes] = 1; // Mark as requested by Philosopher i
    }

    cout << "Resource Graph after all philosophers request their right chopstick:" << endl;
    displayResGraph();

    // Step 4: Final deadlock check after all requests are made
    if (deadlockCheck()) {
        cout << "Deadlock detected after right chopstick requests\n";
    } else {
        cout << "No deadlock detected\n";

        // Step 5: If no deadlock, convert requests to held states
        for (int i = 0; i < numProc; i++) {
            resourceGraph[i][(i + 1) % numRes] = -1; // Mark as held by Philosopher i
        }

        cout << "Resource Graph after philosophers acquire their right chopstick:" << endl;
        displayResGraph();
    }
}

int main() {
    // Uncomment one of the following lines to test either function
    
    // Run the hard-coded deadlock test
    // deadlockTester();
    // exit(0); // Uncomment to exit after deadlockTester
    
    // Run the dining philosophers deadlock simulation
    diningPhilosophersTest();

    return 0;
}