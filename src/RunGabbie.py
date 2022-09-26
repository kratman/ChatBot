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

# Initialize Gabbie
gabbie = GabbieBot()

# Read trained memories
gabbie.readPersonality()
gabbie.readGreetings()
gabbie.readFrequencies()
gabbie.readPairs()
gabbie.readTrios()

# Print a blank line for formatting
print("")

# Save user's input
userInput = ""
try:
    # Save the user input
    sentence = ""
    sentence += sys.argv[1]
    sentence = gabbie.fixPunctuation(sentence)
    sentence = gabbie.fixCase(sentence)
    userInput = sentence
    # Improve formatting
    if sentence[0] != " ":
        sentence = " " + sentence
    if gabbie.printUser:
        print(" User:" + sentence + '\n')
    # Reset the sentence for Gabbie
    sentence = ""
except IndexError:
    # Ignore the error and do nothing
    if gabbie.debugGabbie:
        gabbie.debugLine += "  Exception: No user input given."
        gabbie.debugLine += '\n'

# Process the user's statement
try:
    # Copy the user input
    sentence = userInput
    try:
        # Save the last three words as input for Gabbie
        prevTrio = sentence.strip().split()
        prevTrio = prevTrio[-3] + " " + prevTrio[-2] + " " + prevTrio[-1]
    except IndexError:
        # Save the last two words as input for Gabbie
        if gabbie.debugGabbie:
            gabbie.debugLine += "  Exception: User input was less than three words."
            gabbie.debugLine += '\n'
        prevTrio = None
    prevPair = sentence.strip().split()
    prevPair = prevPair[-2] + " " + prevPair[-1]
    # Reset the sentence for Gabbie
    sentence = ""
except IndexError:
    # Randomly pick the first statement
    if gabbie.debugGabbie:
        gabbie.debugLine += "  Exception: Could not form a word pair/trio."
        gabbie.debugLine += '\n'
    prevTrio = None
    if gabbie.quitGabbie:
        prevPair = ""
    else:
        prevPair = gabbie.getRandomWord()
    sentence = prevPair

# Pre-programmed conversations
oldSent = sentence
contSen, sentence = gabbie.knownPhrases(userInput)
# Restore the previous sentence
if contSen:
    sentence = oldSent

# Initialize variables
if gabbie.quitGabbie:
    # Avoid crashes when no memory files were located
    contSen = False
wordCt = 0  # Word counter

# Generic conversations
while contSen:
    # Decide if pairs or trios of words should be used
    if (prevTrio is None) or (random.random() > gabbie.threeWordFrac):
        # Use the two word Markov chain
        contSen, sentence, prevPair, wordCt = gabbie.markovPairs(sentence, prevPair, wordCt)
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
        contSen, sentence, prevTrio, wordCt = gabbie.markovTrios(sentence, prevTrio, wordCt)
        # Update previous pair
        prevPair = sentence.strip().split()
        if len(prevPair) > 2:
            prevPair = prevPair[-2] + " " + prevPair[-1]
        else:
            # Only 1 word in the sentence
            extraWord = userInput.strip().split()[-1]
            prevPair = extraWord + " " + prevPair[-1]

# Smoothly transition between user input and Gabbie output
if len(sentence) > 0 and sentence[0] != " ":
    sentence = " " + sentence

# Print the result
print(" Gabbie:" + gabbie.fixCase(sentence) + '\n')

# Print debug information
if gabbie.debugGabbie:
    if gabbie.debugLine != "":
        debugLine = "Debugging output:\n" + gabbie.debugLine
        print(debugLine)
