##############################################################################
#                                                                            #
#                        GabbieBot: A simple chat bot                        #
#                              By Eric G. Kratz                              #
#                                                                            #
##############################################################################

# A script for teaching GabbieBot to speak using plain text books

import os
import re
import sys

# Make all letters lower case to improve the number of matches
allLowerCase = True  # Suggestion: True
GabbiePath = "./"

# Initialize variables
totalWords = 0.0  # Total number of words in all books
numWords = 0.0  # Number of unique words in all books
bookNames = []  # List of book file names
wordFreqs = {}  # A word list and the frequency of appearance
wordPairs = {}  # A list of all pairs of words to predict the next word
wordTrios = {}  # A list of all trios of words


def SortKey(wordList):
    return wordList[1]


def removeSpecialCharacters(text):
    # Symbols to remove from the texts
    removalList = [r'\[', r'\{', r'\(', r'\<', r'\]', r'\}', r'\)', r'\>']
    newText = text  # Make a copy
    for symbol in removalList:
        newText = re.sub(symbol, "", newText)
    return newText


def sortByFrequency(wordGroups, frequencies):
    for group in wordGroups:
        tempWords = list(wordGroups[group])
        sortedWords = []
        for aWord in tempWords:
            temp = [aWord, frequencies[aWord]]
            sortedWords.append(temp)
        sortedWords = sorted(sortedWords, key=SortKey)
        tempWords = []
        for aWord in sortedWords:
            tempWords.append(aWord[0])
        tempWords.reverse()
        wordGroups[group] = tempWords
    return wordGroups


# Makes the output look a little better
print("")

# Use a count of the arguments given to python
# Note: The first argument is always the name of the script
numBooks = len(sys.argv) - 1
numErrors = 0  # Temporary storage for the number of errors
for i in range(numBooks):
    # Safely read the name of the book
    tempName = sys.argv[i + 1]
    if os.path.exists(tempName):
        # The operating system located the book
        bookNames.append(tempName)
    else:
        # The book is missing
        numErrors += 1  # Increase the number of errors
        textLine = ""  # Empty string
        # Add an error message
        textLine += "Error: A book "
        textLine += tempName
        textLine += " was not found!"
        # Print the error and continue
        print(textLine)

# Adjust the number of books by subtracting the number of errors
numBooks -= numErrors

# Convert books to dictionaries
for book in bookNames:
    # Open the book in read (r) mode
    bookFile = open(book, "r")
    # Loop over all the lines in the book
    tempList = []  # A simpler format for the word list
    for sentence in bookFile:
        # Use regular expressions to remove garbage characters
        words = removeSpecialCharacters(sentence)
        # Change the case
        if allLowerCase:
            words = words.lower()
        # Break the line into words
        words = words.strip().split()
        # Loop over all words
        for word in words:
            tempList.append(word)
            totalWords += 1.0
            # Check if the word is in the dictionary
            if word in wordFreqs:
                # Update the number of times the word appears
                wordFreqs[word] += 1.0
            else:
                # Add the word to the dictionary
                tempDict = {word: 1.0}  # Blank item for the word
                wordFreqs.update(tempDict)  # Add the new word
                # Update the statistics
                numWords += 1.0

    # Gather word pairs/trios and the next word
    bookWords = len(tempList)  # Number of words in this book
    for i in range(1, bookWords):
        # Add pairs of words
        if i < (bookWords - 2):
            # Identify a pair of words
            pair = tempList[i - 1] + " " + tempList[i]
            # Identify a word that follows the pair
            result = tempList[i + 1]
            # Change the case
            if allLowerCase:
                pair = pair.lower()
                result = result.lower()
            # Add the word pair to the dictionary
            if pair in wordPairs:
                # Make sure the word is not a repeat
                hasWord = False
                for word in wordPairs[pair]:
                    if word == result:
                        hasWord = True
                if not hasWord:
                    # Add the word to the list
                    wordPairs[pair].append(result)
            else:
                newList = [result]
                tempDict = {pair: newList}
                wordPairs.update(tempDict)
        # Add trios of words
        if (i > 1) and (i < (bookWords - 2)):
            # Identify a trio of words
            trio = tempList[i - 2] + " " + tempList[i - 1] + " " + tempList[i]
            # Identify a word that follows the trio
            result = tempList[i + 1]
            # Change the case
            if allLowerCase:
                trio = trio.lower()
                result = result.lower()
            # Add the word trio to the dictionary
            if trio in wordTrios:
                # Make sure the word is not a repeat
                hasWord = False
                for word in wordTrios[trio]:
                    if word == result:
                        hasWord = True
                if not hasWord:
                    # Add the word to the list
                    wordTrios[trio].append(result)
            else:
                newList = [result]
                tempDict = {trio: newList}
                wordTrios.update(tempDict)
    # Close the book
    bookFile.close()

# Calculate the statistical weight of the word
for word in wordFreqs:
    wordFreqs[word] /= totalWords

# Sort groups by frequency
wordPairs = sortByFrequency(wordPairs, wordFreqs)
wordTrios = sortByFrequency(wordTrios, wordFreqs)

# Save word frequency
memFile = open(GabbiePath + "/Knowledge/Memories_frequency.txt", "w")
for word in wordFreqs:
    line = ""
    line += word
    line += " "
    line += str(wordFreqs[word])
    line += '\n'
    memFile.write(line)
memFile.close()

# Save word pairs and responses
memFile = open(GabbiePath + "/Knowledge/Memories_pairs.txt", "w")
for pair in wordPairs:
    line = ""
    line += pair
    for word in wordPairs[pair]:
        line += " "
        line += word
    line += '\n'
    memFile.write(line)
memFile.close()

# Save word trios and responses
memFile = open(GabbiePath + "/Knowledge/Memories_trios.txt", "w")
for trio in wordTrios:
    line = ""
    line += trio
    for word in wordTrios[trio]:
        line += " "
        line += word
    line += '\n'
    memFile.write(line)
memFile.close()

# Create an empty line of text
textLine = ""

# Add a description
textLine += "Learning statistics:"
textLine += '\n'

# Number of books
textLine += "  Number of books: "
textLine += str(int(numBooks))
textLine += '\n'

# Number of words
textLine += "  Total number of words: "
textLine += str(int(totalWords))
textLine += '\n'
textLine += "  Number of unique words: "
textLine += str(int(numWords))
textLine += '\n'

# Print results
print(textLine)

# Clean up and exit
exit(0)
