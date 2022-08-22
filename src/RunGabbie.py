##############################################################################
#                                                                            #
#                        GabbieBot: A simple chat bot                        #
#                              By Eric G. Kratz                              #
#                                                                            #
##############################################################################

# Primary GabbieBot program

import sys
import random
from Gabbie import GabbieBot

# Main routines
gabbie = GabbieBot()

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
        prevPair = prevPair[-2] + " " + prevPair[-1]

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
