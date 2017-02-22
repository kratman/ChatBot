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
wordTrios = {} #A list of all trios of words to predict the next word

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

#Read word trios
try:
  memFile = open(GabbiePath+"/Knowledge/Memories_trios.txt","r")
  memData = memFile.readlines()
  for triolist in memData:
    tempData = triolist.strip().split()
    tempTrio = tempData[0]+" "+tempData[1]+" "+tempData[2]
    tempDict = {tempTrio : tempData[3:]}
    wordTrios.update(tempDict)
  memFile.close()
  memData = [] #Clear RAM
except:
  line = ""
  line += "Error: No memories located!"
  print(line)

### Functions ###

#Two word Markov chain model
def ConvPairs(text,pair,ct):
  #Defined constraints
  maxWords = 40
  #Continue the sentence
  if (pair in wordPairs):
    #Add the next word
    if (len(wordPairs[pair]) > 1):
      binSize = 1.0/(len(wordPairs[pair])-1)
    else:
      binSize = 1.0/len(wordPairs[pair])
    wordFound = False
    wordID = 0
    #Find a word with a biased random choice
    while (wordFound == False):
      if (random.random() < binSize):
        #Accept this word
        wordFound = True
      else:
        #Move to the next word
        wordID += 1
        wordID = wordID%len(wordPairs[pair])
      nextWord = wordPairs[pair][wordID]
    text += " "+nextWord
    pair = pair.split()[1]+" "+nextWord
    ct += 1
  else:
    #Choose randomly
    pair = random.choice(list(wordPairs.keys()))
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
    #Stop the sentence
    noEnd = False
    #Add a period to improve the formatting
    text += "."
  #Return the update conversation
  return noEnd,text,pair,ct

#Three word Markov chain model
def ConvTrios(text,trio,ct):
  #Defined constraints
  maxWords = 40
  #Continue the sentence
  if (trio in wordTrios):
    #Add the next word
    if (len(wordTrios[trio]) > 1):
      binSize = 1.0/(len(wordTrios[trio])-1)
    else:
      binSize = 1.0/len(wordTrios[trio])
    wordFound = False
    wordID = 0
    #Find a word with a biased random choice
    while (wordFound == False):
      if (random.random() < binSize):
        #Accept this word
        wordFound = True
      else:
        #Move to the next word
        wordID += 1
        wordID = wordID%len(wordTrios[trio])
      nextWord = wordTrios[trio][wordID]
    text += " "+nextWord
    trio = trio.split()[1]+trio.split()[2]+" "+nextWord
    ct += 1
  else:
    #Choose randomly
    trio = random.choice(list(wordTrios.keys()))
    text += " "+trio
    ct += 3
  #Check for punctuation
  lastChar = trio[-1]
  noEnd = True
  if (lastChar == "!"):
    noEnd = False
  if (lastChar == "."):
    noEnd = False
  if (lastChar == "?"):
    noEnd = False
  #Avoid infinite conversations
  if (ct > maxWords):
    #Stop the sentence
    noEnd = False
    #Add a period to improve the formatting
    text += "."
  #Return the update conversation
  return noEnd,text,trio,ct

### Main routines ###

#Print a blank line for formatting
print("")

#Save user's input
try:
  #Save the user input
  sentence = ""
  sentence += sys.argv[1]
  #Check punctuation
  lastChar = sentence[-1]
  if ((lastChar != ".") and (lastChar != "!") and (lastChar != "?")):
    #Add a period
    sentence = sentence+"."
  #Improve formatting
  if (sentence[0] != " "):
    sentence = " "+sentence
  #Identify the user
  sentence = " User:"+sentence
  #Print the user input
  sentence += '\n'
  print(sentence)
  #Reset the sentence for Gabbie
  sentence = ""
except:
  #Ignore the error and do nothing
  pass

#Process the user's statement
try:
  #Copy the user input
  sentence = ""
  sentence += sys.argv[1]
  #Check punctuation
  lastChar = sentence[-1]
  if ((lastChar != ".") and (lastChar != "!") and (lastChar != "?")):
    #Add a period
    sentence = sentence+"."
  try:
    #Save the last three words as input for Gabbie
    prevPair = None
    prevTrio = sentence.strip().split()
    prevTrio = prevTrio[-3]+" "+prevTrio[-2]+" "+prevTrio[-1]
  except:
    #Save the last two words as input for Gabbie
    prevTrio = None
    prevPair = sentence.strip().split()
    prevPair = prevPair[-2]+" "+prevPair[-1]
  #Reset the sentence for Gabbie
  sentence = ""
except:
  #Randomly pick the first statement
  prevTrio = None
  prevPair = random.choice(list(wordPairs.keys()))
  sentence = prevPair

#Continue the conversation
contSen = True #Flag to continue talkng
wordCt = 0 #Word counter
while (contSen):
  #Decide if pairs or trios of words should be used
  if ((prevTrio == None) or (random.random() > 0.5)):
    #Use the the two word Markov chain
    contSen,sentence,prevPair,wordCt = ConvPairs(sentence,prevPair,wordCt)
    #Update previous trio
    prevTrio = sentence.strip().split()
    if (len(prevTrio) > 2):
      #A valid trio exists
      prevTrio = prevTrio[-3]+" "+prevTrio[-2]+" "+prevTrio[-1]
    else:
      #Avoid using an invalid trio
      prevTrio = None
  else:
    #Use the three word Markov chain
    contSen,sentence,prevTrio,wordCt = ConvTrios(sentence,prevTrio,wordCt)
    #Update previous pair
    prevPair = sentence.strip().split()
    prevPair = prevTrio[-2]+" "+prevTrio[-1]
sentence += '\n'

#Remove random capitalization
sentence = sentence.lower()

#Smoothly transion between user input and Gabbie output
if (sentence[0] != " "):
  sentence = " "+sentence

#Add Gabbie's identity
sentence = " Gabbie:"+sentence

#Print the result
print(sentence)

#Quit
exit(0)
