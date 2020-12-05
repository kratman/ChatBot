##############################################################################
#                                                                            #
#                        GabbieBot: A simple chat bot                        #
#                              By Eric G. Kratz                              #
#                                                                            #
##############################################################################

# Primary GabbieBot program

import sys
import random

# Fraction of the updates which use the three word Markov chains
threeWordFrac = 0.25  # Suggestion: 0.25
GabbiePath = "./"

# Make all letters lower case to improve the number of matches
allLowerCase = True  # Suggestion: True

# Turn on printing of the user input
printUser = True  # For the text interface

# Turn on command line debugging output
debugGabbie = False

# Initialize variables
debugLine = ""  # A set of debug messages
quitGabbie = False  # Quits gabbie if an error was found
canPhrases = {}  # A list of canned responses
wordFreqs = {}  # A word list and the frequency of appearance
wordPairs = {}  # A list of all pairs of words to predict the next word
wordTrios = {}  # A list of all trios of words to predict the next word

# Read personality
try:
    # Open file
    memFile = open(GabbiePath + "/Canned/Personality.txt", "r")
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
        debugLine += "  Exception: No personality memories were located."
        debugLine += '\n'

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


# Main routines

# Print a blank line for formatting
print("")

# Save user's input
try:
    # Save the user input
    sentence = ""
    sentence += sys.argv[1]
    # Check punctuation
    lastChar = sentence[-1]
    if (lastChar != ".") and (lastChar != "!") and (lastChar != "?"):
        # Add a period
        sentence = sentence + "."
    # Improve formatting
    if sentence[0] != " ":
        sentence = " " + sentence
    # Change the case
    if allLowerCase:
        sentence = sentence.lower()
    # Identify the user
    sentence = " User:" + sentence
    # Print the user input
    sentence += '\n'
    if printUser:
        print(sentence)
    # Reset the sentence for Gabbie
    sentence = ""
except:
    # Ignore the error and do nothing
    if debugGabbie:
        debugLine += "  Exception: No user input given."
        debugLine += '\n'

# Process the user's statement
try:
    # Copy the user input
    sentence = ""
    sentence += sys.argv[1]
    # Check punctuation
    lastChar = sentence[-1]
    if (lastChar != ".") and (lastChar != "!") and (lastChar != "?"):
        # Add a period
        sentence = sentence + "."
    # Change the case
    if allLowerCase:
        sentence = sentence.lower()
    try:
        # Save the last three words as input for Gabbie
        prevPair = None
        prevTrio = sentence.strip().split()
        prevTrio = prevTrio[-3] + " " + prevTrio[-2] + " " + prevTrio[-1]
    except:
        # Save the last two words as input for Gabbie
        if debugGabbie:
            debugLine += "  Exception: User input was less than three words."
            debugLine += '\n'
        prevTrio = None
        prevPair = sentence.strip().split()
        prevPair = prevPair[-2] + " " + prevPair[-1]
    # Reset the sentence for Gabbie
    sentence = ""
except:
    # Randomly pick the first statement
    if debugGabbie:
        debugLine += "  Exception: Could not form a word pair/trio."
        debugLine += '\n'
    prevTrio = None
    if quitGabbie:
        prevPair = ""
    else:
        prevPair = random.choice(list(wordPairs.keys()))
    sentence = prevPair

# Pre-programmed conversations
oldSent = sentence
try:
    contSen = True
    initSent = sys.argv[1]
    # Check punctuation
    lastChar = initSent[-1]
    if (lastChar != ".") and (lastChar != "!") and (lastChar != "?"):
        # Add a period
        initSent = initSent + "."
    # Change case
    if allLowerCase:
        initSent = initSent.lower()
    # Check for a response
    contSen, sentence = knownPhrases(initSent)
    # Restore the previous sentence
    if contSen:
        sentence = oldSent
except:
    # Restore the previous sentence
    if debugGabbie:
        debugLine += "  Exception: User input could not be interpreted."
        debugLine += '\n'
    sentence = oldSent
    contSen = True

# Initialize variables
if quitGabbie:
    # Avoid crashes when no memory files were located
    contSen = False
wordCt = 0  # Word counter

# Generic conversations
while contSen:
    # Decide if pairs or trios of words should be used
    if (prevTrio is None) or (random.random() > threeWordFrac):
        # Use the the two word Markov chain
        contSen, sentence, prevPair, wordCt = ConvPairs(sentence, prevPair, wordCt)
        # Update previous trio
        prevTrio = sentence.strip().split()
        if len(prevTrio) > 2:
            # A valid trio exists
            prevTrio = prevTrio[-3] + " " + prevTrio[-2] + " " + prevTrio[-1]
        else:
            # Avoid using an invalid trio
            prevTrio = None
    else:
        # Use the three word Markov chain
        contSen, sentence, prevTrio, wordCt = ConvTrios(sentence, prevTrio, wordCt)
        # Update previous pair
        prevPair = sentence.strip().split()
        prevPair = prevTrio[-2] + " " + prevTrio[-1]

# Print an extra blank line to format the command line output
sentence += '\n'

# Remove random capitalization
sentence = sentence.lower()

# Smoothly transition between user input and Gabbie output
if sentence[0] != " ":
    sentence = " " + sentence

# Add Gabbie's identity
sentence = " Gabbie:" + sentence

# Print the result
print(sentence)

# Print debug information
if debugGabbie:
    if debugLine != "":
        debugLine = "Debugging output:\n" + debugLine
        print(debugLine)

# Quit
exit(0)
