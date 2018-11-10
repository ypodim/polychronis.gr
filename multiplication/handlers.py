import tornado.web
from multiplication.store import Store

class DefaultHandler(tornado.web.RequestHandler):
  def initialize(self, store):
    self.store = store

class MainHandler(DefaultHandler):
  def get(self, gid=None):
    self.render("index.html", gid=gid)

class QuizDataHandler(DefaultHandler):
  def get(self, quizKey):
    self.store.get(quizKey).getStats()
    quiz = self.store.get(quizKey)
    self.write(dict(qKeys=quiz.getQuestionKeys(), 
                    operation=quiz.getOperation(), 
                    stats=self.store.get(quizKey).getStats()))

class QuestionDataHandler(DefaultHandler):
  def get(self, quizKey, qKey):
    self.write(self.store.get(quizKey).getQuestion(qKey))

  def post(self, quizKey, qKey):
    response = self.get_argument("response")
    result = self.store.get(quizKey).testQuestion(qKey, response)
    self.write(dict(qKey=qKey, response=response, outcome=result))

class GameHandler(DefaultHandler):
  def get(self, quizKey):
    questions = self.store.get(quizKey)
    quiz = self.store.get(quizKey)
    if not quiz:
      self.render("404.html")
      return
    questions = quiz.getQuestionKeys()
    if questions:
      self.render("game.html")
    else:
      self.write("quiz %s not found" % quizKey)
  def post(self, path=None):
    questions = self.get_argument("questions")
    digits = self.get_argument("digits")
    operation = "x"
    if self.get_argument("operation") == "addition":
      operation = "+"
    quizKey = self.store.create(questionsNumber=questions, digits=digits, operation=operation)
    self.write(dict(quizKey=quizKey))

def get_app():
  settings = dict(template_path="multiplication/html", static_path="static", debug=True)
  store = Store()
  handlers = [
    (r"/multiplication/?", MainHandler, dict(store=store)),
    (r"/multiplication/data/([a-z0-9]*)", QuizDataHandler, dict(store=store)),
    (r"/multiplication/data/([a-z0-9]*)/([a-z0-9]*)", QuestionDataHandler, dict(store=store)),
    (r"/multiplication/game/?(.*)", GameHandler, dict(store=store)),
  ]
  return tornado.web.Application(handlers, **settings)

