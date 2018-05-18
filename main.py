import os
import tornado.httpserver
import tornado.ioloop
import tornado.web
from tornado.routing import RuleRouter, Rule, PathMatches
import time
import json
# import redis
import random
import datetime
from operator import attrgetter, itemgetter

supportedApps = ["app1", "game2"]

class MainHandler(tornado.web.RequestHandler):
    def get(self, gid=None):
        self.render("index.html", gid=gid)

class DefaultHandler(tornado.web.RequestHandler):
    def get(self, path=""):
        self.render("404.html", path=path, supported=supportedApps)
 
def main():
    settings = dict(template_path="html", static_path="static", debug=True)
    
    rules = []
    for appName in supportedApps:
        app = tornado.web.Application([(r"/%s(.*)" % appName, MainHandler)], **settings)
        rules.append(Rule(PathMatches("/%s.*" % appName), app))

    app = tornado.web.Application([(r"/(.*)", DefaultHandler)], **settings)
    rules.append(Rule(PathMatches(r"/.*"), app))
    router = RuleRouter(rules)

    # application = tornado.web.Application([
    #     (r"/(.*)", MainHandler),
    #     # (r'/favicon.ico', tornado.web.StaticFileHandler),
    #     (r'/static/', tornado.web.StaticFileHandler),
    # ], **settings)

    http_server = tornado.httpserver.HTTPServer(router)
    port = int(os.environ.get("PORT", 5000))
    http_server.listen(port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()

