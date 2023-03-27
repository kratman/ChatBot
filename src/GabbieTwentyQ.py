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
    knownAnswers = {}
    questions = []
    usedQuestions = []
    userAnswers = []

    def play(self):
        count = 0
        while count < self.numberOfQuestions:
            nextQuestion = self.selectQuestion()
            self.askQuestion(nextQuestion)
            self.userAnswers.append(self.getResponse())
        guess = self.makeGuess()
        if not self.guessIsCorrect(guess):
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
        print(nextQuestion)

    def makeGuess(self):
        raise NotImplementedError

    def getResponse(self):
        raise NotImplementedError

    def guessIsCorrect(self, guess):
        raise NotImplementedError

    def updateMemories(self):
        raise NotImplementedError

    def readMemories(self, memPath):
        raise NotImplementedError
