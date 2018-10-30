import time
import random

class Multiplication:
  questionsTemplate = {
    "2 1": 3,
    "1 1": 5
  }
  quiz = {}
  threshold = 11

  def getRandom(self, digits=1, lower=3, upper=9):
    result = "".join("%s"%random.randint(lower,upper) for x in range(digits))
    return int(result)

  def __init__(self):
    for (qString, number) in self.questionsTemplate.items():
      for i in range(number):
        x1, x2 = qString.split()
        x1 = self.getRandom(digits=int(x1))
        x2 = self.getRandom(digits=int(x2))
        key = "%s %s" % (x1, x2)
        self.quiz[key] = dict(x1=x1, x2=x2, response=None, success=None, startTime=0, endTime=0)

  def getQuestion(self, questionKey):
    self.quiz[questionKey]["startTime"] = time.time()
    return self.quiz[questionKey]

  def testQuestion(self, questionKey, response):
    self.quiz[questionKey]["response"] = response
    x1 = self.quiz[questionKey]["x1"]
    x2 = self.quiz[questionKey]["x2"]
    self.quiz[questionKey]["success"] = (str(response) == str(x1 * x2))
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

  def run(self):
    qKeys = self.getQuestionKeys()

    output = ""
    for qKey in qKeys:
      q = self.getQuestion(qKey)
      response = input("what is %s x %s = " % (q["x1"], q["x2"]))
      output += "%s\n" % self.testQuestion(qKey, response)
    
    print(output)
    print("average time: %.1fsecs, threshold: %.1fsecs" % (1.0*self.getTotalDuration()/len(qKeys), self.threshold))

m = Multiplication()
m.run()
