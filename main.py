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

# https://www.a2hosting.com/web-hosting
# https://www.hostwinds.com/vps/linux


supportedApps = ["multiplication", "sirma", "job"]
restrictedApps = ["sirma"]

handlers = list(map(lambda x: __import__("%s.handlers" % x, fromlist="get_app"), supportedApps))

class DefaultHandler(tornado.web.RequestHandler):
    def get(self, path=""):
        print("path is -%s-" % path)
        if path:
            publicApps = filter(lambda x: x not in restrictedApps, supportedApps)
            self.render("404.html", path=path, supported=publicApps)
        else:
            self.render("home.html", path=path, supported=supportedApps)

def main():
    rules = []
    for i, appName in enumerate(supportedApps):
        app = handlers[i].get_app()
        rules.append(Rule(PathMatches("/%s.*" % appName), app))

    # Default app
    settings = dict(template_path="html", static_path="static", debug=True)
    app = tornado.web.Application([
        (r"/(.*)", DefaultHandler),
        (r'/favicon.ico', tornado.web.StaticFileHandler),
        (r'/static/', tornado.web.StaticFileHandler),
    ], **settings)
    rules.append(Rule(PathMatches(r"/.*"), app))
    router = RuleRouter(rules)

    http_server = tornado.httpserver.HTTPServer(router)
    port = int(os.environ.get("PORT", 5000))
    http_server.listen(port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()

