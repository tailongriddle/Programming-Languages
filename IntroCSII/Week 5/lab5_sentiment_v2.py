# --------------------------------------------------
# lab5_sentiment_v2.py    Created 24.01.21, revised 24.02.07
# Authors:  Scott T. Leutenegger, Andrew Hannum
#
# Purpose - to explore sentiment analysis
#
# Approaches explored in this lab:
# 1) hand coded lexicon 
# 2) Vader
# 3) NRCLex
#
# --------------------------------------------------


import sys
import subprocess
subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
subprocess.check_call([sys.executable, "-m", "pip", "install", "nltk"])
subprocess.check_call([sys.executable, "-m", "pip", "install", "nrclex"])


import nltk
import requests
import string
import matplotlib.pyplot as plt
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')
nltk.download('vader_lexicon')

print("\n\nStarting...")



########################################################
# Section 1:   hand coded lexicon
#  One needed file:   catDogLexicon.txt
# 
# To do:
#  A) Run the code and understand it
#  B) Print out the contents of  "lexicon" after it is loaded
#  C) Assume you want to promote dogs instead of cats.  Modify the catDogLexicon.txt file 
#     so that you get the opposite results (i.e. sent1 below is positive and sent2 is negative).
#     Run your code on the modified cotDogLexicon file
#
#  D) What to put into your document for section 1:
#     In prose, explain what you changed in the catDogLexicon.  Then show the first few 
#     lines of the printed out lexicon dictionary object before your change to the file and after
#     your change, and show the output (just the few lines from section 1) after the change.
########################################################


print("\n\n--------- Section 1 ---------\n\n")

# Read in a lexicon file and build the lexicon
# Note - the following code assumes a file format of rows where each row is a {word, score} pair, word & score separated by a tab
lexicon = {}
try:
    f=open("catDogLexicon.txt","r")   #assumes input file has format of [word, \t, integer, \n]

    lines = f.readlines()
    line_iter = iter(lines)
    count = 1
    for line in line_iter:
        # get the word,value pair and put in w,n
        w, n = line.split("\t")
        lexicon[w] = n    # add to dictionary
    print(lexicon)

except FileNotFoundError:
       print ("File is not found")
else:
       f.close()
print("len(lexicon) = " + str(len(lexicon)) )


# Function that takes in a sentence (string of words) and returns the sum 
# of pos/negative words for all input words that are in the lexicn
# Observation - perhpas the function return a normalized (for example dived by number of words) score?
def stringSentimentScore(inString):
    # print("Entering stringSentimentScore for: " + inString)
    total = 0
    tokens = nltk.word_tokenize(inString)
    tokens = [t for t in tokens if t.isalnum()]
    for w in tokens:
        if w in lexicon:
            total += int( lexicon[w] )
            # print( str( int(lexicon[w])  ) + ", total now = " + str(total)  + ": " + str(w))

    return(total)


# Function that takes in a string and return a list of sentiment values:
#  [numberNegativeWord, numberPostiveWord, numberNeutralWords, sum of neg+ps] 
def stringSentimentScoreMultiValueReturn(inString):
    # print("Entering stringSentimentScore for: " + inString)
    totalNeg = 0
    totalNeutral = 0 
    totalPos = 0
    tokens = nltk.word_tokenize(inString)
    tokens = [t for t in tokens if t.isalnum()]

    for w in tokens:
        if w in lexicon:
            val = int(lexicon[w])
            if (val < 0):
                totalNeg += val
            if (val > 0):
                totalPos += val
            if (val ==0):
                totalNeutral += 1
        else:
            totalNeutral +=1
    total = totalNeg + totalPos 
    returnList = [totalNeg,totalNeutral,totalPos,total]
    # print( str( int(lexicon[w])  ) + ", total now = " + str(total)  + ": " + str(w))
    return(returnList)


sent1 = "The puppy liked to bark and bark. The dog was loyal and liked its collar"
sent2 = "The kitten liked to purr and meow.  It was independent."

print(stringSentimentScore(sent1))
print(stringSentimentScoreMultiValueReturn(sent1))
print(stringSentimentScore(sent2))
print(stringSentimentScoreMultiValueReturn(sent2))



########################################################
#  Section 2 - Using Vader to explore Barbie Movie Reviews
#  Two needed files:   reviewBarbie1.txt and reviewBarbie2.txt
#  
#  To do:   
#    1) understand the code in this section
#    2) Create a list of words for reviewBarbie2 that are responsible for the review being categorized as negative.
#    3) Create a modified review, reviewBarbie3.txt, where you replace 6 to 10 words without significantly changing, you will 
#       soften the negativity some, but overall the review is still negative, yet now the review is categorized as postiive (i.e. the 
#       compound score is positive).  NOTE - initially reviewBarbie3.txt is the same as reviewBabie2.txt but you will change
#       6-10 words in reviewBarbie3.txt.   Write down the set words that 
#       you changed, for example { (painlfully -> very) and (disaster -> experience) }.  Keep track of the word pair (original,new) for your changes.
#       HINT - you will first need to write code to identify which words are causing the most negativity
#
#    4) What to put into your document for section 1:
#       a) the set of (original,new) words pairs for your changes
#       b) the snippet of code you used to identify which words you should replace
#       c) the output [numPositiveSentences, numNegativeSentences, numNeturalSentences] from running the original review and your modified review
#       d) Answer this question:   Is vader foolproof at capturing the sentiment of a document?  Why or why not?
#     
########################################################

print("\n\n--------- Section 2 ---------\n\n")



from nltk.corpus import stopwords
english_stop_words = set(stopwords.words('english'))   #nltk provides stop words for several languages
from nltk.sentiment.vader import SentimentIntensityAnalyzer
sentiment_analyzer = SentimentIntensityAnalyzer()

# open the files ar read them into variable allText1 and allText2
try:
    f=open("reviewBarbie1.txt","r")
    allText1 = f.read()
except FileNotFoundError:
       print ("File is not found")
else:
       f.close()
try:
    f=open("reviewBarbie2.txt","r")
    allText2 = f.read()
except FileNotFoundError:
       print ("File is not found")
else:
       f.close()
try:
    f=open("reviewBarbie3.txt","r")
    allText3 = f.read()
except FileNotFoundError:
       print ("File is not found")
else:
       f.close()




print("\n\nStarting analysis of reviewBarbie1.txt")
theStringBarbie1 = str(allText1)
theTokens = nltk.word_tokenize(theStringBarbie1)
theTokensBarbie1 = [t for t in theTokens if (t.isalnum())  and (t.lower() not in english_stop_words)]
textLines = nltk.sent_tokenize(theStringBarbie1)
# wordFreqDist = nltk.FreqDist(theTokens)    # create an nltk.FreqDist which just counts frequency
# print("Most frequent words:")
# print(wordFreqDist.most_common(20))
result = sentiment_analyzer.polarity_scores(theStringBarbie1)
print("Overall vader: " + str(result))      
numPostiveSentences = 0
numNegSentences = 0 
numNeutralSentencs = 0 
# loop through all the sentences and count how many sentences are neg, neutral, and pos
for l in textLines:
    result = sentiment_analyzer.polarity_scores(l)
    if (result["compound"]) > 0:
        numPostiveSentences += 1
    if (result["compound"]) < 0:
        numNegSentences += 1
    if (result["compound"]) == 0:
        numNeutralSentencs += 1    
print("NumPostiveSentences = " + str(numPostiveSentences) + ", numNegativeSentences = " + str(numNegSentences) + ", numNeutralSentences = " + str(numNeutralSentencs))


print("\n\nStarting analysis of reviewBarbie2.txt")
theStringBarbie2 = str(allText2)
theTokens = nltk.word_tokenize(theStringBarbie2)
theTokens = [t for t in theTokens if (t.isalnum())  and (t.lower() not in english_stop_words)]
textLines = nltk.sent_tokenize(theStringBarbie2)
# wordFreqDist = nltk.FreqDist(theTokens)    # create an nltk.FreqDist which just counts frequency
# print("Most frequent words:")
# print(wordFreqDist.most_common(20))
result = sentiment_analyzer.polarity_scores(theStringBarbie2)
print("Overall vader: " + str(result))      
numPostiveSentences = 0
numNegSentences = 0 
numNeutralSentencs = 0 
# loop through all the sentences and count how many sentences are neg, neutral, and pos
for l in textLines:
    result = sentiment_analyzer.polarity_scores(l)
    if (result["compound"]) > 0:
        numPostiveSentences += 1
    if (result["compound"]) < 0:
        numNegSentences += 1
    if (result["compound"]) == 0:
        numNeutralSentencs += 1    
print("NumPostiveSentences = " + str(numPostiveSentences) + ", numNegativeSentences = " + str(numNegSentences) + ", numNeutralSentences = " + str(numNeutralSentencs))




print("\n\nStarting analysis of reviewBarbie2_modified.txt")
theStringBarbie3 = str(allText3)
theTokens = nltk.word_tokenize(theStringBarbie3)
theTokens = [t for t in theTokens if (t.isalnum())  and (t.lower() not in english_stop_words)]
textLines = nltk.sent_tokenize(theStringBarbie3)
# wordFreqDist = nltk.FreqDist(theTokens)    # create an nltk.FreqDist which just counts frequency
# print("Most frequent words:")
# print(wordFreqDist.most_common(20))
result = sentiment_analyzer.polarity_scores(theStringBarbie3)
print("Overall vader: " + str(result))      
numPostiveSentences = 0
numNegSentences = 0 
numNeutralSentencs = 0 
wordsToRemove = []
# loop through all the sentences and count how many sentences are neg, neutral, and pos
for l in textLines:
    result = sentiment_analyzer.polarity_scores(l)
    if (result["compound"]) > 0:
        numPostiveSentences += 1
    if (result["compound"]) < 0:
        numNegSentences += 1
        theWords = nltk.word_tokenize(l)
        for w in theWords:
             r2 = sentiment_analyzer.polarity_scores(w)
             if r2["compound"] < 0:
                  wordsToRemove.append(w)
                  print(w, end = " ")
                  print(r2)
    if (result["compound"]) == 0:
        numNeutralSentencs += 1    
print("NumPostiveSentences = " + str(numPostiveSentences) + ", numNegativeSentences = " + str(numNegSentences) + ", numNeutralSentences = " + str(numNeutralSentencs))
print(wordsToRemove)

########################################################
# Section 3:  NRCLexicon
#
# The code below using the NRC Lexicon analysis approach to comapre the two reviews
# You can see that the emotion counts are very different.
#
# To do:
#   1) which are the two strongest emotions in review1 and review2 (do not include positive & negative):
#   2) Which words are responsible for the high "sadness" emotion in review2?
#   3) Which words are responsible for the high "joy" emotion in review1?
#
#   4) What to put in your document/report for section3:  The answers to the above three questions.
#
#
########################################################

print("\n\n--------- Section 3 ---------\n\n")


from nrclex import NRCLex
print("\nNow lets give a list of words to NRCLex")
emotion = NRCLex("A snake bite injured the happy dog")
print(emotion) 
print(emotion.words)
print(emotion.sentences)
print(emotion.affect_list)
print(emotion.affect_dict)
for key, value in emotion.affect_dict.items():
    print( str(key) + ":\t" + str(value))
print(emotion.raw_emotion_scores)
print(emotion.top_emotions)
print(emotion.affect_frequencies)

print("\nProcessing reviewBarbie1.txt with NRC")
emotion = NRCLex(theStringBarbie1)
print(emotion.top_emotions)
print(emotion.affect_frequencies)
print(emotion.raw_emotion_scores) 

for key, value in emotion.affect_dict.items():
    if 'joy' in value:
        print( str(key), "," ,end=" ")

print("\nProcessing reviewBarbie2.txt with NRC")
emotion = NRCLex(theStringBarbie2)
print(emotion.top_emotions)
print(emotion.affect_frequencies)
print(emotion.raw_emotion_scores) 
print(emotion.affect_dict)

for key, value in emotion.affect_dict.items():
    if 'sadness' in value:
        print( str(key), "," ,end=" ")


print("\nProcessing reviewBarbie3.txt with NRC")
emotion = NRCLex(theStringBarbie3)
print(emotion.top_emotions)
print(emotion.affect_frequencies)
print(emotion.raw_emotion_scores) 


