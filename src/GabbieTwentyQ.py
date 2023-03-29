##############################################################################
#                                                                            #
#                        GabbieBot: A simple chat bot                        #
#                              By Eric G. Kratz                              #
#                                                                            #
##############################################################################

# Python class to play twenty questions

import random


class TwentyQuest:
    numberOfQuestions = 20
    yesNoPrompt = "[Yes, No]"
    maxResponses = 3
    validYeses = ["yes", "yeah", "y"]
    validNos = ["no", "nope", "n"]

    knownAnswers = {}
    questions = []
    usedQuestions = []
    userAnswers = []

    def play(self):
        for _ in range(self.numberOfQuestions):
            nextQuestion = self.selectQuestion()
            self.askQuestion(nextQuestion)
            self.userAnswers.append(self.getResponse())
        guess = self.makeGuess()
        if guess is None or not self.guessIsCorrect(guess):
            self.updateMemories()
        return

    def randomQuestion(self):
        return random.choice(self.questions)

    def selectQuestion(self):
        if len(self.questions) < self.numberOfQuestions:
            raise RuntimeError(f"Fewer than {self.numberOfQuestions} are in defined.")
        while (question := self.randomQuestion()) not in self.usedQuestions:
            continue
        return question

    def askQuestion(self, nextQuestion):
        self.usedQuestions.append(nextQuestion)
        print(f"{nextQuestion} {self.yesNoPrompt}")

    def guessIsCorrect(self, guess):
        print(f"Is it {guess}? {self.yesNoPrompt}")
        return self.getResponse()

    def getResponse(self):
        count = 0
        while count < self.maxResponses:
            response = input("").lower()
            if response in self.validYeses:
                return True
            elif response in self.validNos:
                return False
            else:
                count += 1
                print("I did not understand your response. Please try again.")
        raise RuntimeError("No valid response was provided.")

    def makeGuess(self):
        assert len(self.userAnswers) == len(self.usedQuestions)
        counts, highestCount = self.scoreGuesses()
        return self.pickBestGuess(counts, highestCount)

    @staticmethod
    def pickBestGuess(counts, highestCount):
        if not counts:
            return None
        bestGuesses = []
        for keyCount in counts:
            if keyCount[1] < highestCount:
                break
            else:
                bestGuesses.append(keyCount[0])
        return random.choice(bestGuesses)

    def scoreGuesses(self):
        counts = []
        for key in self.knownAnswers:
            keyCount = [key, 0]
            for question, response in zip(self.usedQuestions, self.userAnswers):
                if response and question in self.knownAnswers[key]:
                    keyCount[1] += 1
            counts.append(keyCount)
        counts.sort(key=lambda x: x[1], reverse=True)
        highestCount = 0
        if len(counts) > 0:
            highestCount = counts[0][1]
        return counts, highestCount

    def updateMemories(self):
        correctAnswer = input("What was it then?")
        newMemory = []
        for question, response in zip(self.usedQuestions, self.userAnswers):
            if response:
                newMemory.append(question)
        self.knownAnswers.update({correctAnswer: newMemory})

    def readMemories(self, memPath):
        raise NotImplementedError
