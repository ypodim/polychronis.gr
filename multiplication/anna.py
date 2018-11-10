import time
import random

class Multiplication:
  def getRandom(self, digits=1, lower=3, upper=9):
    result = "".join("%s"%random.randint(lower,upper) for x in range(digits))
    return int(result)

  def __init__(self, questionsTemplate, operation="x"):
    self.quiz = {}
    self.threshold = 11
    self.operation = operation

    for (qString, number) in questionsTemplate.items():
      for i in range(number):
        x1, x2 = qString.split()
        x1 = self.getRandom(digits=int(x1))
        x2 = self.getRandom(digits=int(x2))
        key = "%s%s" % (x1, x2)
        self.quiz[key] = dict(x1=x1, x2=x2, response=None, success=None, startTime=0, endTime=0)

  def getQuestion(self, questionKey):
    if not self.quiz[questionKey]["startTime"]:
      self.quiz[questionKey]["startTime"] = time.time()
    return self.quiz[questionKey]
  def getOperation(self):
    return self.operation
  def evaluate(self, x1, x2):
    if self.operation == "+":
      return str(x1 + x2)
    return str(x1 * x2)

  def testQuestion(self, questionKey, response):
    self.quiz[questionKey]["response"] = response
    x1 = self.quiz[questionKey]["x1"]
    x2 = self.quiz[questionKey]["x2"]
    self.quiz[questionKey]["success"] = (str(response) == self.evaluate(x1, x2))
    self.quiz[questionKey]["endTime"] = time.time()
    if self.quiz[questionKey]["startTime"] == 0:
      self.quiz[questionKey]["startTime"] = self.quiz[questionKey]["endTime"]

    return self.formatQuestionStat(questionKey)

  def getQuestionKeys(self):
    return self.quiz.keys()
  def getQuiz(self):
    return self.quiz

  def formatQuestionStat(self, qKey):
    q = self.quiz[qKey]
    duration = q["endTime"] - q["startTime"]
    return "%s x %s = %s (%s) in %.1fsecs" % (q["x1"], q["x2"], q["response"], q["success"], duration)

  def getTotalDuration(self):
    totalTime = 0
    for q in self.quiz.values():
      if q["response"]:
        totalTime += q["endTime"] - q["startTime"]
    return totalTime

  def getAverageTime(self):
    return 1.0*self.getTotalDuration()/len(self.quiz)

  def getStats(self):
    result = {}
    for qKey, question in self.quiz.items():
      result[qKey] = dict(success=question["success"], time=question["endTime"]-question["startTime"])
    return result

if __name__=="__main__":
  questionsTemplate = {
    "2 1": 3,
    "1 1": 5
  }
  m = Multiplication(questionsTemplate)

  for qKey in m.getQuestionKeys():
    q = m.getQuestion(qKey)
    response = input("what is %s x %s = " % (q["x1"], q["x2"]))
    m.testQuestion(qKey, response)

  print("average time: %.1fsecs, threshold: %.1fsecs" % (m.getAverageTime(), m.threshold))



