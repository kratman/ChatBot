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
        self.acceptablePunctuation = [".", "!", "?", ",", ":", ";"]

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

    def fixPunctuation(self, text):
        lastChar = text[-1]
        if lastChar not in self.acceptablePunctuation:
            # Add a period
            text += "."
        return text

    def fixCase(self, text):
        if self.allLowerCase:
            text = text.lower()
        return text

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
        except FileNotFoundError:
            # Print an error message
            quitGabbie = True
            if self.debugGabbie:
                self.debugLine += "  Exception: No personality memories were located."
                self.debugLine += '\n'

    def readGreetings(self):
        try:
            # Open file
            memFile = open(self.GabbiePath + "/Canned/Greetings.txt", "r")
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
        except FileNotFoundError:
            # Print an error message
            self.quitGabbie = True
            if self.debugGabbie:
                self.debugLine += "  Exception: No greeting memories were located."
                self.debugLine += '\n'

    def readFrequencies(self):
        try:
            # Open file
            memFile = open(self.GabbiePath + "/Knowledge/Memories_frequency.txt", "r")
            for freq in memFile:
                # Read word frequencies
                tempData = freq.strip().split()
                tempDict = {tempData[0]: float(tempData[1])}
                self.wordFreqs.update(tempDict)
            # Close file
            memFile.close()
        except FileNotFoundError:
            # Print an error message
            self.quitGabbie = True
            if self.debugGabbie:
                self.debugLine += "  Exception: No word frequency memories were located."
                self.debugLine += '\n'

    def readPairs(self):
        try:
            # Open file
            memFile = open(self.GabbiePath + "/Knowledge/Memories_pairs.txt", "r")
            for pairlist in memFile:
                # Read pair list
                tempData = pairlist.strip().split()
                tempPair = tempData[0] + " " + tempData[1]
                tempDict = {tempPair: tempData[2:]}
                self.wordPairs.update(tempDict)
            # Close file
            memFile.close()
        except FileNotFoundError:
            # Print an error message
            self.quitGabbie = True
            if self.debugGabbie:
                self.debugLine += "  Exception: No word pair memories were located."
                self.debugLine += '\n'

    def readTrios(self):
        try:
            # Open file
            memFile = open(self.GabbiePath + "/Knowledge/Memories_trios.txt", "r")
            for triolist in memFile:
                # Read trio list
                tempData = triolist.strip().split()
                tempTrio = tempData[0] + " " + tempData[1] + " " + tempData[2]
                tempDict = {tempTrio: tempData[3:]}
                self.wordTrios.update(tempDict)
            # Close file
            memFile.close()
        except FileNotFoundError:
            # Print an error message
            if self.debugGabbie:
                self.debugLine += "  Exception: No word trio memories were located."
                self.debugLine += '\n'

    def knownPhrases(self, userInput):
        # Initialize variables
        answer = userInput  # Needed when no input is given
        notFound = True  # Forces Gabbie to keep talking
        # Check if Gabbie recognizes the user input
        if userInput in self.canPhrases:
            # Stop the conversation
            notFound = False
            # Save Gabbie's answer
            answer = self.canPhrases[userInput]
        return notFound, answer

    def markovPairs(self, text, pair, ct):
        # Defined constraints
        maxWords = 40
        # Continue the sentence
        if pair in self.wordPairs:
            # Add the next word
            if len(self.wordPairs[pair]) > 1:
                binSize = 1.0 / (len(self.wordPairs[pair]) - 1)
            else:
                binSize = 1.0 / len(self.wordPairs[pair])
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
                    wordID = wordID % len(self.wordPairs[pair])
                nextWord = self.wordPairs[pair][wordID]
            text += " " + nextWord
            pair = pair.split()[1] + " " + nextWord
            ct += 1
        else:
            # Choose randomly
            pair = random.choice(list(self.wordPairs.keys()))
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

    def markovTrios(self, text, trio, ct):
        # Defined constraints
        maxWords = 40
        # Continue the sentence
        if trio in self.wordTrios:
            # Add the next word
            if len(self.wordTrios[trio]) > 1:
                binSize = 1.0 / (len(self.wordTrios[trio]) - 1)
            else:
                binSize = 1.0 / len(self.wordTrios[trio])
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
                    wordID = wordID % len(self.wordTrios[trio])
                nextWord = self.wordTrios[trio][wordID]
            text += " " + nextWord
            trio = trio.split()[1] + trio.split()[2] + " " + nextWord
            ct += 1
        else:
            # Choose randomly
            trio = random.choice(list(self.wordTrios.keys()))
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

    def getRandomWord(self):
        return random.choice(list(self.wordPairs.keys()))
