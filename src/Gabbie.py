##############################################################################
#                                                                            #
#                        GabbieBot: A simple chat bot                        #
#                              By Eric G. Kratz                              #
#                                                                            #
##############################################################################

# Gabbie bot class

import random

class GabbieBot:
    def __init__(self):
        # Fraction of the updates which use the three word Markov chains
        self.threeWordFrac = 0.25  # Suggestion: 0.25
        self.GabbiePath = "./"

        # Make all letters lower case to improve the number of matches
        self.allLowerCase = True  # Suggestion: True

        # Turn on printing of the user input
        self.printUser = True  # For the text interface

        # Turn on command line debugging output
        self.debugGabbie = False

        # Initialize variables
        self.debugLine = ""  # A set of debug messages
        self.quitGabbie = False  # Quits gabbie if an error was found
        self.canPhrases = {}  # A list of canned responses
        self.wordFreqs = {}  # A word list and the frequency of appearance
        self.wordPairs = {}  # A list of all pairs of words to predict the next word
        self.wordTrios = {}  # A list of all trios of words to predict the next word

    def readPersonality(self):
        try:
            # Open file
            memFile = open(self.GabbiePath + "/Canned/Personality.txt", "r")
            memData = memFile.readlines()
            # Read pairs of phrases and responses
            for i in range(len(memData) // 2):
                # Create a temporary string for storage
                dummyLine = ""
                # Read phrase
                phrase = memData[2 * i]
                phrase = phrase.strip().split()
                phrase = phrase[1:]
                for j in range(len(phrase)):
                    if j > 0:
                        dummyLine += " "
                    dummyLine += phrase[j]
                phrase = dummyLine
                # Reset temporary string
                dummyLine = ""
                # Read response
                result = memData[2 * i + 1]
                result = result.strip().split()
                result = result[1:]
                for j in range(len(result)):
                    if j > 0:
                        dummyLine += " "
                    dummyLine += result[j]
                result = dummyLine
                # Change case
                if self.allLowerCase:
                    phrase = phrase.lower()
                    result = result.lower()
                # Save pair
                self.canPhrases.update({phrase: result})
            # Close file
            memFile.close()
        except:
            # Print an error message
            quitGabbie = True
            if self.debugGabbie:
                self.debugLine += "  Exception: No personality memories were located."
                self.debugLine += '\n'

# Read canned greetings
try:
    # Open file
    memFile = open(GabbiePath + "/Canned/Greetings.txt", "r")
    memData = memFile.readlines()
    # Read pairs of phrases and responses
    for i in range(len(memData) // 2):
        # Create a temporary string for storage
        dummyLine = ""
        # Read phrase
        phrase = memData[2 * i]
        phrase = phrase.strip().split()
        phrase = phrase[1:]
        for j in range(len(phrase)):
            if j > 0:
                dummyLine += " "
            dummyLine += phrase[j]
        phrase = dummyLine
        # Reset temporary string
        dummyLine = ""
        # Read response
        result = memData[2 * i + 1]
        result = result.strip().split()
        result = result[1:]
        for j in range(len(result)):
            if j > 0:
                dummyLine += " "
            dummyLine += result[j]
        result = dummyLine
        # Change case
        if allLowerCase:
            phrase = phrase.lower()
            result = result.lower()
        # Save pair
        canPhrases.update({phrase: result})
    # Close file
    memFile.close()
except:
    # Print an error message
    quitGabbie = True
    if debugGabbie:
        debugLine += "  Exception: No greeting memories were located."
        debugLine += '\n'

# Read word frequencies
try:
    # Open file
    memFile = open(GabbiePath + "/Knowledge/Memories_frequency.txt", "r")
    for freq in memFile:
        # Read word frequencies
        tempData = freq.strip().split()
        tempDict = {tempData[0]: float(tempData[1])}
        wordFreqs.update(tempDict)
    # Close file
    memFile.close()
except:
    # Print an error message
    quitGabbie = True
    if (debugGabbie):
        debugLine += "  Exception: No word frequency memories were located."
        debugLine += '\n'

# Read word pairs
try:
    # Open file
    memFile = open(GabbiePath + "/Knowledge/Memories_pairs.txt", "r")
    for pairlist in memFile:
        # Read pair list
        tempData = pairlist.strip().split()
        tempPair = tempData[0] + " " + tempData[1]
        tempDict = {tempPair: tempData[2:]}
        wordPairs.update(tempDict)
    # Close file
    memFile.close()
except:
    # Print an error message
    quitGabbie = True
    if debugGabbie:
        debugLine += "  Exception: No word pair memories were located."
        debugLine += '\n'

# Read word trios
try:
    # Open file
    memFile = open(GabbiePath + "/Knowledge/Memories_trios.txt", "r")
    for triolist in memFile:
        # Read trio list
        tempData = triolist.strip().split()
        tempTrio = tempData[0] + " " + tempData[1] + " " + tempData[2]
        tempDict = {tempTrio: tempData[3:]}
        wordTrios.update(tempDict)
    # Close file
    memFile.close()
except:
    # Print an error message
    if debugGabbie:
        debugLine += "  Exception: No word trio memories were located."
        debugLine += '\n'


# Attempt to use known phrases
def knownPhrases(userInput):
    # Initialize variables
    answer = userInput  # Needed when no input is given
    notFound = True  # Forces Gabbie to keep talking
    # Check if Gabbie recognizes the user input
    if userInput in canPhrases:
        # Stop the conversation
        notFound = False
        # Save Gabbie's answer
        answer = canPhrases[userInput]
    return notFound, answer


# Two word Markov chain model
def ConvPairs(text, pair, ct):
    # Defined constraints
    maxWords = 40
    # Continue the sentence
    if pair in wordPairs:
        # Add the next word
        if len(wordPairs[pair]) > 1:
            binSize = 1.0 / (len(wordPairs[pair]) - 1)
        else:
            binSize = 1.0 / len(wordPairs[pair])
        wordFound = False
        wordID = 0
        # Find a word with a biased random choice
        nextWord = ""
        while not wordFound:
            if random.random() < binSize:
                # Accept this word
                wordFound = True
            else:
                # Move to the next word
                wordID += 1
                wordID = wordID % len(wordPairs[pair])
            nextWord = wordPairs[pair][wordID]
        text += " " + nextWord
        pair = pair.split()[1] + " " + nextWord
        ct += 1
    else:
        # Choose randomly
        pair = random.choice(list(wordPairs.keys()))
        text += " " + pair
        ct += 2
    # Check for punctuation
    lastCharacter = pair[-1]
    noEnd = True
    if lastCharacter == "!":
        noEnd = False
    if lastCharacter == ".":
        noEnd = False
    if lastCharacter == "?":
        noEnd = False
    # Avoid infinite conversations
    if ct > maxWords:
        # Stop the sentence
        noEnd = False
        # Add a period to improve the formatting
        text += "."
    # Return the update conversation
    return noEnd, text, pair, ct


# Three word Markov chain model
def ConvTrios(text, trio, ct):
    # Defined constraints
    maxWords = 40
    # Continue the sentence
    if trio in wordTrios:
        # Add the next word
        if len(wordTrios[trio]) > 1:
            binSize = 1.0 / (len(wordTrios[trio]) - 1)
        else:
            binSize = 1.0 / len(wordTrios[trio])
        wordFound = False
        wordID = 0
        # Find a word with a biased random choice
        nextWord = ""
        while not wordFound:
            if random.random() < binSize:
                # Accept this word
                wordFound = True
            else:
                # Move to the next word
                wordID += 1
                wordID = wordID % len(wordTrios[trio])
            nextWord = wordTrios[trio][wordID]
        text += " " + nextWord
        trio = trio.split()[1] + trio.split()[2] + " " + nextWord
        ct += 1
    else:
        # Choose randomly
        trio = random.choice(list(wordTrios.keys()))
        text += " " + trio
        ct += 3
    # Check for punctuation
    lastCharacter = trio[-1]
    noEnd = True
    if lastCharacter == "!":
        noEnd = False
    if lastCharacter == ".":
        noEnd = False
    if lastCharacter == "?":
        noEnd = False
    # Avoid infinite conversations
    if ct > maxWords:
        # Stop the sentence
        noEnd = False
        # Add a period to improve the formatting
        text += "."
    # Return the update conversation
    return noEnd, text, trio, ct