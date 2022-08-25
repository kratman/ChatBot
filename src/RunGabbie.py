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
try:
    # Save the user input
    sentence = ""
    sentence += sys.argv[1]
    sentence = gabbie.fixPunctuation(sentence)
    # Improve formatting
    if sentence[0] != " ":
        sentence = " " + sentence
    sentence = gabbie.fixCase(sentence)
    # Identify the user
    sentence = " User:" + sentence
    # Print the user input
    sentence += '\n'
    if gabbie.printUser:
        print(sentence)
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
    sentence = ""
    sentence += sys.argv[1]
    sentence = gabbie.fixPunctuation(sentence)
    sentence = gabbie.fixCase(sentence)
    try:
        # Save the last three words as input for Gabbie
        prevPair = None
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
try:
    initSent = sys.argv[1]
    initSent = gabbie.fixPunctuation(initSent)
    initSent = gabbie.fixCase(initSent)
    # Check for a response
    contSen, sentence = gabbie.knownPhrases(initSent)
    # Restore the previous sentence
    if contSen:
        sentence = oldSent
except IndexError:
    # Restore the previous sentence
    if gabbie.debugGabbie:
        gabbie.debugLine += "  Exception: User input could not be interpreted."
        gabbie.debugLine += '\n'
    sentence = oldSent
    contSen = True

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
if gabbie.debugGabbie:
    if gabbie.debugLine != "":
        debugLine = "Debugging output:\n" + gabbie.debugLine
        print(debugLine)

# Quit
exit(0)
