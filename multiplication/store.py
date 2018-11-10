import random
from anna import Multiplication

def randomKey(length=5):
  return ''.join(random.choice("abcdefghijklmnopqrstuvwxyz0123456789") for i in range(length))

class Store():
  def __init__(self):
    self.quizzes = {}
  def create(self, questionsNumber=8, digits=2, operation="x"):
    quizKey = randomKey()
    questionsTemplate = {
      "%s 1" % digits: int(questionsNumber),
      # "1 1": 5
    }
    self.quizzes[quizKey] = Multiplication(questionsTemplate, operation=operation)
    return quizKey
  def get(self, quizKey):
    return self.quizzes.get(quizKey)