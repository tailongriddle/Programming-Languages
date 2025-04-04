#include <stdio.h>

// structFrec
// structure for frequencies
// tracks number and its frequency
struct freq{
    int number;
    int frequency;
}; //structures end with semicolons

// readScores
// adds to array of scores from file input
// returns void
void readScores(int scores[], int *scoresSize){
    while (scanf("%d", &scores[*scoresSize]) != EOF){  //while not at the end of the file...
    (*scoresSize)++; //add to array^ and increment size of numbers entered into array
    }
}

// displayScores
// prints out all scores in array
// returns void
void displayScores(int scores[], int *scoresSize){// no reason to pass as pointer if not modified

    for (int curr = 0; curr < *scoresSize; curr++){ // for each score...
        printf("score %d: %d\n", curr, scores[curr]); // print out the score at i in scores
        
    }
}

// calcHistogram
// adds to array of scores from file input
// returns void
void calcHistogram(struct freq histogram[], int *histoSize, int scores[], int *scoresSize){
    struct freq toAdd; // create frequency to be added
    int isThere = 0; // initialize true/false value for whether or not the number already exists in the histogram

    for (int currS = 0; currS < *scoresSize; currS++){ // for each score...
       isThere = 0; //reset isThere to 0
        for (int currH = 0; currH < *histoSize; currH++){ // for each value in the histogram...
            if (scores[currS] == histogram[currH].number){ // if the score does already exist in the histogram...
                isThere = 1; // set value to '1' for true
                (histogram[currH].frequency)++; // increment the frequency for the number in the histogram
            }
    }

    if (isThere == 0){ // if the score is not already in the histogram...
    toAdd.number = scores[currS]; // set the number to the score
    toAdd.frequency = 1; // set the frequency to one
    histogram[*histoSize] = toAdd; // add to histogram
    (*histoSize)++; // increment size of histogram

    }
    
    }
}

// displayScores
// prints out all scores in array
// returns void
void displayHistogram(struct freq histogram[], int *histoSize){

    for (int curr = 0; curr < *histoSize; curr++){ // for each freq...
        printf("value %d: freq %d\n", histogram[curr].number, histogram[curr].frequency); // print out scores and frequencies in the histogram
        
    }
}

// sortHistogram
// sorts histogram fom largest to smallest frequencies
void sortHistogram(struct freq histogram[], int *histoSize){

    for (int curr = 0; curr < *histoSize - 1; curr++){ // for each freq...
        int maxIndex = curr; // assume current is largest

        for (int check = curr; check < *histoSize; check++){ // for each freq...
            if (histogram[check].frequency > histogram[maxIndex].frequency){ // if the frequency being checked is larger than largest...
                struct freq temp = histogram[curr]; // create temp to hold current value
                histogram[check] = histogram[maxIndex]; // value being checked becomes current value
                histogram[maxIndex] = temp; // current value becomes the largest
            }
    }
    }
}


// main function
int main(){
    int scores[100] = {0}; // array of scores
    int scoresSize = 0; // amount of scores in score array
    struct freq histogram[100] = {0}; // array of frequencies
    int histoSize = 0; // amount of freqs in histogram array
    
    
    readScores(scores, &scoresSize); // call readScores and pass in array and number of scores in array
    displayScores(scores, &scoresSize); // call displayScores to print out array of scores
    calcHistogram(histogram, &histoSize, scores, &scoresSize); // create histogram using array of scores
    displayHistogram(histogram, &histoSize); //display histogram
    sortHistogram(histogram, &histoSize); // sort histogram
    displayHistogram(histogram, &histoSize); //display sorted histogram

}

