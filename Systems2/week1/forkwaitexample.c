#include <stdio.h>
#include <stdlib.h>
#include <unistd.h> // for fork
#include <sys/wait.h> // for waitpid

//run using "gcc filename -o filename" then "./filename"

int main(){ // string{} args 
    sleep(10);
    printf("about to fork\n");
    int pid = fork(); // create another process (now two processes are running)
    printf("%d\n", pid);
    if(pid == 0){
        // child process

        char* args[5]; // create an array of strings
        args[0] = "ls"; // first argument is the command, ls is a program sitting in a directory
        args[1] = "-l"; // second argument is the option
        args[2] = NULL; // last argument is NULL

        int rc = execvp(args[0], args); // execute the command
        printf("might never be reached\n");
        sleep(10);
    } else {
        // parent process
        int result;
        int status;
        result = waitpid(pid, &status, 0); // blocking
        printf("Parent reaped child\n");
    }
    sleep(20);

// do NOT fork bomb ---> while(1) {fork)()} this will break the servers like a DDOS attack
}