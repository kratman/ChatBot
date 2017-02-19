##############################################################################
#                                                                            #
#                        GabbieBot: A simple chat bot                        #
#                              By Eric G. Kratz                              #
#                                                                            #
##############################################################################

#Primary GabbieBot program

### Import libraries ###

import os
import sys
import random

### Initialize variables
wordFreqs = {} #A word list and the frequency of appearance
wordPairs = {} #A list of all pairs of words to predict the next word

GabbiePath = "/home/kratz/Dropbox/Repos/ChatBot"

### Read memory files ###

#Read word frequencies
try:
  memFile = open(GabbiePath+"/Knowledge/Memories_frequency.txt","r")
  memData = memFile.readlines()
  for freq in memData:
    tempData = freq.strip().split()
    tempDict = {tempData[0] : float(tempData[1])}
    wordFreqs.update(tempDict)
  memFile.close()
  memData = [] #Clear RAM
except:
  line = ""
  line += "Error: No memories located!"
  print(line)

#Read word pairs
try:
  memFile = open(GabbiePath+"/Knowledge/Memories_pairs.txt","r")
  memData = memFile.readlines()
  for pairlist in memData:
    tempData = pairlist.strip().split()
    tempPair = tempData[0]+" "+tempData[1]
    tempDict = {tempPair : tempData[2:]}
    wordPairs.update(tempDict)
  memFile.close()
  memData = [] #Clear RAM
except:
  line = ""
  line += "Error: No memories located!"
  print(line)

### Functions ###

def ContConv(text,pair,ct):
  #Defined constraints
  maxWords = 25
  #Continue the sentence
  if (wordPairs.has_key(pair) == True):
    #Add the next word
    nextWord = random.choice(wordPairs[pair])
    text += " "+nextWord
    pair = pair.split()[1]+" "+nextWord
    ct += 1
  else:
    #Choose randomly
    pair = random.choice(wordPairs.keys())
    text += " "+pair
    ct += 2
  #Check for punctuation
  lastChar = pair[-1]
  noEnd = True
  if (lastChar == "!"):
    noEnd = False
  if (lastChar == "."):
    noEnd = False
  if (lastChar == "?"):
    noEnd = False
  #Avoid infinite conversations
  if (ct > maxWords):
    noEnd = False
  #Return the update conversation
  return noEnd,text,pair,ct

### Main routines ###

#Print a blank line for formatting
print("")

#Pick the first statement
prevPair = random.choice(wordPairs.keys())
sentence = prevPair

#Continue the conversation
contSent = True #Flag to continue talkng
wordCt = 0 #Word counter
while (contSent):
  contSent,sentence,prevPair,wordCt = ContConv(sentence,prevPair,wordCt)
sentence += '\n'

#Remove random capitalization
sentence = sentence.lower()

#Add Gabbie's identity
sentence = " Gabbie: "+sentence

#Print the result
print(sentence)
