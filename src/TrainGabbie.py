##############################################################################
#                                                                            #
#                        GabbieBot: A simple chat bot                        #
#                              By Eric G. Kratz                              #
#                                                                            #
##############################################################################

#A script for teaching GabbieBot to speak using plain text books

### Usage ###
#
# user:$ python TrainGabbie.py BookFileName <...>
#
# Note: <...> represents additional books which are optional to include
#

### Import libraries ###

import os
import sys

### Initialize variables

numBooks = 0 #Number of books given to Gabbie
numErrors = 0 #Temporary storage for the number of errors
totalWords = 0 #Total number of words in all books
numWords = 0 #Number of unique words in all books
bookNames = [] #List of book file names
wordStats = {} #List of all words and the statistics

### Print a blank line ###

#Makes the output look a little bit better
print("")

### Read the names of the books ###

#Use a count of the arguments given to python
#Note: The first argument is always the name of the script
numBooks = len(sys.argv)-1

for i in range(numBooks):
  #Safely read the name of the book
  tempName = sys.argv[i+1]
  if (os.path.exists(tempName) == True):
    #The operating system located the book
    bookNames.append(tempName)
  else:
    #The book is missing
    numErrors += 1 #Increase the number of errors
    textLine = "" #Empty string
    #Add an error message
    textLine += "Error: A book "
    textLine += tempName
    textLine += " was not found!"
    #Print the error and continue
    print(textLine)

#Adjust the number of books by subtracting the number of errors
numBooks -= numErrors

#Reset the number of errors
numErrors = 0

### Convert books to dictionaries ###

#Loop over the books
for book in bookNames:
  #Open the book in read (r) mode
  bookFile = open(book,"r")
  #Read the entire book into memory
  bookData = bookFile.readlines()
  #Loop over all of the lines in the book
  for sentence in bookData:
    #Break the line into words
    words = sentence.strip().split()
    #Loop over all words
    for word in words:
      #Check if the word is in the dictionary
      if (wordStats.has_key(word) == True):
        #Update the number of times the word appears
        wordStats[word] += 1
        #Update the word count
        totalWords += 1
      else:
        #Add the word to the dictionary
        tempDict = {word : 1.0} #Blank item for the word
        wordStats.update(tempDict) #Add the new word
        #Update the statistics
        totalWords += 1
        numWords += 1

### Calculate statistics for word order ###

#Calculate the statistical weight of the word


#Loop over the words a second time to learn word order


### Save dictionary to the memory files ###



### Print final output ###

#Create an empty line of text
textLine = ""

#Add a description
textLine += "Learning statistics:"
textLine += '\n'

#Number of books
textLine += "  Number of books: "
textLine += str(numBooks)
textLine += '\n'

#Number of words
textLine += "  Total number of words: "
textLine += str(totalWords)
textLine += '\n'
textLine += "  Number of unique words: "
textLine += str(numWords)
textLine += '\n'

#Print results
print(textLine)

### Clean up and exit
exit(0) #Cleanly exit the program
