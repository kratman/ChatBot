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
        print(f"{nextQuestion} {self.yesNoPrompt}")

    def guessIsCorrect(self, guess):
        print(f"Is it {guess}? {self.yesNoPrompt}")
        return self.getResponse()

    def getResponse(self):
        raise NotImplementedError

    def makeGuess(self):
        assert len(self.userAnswers) == len(self.usedQuestions)
        raise NotImplementedError

    def updateMemories(self):
        raise NotImplementedError

    def readMemories(self, memPath):
        raise NotImplementedError
