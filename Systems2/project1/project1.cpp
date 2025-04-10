#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/wait.h>
#include <signal.h>

#define MAX_INPUT_SIZE 1024
#define MAX_ARG_SIZE 100
#define MAX_HISTORY 100

char history[MAX_HISTORY][MAX_INPUT_SIZE];
int history_count = 0;

// Function to handle the SIGCHLD signal for cleaning up zombie processes
void sigchld_handler(int signo) {
    // Reap all dead children
    while (waitpid(-1, NULL, WNOHANG) > 0);
}

// Function to parse the input into tokens
int parse_input(char *input, char **args) {
    int arg_count = 0;
    char *token = strtok(input, " \t\n");
    while (token != NULL && arg_count < MAX_ARG_SIZE - 1) {
        args[arg_count++] = token;
        token = strtok(NULL, " \t\n");
    }
    args[arg_count] = NULL; // Null-terminate the array
    return arg_count;
}

// Function to save command to history
void save_to_history(char *input) {
    // Don't save empty input or repeated history commands
    if (input[0] == '\n' || (history_count > 0 && strcmp(history[history_count - 1], input) == 0)) return;

    // Save command to history
    strncpy(history[history_count % MAX_HISTORY], input, MAX_INPUT_SIZE - 1);
    history[history_count % MAX_HISTORY][MAX_INPUT_SIZE - 1] = '\0'; // Ensure null-terminated
    history_count++;
}

// Function to check for input or output redirection
int handle_redirection(char **args, int arg_count) {
    for (int i = 0; i < arg_count; ++i) {
        if (strcmp(args[i], ">") == 0) {
            freopen(args[i + 1], "w", stdout); // Redirect stdout to file
            args[i] = NULL; // Remove redirection from args
            return 1;
        } else if (strcmp(args[i], "<") == 0) {
            freopen(args[i + 1], "r", stdin); // Redirect stdin from file
            args[i] = NULL; // Remove redirection from args
            return 1;
        }
    }
    return 0;
}

// Function to print command history
void print_history() {
    int start = history_count > MAX_HISTORY ? history_count - MAX_HISTORY : 0;
    for (int i = start; i < history_count; ++i) {
        printf("%d %s", i - start + 1, history[i % MAX_HISTORY]);
    }
}

// Function to execute a command from history
int execute_from_history(int index, char **args) {
    if (index < 1 || index > history_count || (history_count > MAX_HISTORY && index > MAX_HISTORY)) {
        fprintf(stderr, "No such command in history.\n");
        return -1;
    }

    int history_index = (history_count > MAX_HISTORY ? (history_count - MAX_HISTORY) + index - 1 : index - 1);
    printf("Executing: %s", history[history_index % MAX_HISTORY]);
    
    // Parse and execute the command from history
    parse_input(history[history_index % MAX_HISTORY], args);
    return 0;
}

// Main shell loop
int main() {
    char input[MAX_INPUT_SIZE];
    char *args[MAX_ARG_SIZE];
    char cwd[1024];
    pid_t pid;
    int background;

    // Set up signal handler to reap zombie processes
    signal(SIGCHLD, sigchld_handler);

    while (1) {
        // Get the current working directory
        if (getcwd(cwd, sizeof(cwd)) != NULL) {
            printf("%s> ", cwd);
        } else {
            perror("getcwd");
            exit(EXIT_FAILURE);
        }

        // Get input from the user
        if (fgets(input, MAX_INPUT_SIZE, stdin) == NULL) {
            perror("fgets");
            continue;
        }

        // Save to history
        save_to_history(input);

        // Parse the input into arguments
        int arg_count = parse_input(input, args);

        // Check if the command is empty
        if (arg_count == 0) {
            continue;
        }

        // Handle shell-specific commands
        if (strcmp(args[0], "exit") == 0) {
            break; // Exit the shell
        } else if (strcmp(args[0], "cd") == 0) {
            if (arg_count > 1) {
                if (chdir(args[1]) != 0) {
                    perror("cd");
                }
            } else {
                fprintf(stderr, "cd: missing argument\n");
            }
            continue;
        } else if (strcmp(args[0], "history") == 0) {
            print_history();
            continue;
        } else if (args[0][0] == '!') {
            // Handle executing a specific history command
            int index = atoi(args[0] + 1);
            if (execute_from_history(index, args) != 0) {
                continue;
            }
        }

        // Check if the command is to be run in the background
        background = (strcmp(args[arg_count - 1], "&") == 0);
        if (background) {
            args[arg_count - 1] = NULL; // Remove '&' from args
        }

        // Fork a child process to execute the command
        pid = fork();
        if (pid < 0) {
            perror("fork");
            continue;
        }

        // Child process
        if (pid == 0) {
            // Handle redirection if any
            handle_redirection(args, arg_count);

            // Execute the command
            if (execvp(args[0], args) < 0) {
                perror("execvp");
                exit(EXIT_FAILURE);
            }
        } else {
            // Parent process
            if (!background) {
                // Wait for the child process to complete if not background
                waitpid(pid, NULL, 0);
            }
        }
    }
    return 0;
}