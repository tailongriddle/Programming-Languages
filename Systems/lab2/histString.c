#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// structFrec
// structure for frequencies
// tracks word and its frequency
struct freq {
    char* word;
    int frequency; // Added missing data type for frequency
}; //structures end with semicolons

typedef struct freq Histogram; // typedef used to replace struct freq

// readwords (mod)
// adds to array of words from file input
// retursn int* of words
char** readwords(int *wordsSize) {
    int capacity = 10; // initial capacity for words array
    char **words = (char**) malloc(capacity * sizeof(char*)); // Allocate memory for words array
    char currWord[100]; // Allocate memory for current word
    int wordLength = 0; // length of word

    while (scanf("%s", currWord) != EOF) {  //while not at the end of the file...
        wordLength = strlen(currWord);  // get length of word
        if (*wordsSize == capacity) { // Check if capacity exceeded
            capacity *= 2; // Double the capacity
            words = realloc(words, capacity * sizeof(char*)); // Resize words array
        }
        words[*wordsSize] = (char*)malloc((wordLength + 1) * sizeof(char)); // allocate memory for word in array, +1 for null terminator
        strcpy(words[*wordsSize], currWord); // copy current word into array
        (*wordsSize)++; //increment size of words entered into array
    }

    return words; // return array of words
}

// displaywords
// prints out all words in array
// returns void
void displaywords(char **words, int *wordsSize) {// no reason to pass as pointer if not modified
    for (int curr = 0; curr < *wordsSize; curr++) { // for each score...
        printf("word %d: %s\n", curr, words[curr]); // print out the score at i in words
    }
}


// calcHistogram (mod)
// adds to array of words from file input
// returns int histoSize
int* calcHistogram(char **words, int *wordsSize, Histogram **histogram, int *histoSize) {
    *histoSize = 0; // amount of freqs in histogram array

    // Allocate memory for histogram
    *histogram = (Histogram*)malloc(100 * sizeof(Histogram));

    Histogram toAdd; // create frequency to be added
    int isThere = 0; // initialize true/false value for whether or not the word already exists in the histogram

    for (int currS = 0; currS < *wordsSize; currS++) { // for each score...
        isThere = 0; //reset isThere to 0
        for (int currH = 0; currH < *histoSize; currH++) { // for each value in the histogram...
            if (strcmp(words[currS], (*histogram)[currH].word) == 0) { // if the word does already exist in the histogram...
                isThere = 1; // set value to '1' for true
                (*histogram)[currH].frequency++; // increment the frequency for the word in the histogram
            }
        }

        if (isThere == 0) { // if the word is not already in the histogram...
            toAdd.word = words[currS]; // set the word to the word
            toAdd.frequency = 1; // set the frequency to one
            (*histogram)[*histoSize] = toAdd; // add to histogram
            (*histoSize)++; // increment size of histogram
        }
    }

    return histoSize; // return size of histogram
}


// displaywords
// prints out all words in array
// returns void
void displayHistogram(Histogram *histogram, int *histoSize) {
    for (int curr = 0; curr < *histoSize; curr++) { // for each freq...
        printf("word %s: freq %d\n", histogram[curr].word, histogram[curr].frequency); // print out words and frequencies in the histogram
    }
}

// sortHistogram
// sorts histogram fom largest to smallest frequencies
void sortHistogram(Histogram *histogram, int *histoSize) {
 
    // Bubble sort algorithm to sort histogram
    for (int curr = 0; curr < *histoSize - 1; curr++) { // for each freq...
        int maxIndex = curr; // assume current is largest
        for (int check = curr; check < *histoSize; check++) { // for each freq...
            if (histogram[check].frequency > histogram[maxIndex].frequency) { // if the frequency being checked is larger than largest...
                Histogram temp = histogram[curr]; // create temp to hold current value
                histogram[curr] = histogram[check]; // value being checked becomes current value
                histogram[check] = temp; // current value becomes the largest
            }
        }
    }
}

// main function
int main() {
    int *wordsSize = (int*)malloc(sizeof(int)); // allocate memory for wordsSize
    *wordsSize = 0; // initialize wordsSize to 0
    char **words = readwords(wordsSize); // call readwords and pass in array and word of words in array)
    int *histoSize = (int*)malloc(sizeof(int)); // allocate memory for histoSize
    *histoSize = 0; // initialize histoSize to 0
    Histogram *histogram = NULL;

    calcHistogram(words, wordsSize, &histogram, histoSize); // Calculate histogram
    printf("Display Words:\n");
    displaywords(words, wordsSize); // call displaywords to print out array of words
    printf("\n");
    printf("Display Histogram:\n");
    displayHistogram(histogram, histoSize); // Display histogram
    sortHistogram(histogram, histoSize); // Sort histogram
    printf("\n");
    printf("Display Sorted Histogram:\n");
    displayHistogram(histogram, histoSize); // Display histogram

    // free memory for each word in array of words
    for (int i = 0; i < *wordsSize; i++) {
        free(words[i]); // free memory allocated for word
    }
    free(words); // free memory allocated for words
    free(histogram); // free memory allocated for histogram
    free(wordsSize); // free memory allocated for wordsSize
    free(histoSize); // free memory allocated for histoSize

    return 0;
}
