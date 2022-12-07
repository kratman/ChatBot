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
        self.maxWords = 40

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

    def readPreProgrammed(self, fileName, errorMessage):
        try:
            # Open file
            memFile = open(self.GabbiePath + fileName, "r")
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
            if self.debugGabbie:
                self.debugLine += "  " + errorMessage
                self.debugLine += '\n'

    def readPersonality(self):
        self.readPreProgrammed("/Canned/Personality.txt", "Exception: No personality memories were located.")

    def readGreetings(self):
        self.readPreProgrammed("/Canned/Greetings.txt", "Exception: No greeting memories were located.")

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
            for trioList in memFile:
                # Read trio list
                tempData = trioList.strip().split()
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
        # Continue the sentence
        if pair in self.wordPairs:
            # Add the next word
            binSize = self.getBinSize(self.wordPairs, pair)
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
        noEnd, text = self.checkEndOfSentence(pair, text, ct)
        # Return the update conversation
        return noEnd, text, pair, ct

    def markovTrios(self, text, trio, ct):
        # Continue the sentence
        if trio in self.wordTrios:
            # Add the next word
            binSize = self.getBinSize(self.wordTrios, trio)
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
        noEnd, text = self.checkEndOfSentence(trio, text, ct)
        # Return the update conversation
        return noEnd, text, trio, ct

    @staticmethod
    def getBinSize(wordList, phrase):
        if len(wordList[phrase]) > 1:
            binSize = 1.0 / (len(wordList[phrase]) - 1)
        else:
            binSize = 1.0 / len(wordList[phrase])
        return binSize

    def checkEndOfSentence(self, phrase, output, ct):
        lastCharacter = phrase[-1]
        noEnd = True
        if lastCharacter not in ["!", ".", "?"]:
            noEnd = False
        # Avoid infinite conversations
        if ct > self.maxWords:
            # Stop the sentence
            noEnd = False
            # Add a period to improve the formatting
            output += "."
        return noEnd, output

    def getRandomWord(self):
        return random.choice(list(self.wordPairs.keys()))
