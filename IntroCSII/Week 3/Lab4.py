'''
--------------------------------------------------
nltk1.py    Created 24.01.26, revised 24.01.28
Authors:  Scott T. Leutenegger, Andrew Hannum

Purposes:    
1) To begin exploring NLP text analysis using the NLTK library:
- nltk.word_tokenize(str) - returns a list of words
- nltk.sent_tokenize(str) - returns a list of sentences
- ntlk.FreqDist(list of elements) - elements could be chars, words, bigrams, 
- nltk.FreqDist.most_common(N) - returns the N most frequent elements along with frequency count
- ntlk.ngrams(N) - create a list of ngrams:  2-bigrams; 3-trigrams

- Calculate simple text analyis statistics:  average words per sentence, average chars per word
- Understand "stopwords" and how to remove them (do not always want to remove)
- Understand punctuation and how to remove them (do not always want to remove)
- Understand and use bigrams

2) To continue to improve code-reading skills

Lab Instructions:

This lab has 8 parts - there is nothing to turn in for part 1, but don't skip it!  Spend time making sure you understand the code!  For steps 2..8
write down your answer in a document.  The document will presumably be mostly English, but you should be putting in a bit of code too for steps 3, 5, and 8.
Upload a .pdf file of your document (everyone upload, it can be the same docuemnt for everyone in your group)

1) Read through and run the code understanding each section.  As a group - read through and ask each other questions about 
   anything you do not understand.

2) For the code as written, what insight does the bigram/trigram output at the end provide?  (Answer in prose)

3) The code below just gives quantiative numbers for text1 and text2.  Often it helps to augment these numbers with a ratio of text1/text2 (or expressed
   as a precentage, e.g. "text2 has 15% more..." ).  Write code to give ratios or percentages for text1 vs text2 based on words per sentence and characters
   per word.  (Your answer should included relevant code snippets and prose that includes your numeric results)

4) When counting words per sentence, should punctuation and stopwords be included?  Write code to explore the effect on relative comparison and
   present your results. For example, "before removing punct/stop text1 and text2 had N1,N2 words per sentence, after removing punct/stop they had N1b,N2b".
   (Your answer should be just the prose and numbers, no code snippets)

5) When comparing two texts by the most frequent words used, for many novels the list of frequent words contain many character names
   so we are not really getting at the authors use of English prose.  How can you "fix this"?  Do so for the pair (Bleak House, Middlemarch) and show 
   the diffrence before and after removing common character names.  Specify how you found (presumably by visual inspection) and removed character names. 
   (Your answer should include prose and relevant code snippets)

6) The code as written compares the texts "Bleak House" and "Middlemarch".  What happens if you keep Bleak House but change Middlemarch to Ezra Pound Poetry 
   or Milton's Paradise lost?  (Your answer should be prose, no code snippets)

7) In general, comparing different works can result in all this being useful or not so useful.  Explore different pairings of the texts above (you
   will need to un-comment the request staements) for certain metrics.  
   Which texts are similar?  Why do you say that?  Which are dissimilar?  Why do you say that?  Do this for at least 4 different pairings of books.
   (Your answer should be prose that includes numbers and short outputs/lists-of-words, no code snippets)

8) How "big is the vocabulary" in the two books?  How do you measure and calculate?  Write the code, run a comparative study for your 
   two books, and present your results.  (Your answer should be prose and code snippets)


--------------------------------------------------
'''

import sys
import subprocess
subprocess.check_call([sys.executable, "-m", "pip", "install", "nltk"])

import nltk
import requests
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

print("\n\nStarting...")

# uncomment the ones you want to use, uncommenting all of the folowing lines will slow down the execution of your code.  Why?
# r1 = requests.get('https://www.gutenberg.org/cache/epub/98/pg98.txt')  # Dickens : A Tale of Two Cities
# r2 = requests.get('https://www.gutenberg.org/cache/epub/1023/pg1023.txt') # Dickens: Bleak House
# r3 = requests.get('https://www.gutenberg.org/cache/epub/619/pg619.txt')  # A. Trollope:  The Warden
# r4 = requests.get('https://www.gutenberg.org/cache/epub/107/pg107.txt')  # T. Hardy:  Far From the Madding Crowd
# r5 = requests.get('https://www.gutenberg.org/cache/epub/145/pg145.txt')  # G. Eliot:  Middlemarch
r6 = requests.get('https://www.gutenberg.org/cache/epub/36/pg36.txt') # H.G. Wells:  War of the Worlds
# r7 = requests.get('https://www.gutenberg.org/cache/epub/164/pg164.txt') # J. Verne:  Twenty Thousand Leagues Under The Sea
# r8 = requests.get('https://www.gutenberg.org/cache/epub/1513/pg1513.txt')  # Shakespeare: T2
r9 = requests.get('https://www.gutenberg.org/cache/epub/4300/pg4300.txt')  # j joyce: Ulyses
# r10 = requests.get('https://www.gutenberg.org/cache/epub/1228/pg1228.txt')  # darwin:  on the origin of specied
# r11 = requests.get('https://www.gutenberg.org/cache/epub/51992/pg51992.txt') # Ezra Pound: poetry collection
# r12 = requests.get('https://www.gutenberg.org/cache/epub/26/pg26.txt')  # J. Milton: Paradise Lost

# set req1 and req2 to be what you want.  If you do not change the default is "T1" and "T2"
# req2 = rb2   # reset "T2" to "on the origin of species"

req1 = r6      # Dickens - Bleak House
req2 = r9      # Eliot - Middlemarch


#############
# Section 1:   word and sentence tokenization
#############

print("\n\n--------- Section 1 ---------\n\n")

# structure as a string holding all the text
theTextT1 = str( req1.text )
print("Length of T1 in chars: " + str( len(theTextT1)))
print("Printing chars 4500..4600")
print( theTextT1[4500:4600]) 

# structure as words using word_tokenize
theTokensT1 = nltk.word_tokenize(theTextT1)
print("\nLength of T1 in words/tokens: " + str( len(theTokensT1)))
print("Printing theTokensT1[1000:1050]")
print(theTokensT1[1000:1050])

# structure as sentences using sent_tokenize
theSentencesT1 = nltk.sent_tokenize(theTextT1)
print("\nLength of T1 in sentences: " + str( len(theSentencesT1)))
print("\nPrinting the 6 sentences starting 1/3 of the way through:")
numberSentences = len(theSentencesT1)
for i in range( int( numberSentences/3) - 3,  int( numberSentences / 3) + 3):
    print(str(i) + " " + theSentencesT1[i])



# Lets do the same three things for T2
# structure as a string holding all the text
theTextT2 = str( req2.text )
print( "\nLength of T2 in chars: " + str( len(theTextT2)))
print("Printing chars 4500..5000")
print( theTextT2[4500:5000]) 

# structure as words using word_tokenize
theTokensT2 = nltk.word_tokenize(theTextT2)
print("Length of T2 in words/tokens: " + str( len(theTokensT2)))
print("Printing theTokensT2[1000:1050]")
print(theTokensT2[1000:1050])

# structure as sentences using sent_tokenize
theSentencesT2 = nltk.sent_tokenize(theTextT2)
print("\nLength of T2 in sentences: " + str( len(theSentencesT2)))
print("\nPrinting the middle 6 sentences")
numberSentences = len(theSentencesT2)
for i in range( int( numberSentences/2) - 3,  int( numberSentences / 2) + 3):
    print(str(i) + " " + theSentencesT2[i])


#############
# Section 2:  calculating simple statistics
#############

print("\n\n--------- Section 2 ---------\n\n")

# Lets calculate statistics to compare these two texts
# Since there are differing amounts of "white space" in the two texts, lets use the tokens instead of chars

def averageWordLength(tokens):
    numChars = 0
    for w in tokens:
        numChars += len(w)
    return numChars / len(tokens)

# average word length:
avgCharsPerWordT1 = averageWordLength(theTokensT1)
avgCharsPerWordT2 = averageWordLength(theTokensT2)

print("Average number chars per word T1 = " + str(avgCharsPerWordT1))
print("Average number chars per word T2 = " + str(avgCharsPerWordT2))

def averageSentenceLength(sentences):
    numWords = 0
    for s in sentences:
        numWords += len( nltk.word_tokenize(s) )
    return numWords / len(sentences)

# average words per sentence:
avgWordsPerSentenceT1 = averageSentenceLength(theSentencesT1)
avgWordsPerSentenceT2 = averageSentenceLength(theSentencesT2)

print("Average number words per sentence T1 = " + str(avgWordsPerSentenceT1))
print("Average number words per sentence T2 = " + str(avgWordsPerSentenceT2))


#############
# Section 3 - frequency of words
#############

print("\n\n--------- Section 3 ---------\n\n")


# Lets see what are the most frequent words
wordFreqDist = nltk.FreqDist(theTokensT1)    # create an nltk.FreqDist which just counts frequency
print("Most frequent words in T1")
print(wordFreqDist)
print(wordFreqDist.most_common(20))
frequentWordsT1 = wordFreqDist.most_common(15)

wordFreqDist = nltk.FreqDist(theTokensT2)
print("\nMost frequent words in T1")
print(wordFreqDist)
print(wordFreqDist.most_common(20))
frequentWordsT2 = wordFreqDist.most_common(15)

print("\nJust the words without counts:")
for element in frequentWordsT1:
    print( element[0] + " " , end = "")     # strip of the counts only printing the first part of each freqDist element
print("\n")
for element in frequentWordsT2:
    print( element[0] + " " , end = "")
print("\n")



#############
# Section 4 - stopword removal
#############

print("\n\n--------- Section 4 ---------\n\n")

# That did not tell us much because the most common words were not "interesting" and hence both have similar common words
# There is the concept of "stop words", common words to all writing, that we can remove to better reveal differences

# lets remove stop words
from nltk.corpus import stopwords
english_stop_words = set(stopwords.words('english'))   #nltk provides stop words for several languages
noStopTokensT1 = [word for word in theTokensT1 if word.lower() not in english_stop_words]
noStopTokensT2 = [word for word in theTokensT2 if word.lower() not in english_stop_words]

wordFreqDist = nltk.FreqDist(noStopTokensT1)
print("Most frequent words in T1")
print(wordFreqDist)
print(wordFreqDist.most_common(20))
frequentWordsT1 = wordFreqDist.most_common(15)

wordFreqDist = nltk.FreqDist(noStopTokensT2)
print("\nMost frequent words in T2")
print(wordFreqDist)
print(wordFreqDist.most_common(20))
frequentWordsT2 = wordFreqDist.most_common(15)

print("\nJust the words without counts:")
for element in frequentWordsT1:
    print( element[0] + " " , end = "")
print("\n")
for element in frequentWordsT2:
    print( element[0] + " " , end = "")
print("\n")






#############
# Section 5 - punctuation removal
#############

print("\n\n--------- Section 5 ---------\n\n")

# Okay - in the above we seeing a difference in word usage, but punctuation is dominating. So, lets remove punctuation also...

noStopPunctT1 = [word for word in noStopTokensT1 if word.isalnum()]
noStopPunctT2 = [word for word in noStopTokensT2 if word.isalnum()]

wordFreqDist = nltk.FreqDist(noStopPunctT1)
print("Most frequent words in T1")
print(wordFreqDist)
print(wordFreqDist.most_common(25))
frequentWordsT1 = wordFreqDist.most_common(25)

wordFreqDist = nltk.FreqDist(noStopPunctT2)
print("\nMost frequent words in T2")
print(wordFreqDist)
print(wordFreqDist.most_common(25))
frequentWordsT2 = wordFreqDist.most_common(25)

print("\nJust the words without counts:")
print("\nFor text1:")
for element in frequentWordsT1:
    print( element[0] + " " , end = "")

print("\nFor text2:")
for element in frequentWordsT2:
    print( element[0] + " " , end = "")
print("\n")



#############
# Section 6 - recalculate average word length with stopwords and punctuation removed
#############

print("\n\n--------- Section 6 ---------\n\n")

# which versions of {full words, no punctation, no stopwords, neither punctuation nor stopwords} should
# we use when calculating statistics?
# When we printed out average number of chars per word both lists included stop words and punctuation, does that effect the relative comparison?
# Lets "fix this", i.e. get the number without the stopwords and punctuation

avgCharsPerWordT1 = averageWordLength(noStopPunctT1)
avgCharsPerWordT2 = averageWordLength(noStopPunctT2)

print("Average number chars per word stop words removed T1 = " + str(avgCharsPerWordT1))
print("Average number chars per word stop words removed T2 = " + str(avgCharsPerWordT2))



#############
# Section 7: ngrams
#############

print("\n\n--------- Section 7 ---------\n\n")

# Another way to see differences in writing style is to look at frequent bigrams.  Bigrams are subseuent word pairs.
# For example, if the string was "The cat sat on the hat" the bigrams would be:  [(the cat), (cat sat) (sat on), (on the), (the hat)]
# Question - could you write your own code to create a list of bigrams instead of using the following ngram function?
bigramsText1 = nltk.ngrams(theTokensT1,2) 
bigramsText2 = nltk.ngrams(theTokensT2,2)
bigramFreqDist1 = nltk.FreqDist(bigramsText1)
bigramFreqDist2 = nltk.FreqDist(bigramsText2)
print("most frequent bigrams text1:")
print(bigramFreqDist1.most_common(15))
print("most frequent bigrams text2:")
print(bigramFreqDist2.most_common(15))

#okay, that punctuation is problematic, so lets remove it
bigramsText1 = nltk.ngrams(noStopPunctT1,2) 
bigramsText2 = nltk.ngrams(noStopPunctT2,2)
bigramFreqDist1 = nltk.FreqDist(bigramsText1)
bigramFreqDist2 = nltk.FreqDist(bigramsText2)
print("most frequent bigrams with stopwords and punctuation removed text1:")
print(bigramFreqDist1.most_common(15))
print("most frequent bigrams with stopwords and punctuation removed text2:")
print(bigramFreqDist2.most_common(15))

#better, but some look like they are missing (stop) words, so how about removing punct but not stopWords?
noPunctT1 =  [w for w in theTokensT1 if w.isalnum()]
noPunctT2 =  [w for w in theTokensT2 if w.isalnum()]
bigramsText1 = nltk.ngrams(noPunctT1,2) 
bigramsText2 = nltk.ngrams(noPunctT2,2)
bigramFreqDist1 = nltk.FreqDist(bigramsText1)
bigramFreqDist2 = nltk.FreqDist(bigramsText2)
print("most frequent bigrams with punctuation removed text1:")
print(bigramFreqDist1.most_common(15))
print("most frequent bigrams with punctuation removed text2:")
print(bigramFreqDist2.most_common(15))

# okay, now that is just dominated by stopwords and means almost nothing, how about trigrams?
trigramsT1 = nltk.ngrams(noPunctT1,3) 
trigramsT2 = nltk.ngrams(noPunctT2,3)
trigramFreqDist1 = nltk.FreqDist(trigramsT1)
trigramFreqDist2 = nltk.FreqDist(trigramsT2)
print("\nMost frequent trigrams with punctuation removed text1:")
print(trigramFreqDist1.most_common(25))
print("\nMost frequent trigrams with punctuation removed text2:")
print(trigramFreqDist2.most_common(25))

#print ratio for words per sentence
if (avgWordsPerSentenceT1 > avgWordsPerSentenceT2):
    wordsPerSentencePercentage = ((avgWordsPerSentenceT1 - avgWordsPerSentenceT2)/avgWordsPerSentenceT1) * 100
    print("text1 has ", round(wordsPerSentencePercentage), "% more average words per sentence.")
else:
    wordsPerSentencePercentage = ((avgWordsPerSentenceT2 - avgWordsPerSentenceT1)/avgWordsPerSentenceT2) * 100
    print("text2 has ", round(wordsPerSentencePercentage), "% more average words per sentence.")

    
#print ratio for characters per word
if (avgCharsPerWordT1 > avgCharsPerWordT2):
    charsPerWordPercentage = ((avgCharsPerWordT1 - avgCharsPerWordT2)/avgCharsPerWordT1) * 100
    print("text1 has ", round(charsPerWordPercentage), "% more average chars per word.")
else:
    charsPerWordPercentage = ((avgCharsPerWordT2 - avgCharsPerWordT1)/avgCharsPerWordT2) * 100
    print("text2 has ", round(charsPerWordPercentage), "% more average chars per word.")

#print textSentenceCount no stop/punct

def theSentenceLength(sentences):
    numWords = 0
    for s in sentences:
        numWords += len( nltk.word_tokenize(s) )
    return numWords

# average word length:
SentenceLengthT1 = theSentenceLength(theTokensT1)
SentenceLengthT2 = theSentenceLength(theTokensT2)
# average word length without stop/punct
RemovedSentenceLengthT1 = theSentenceLength(noStopPunctT1)
RemovedSentenceLengthT2 = theSentenceLength(noStopPunctT2)

print("T1 No Removed:",SentenceLengthT1)
print("T2 No Removed:",SentenceLengthT2)
print("T1 Removed:",RemovedSentenceLengthT1)
print("T2 Removed:",RemovedSentenceLengthT2)



common_names = ["Sir","Miss", "Lady", "Leicester","Summerson","Dedlock","Dorothea","Chesney","Wold","Richard",
                "Flite","Baronet","Bucket","James","Lydgate","Rosamond","Brooke","Mary","Stone","Celia","Fred",
                "Bulstrode","Caleb","Richard","Rosamund","Dorothea","Lydgate"]  
noNamesT1 = [word for word in noStopPunctT1 if word.lower() not in common_names]
noNamesT2 = [word for word in noStopPunctT2 if word.lower() not in common_names]

wordFreqDistT1 = nltk.FreqDist(noNamesT1)
wordFreqDistT2 = nltk.FreqDist(noNamesT2)


print("\nMost frequent words in T1 no names:")
print("No Names T1: ", wordFreqDistT1.most_common(25))

print("\nMost frequent words in T2 no names:")
print("No Names T2: ", wordFreqDistT2.most_common(25))





