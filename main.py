import os
import tornado.httpserver
import tornado.ioloop
import tornado.web
import time
import json
# import redis
import random
import datetime
from operator import attrgetter, itemgetter

class MainHandler(tornado.web.RequestHandler):
    def get(self, gid=None):
    	# self.write("ok")
        self.render("index.html")
 
def main():
    settings = dict(template_path="html", static_path="static", debug=True)
    application = tornado.web.Application([
        (r"/(\d*)", MainHandler),
        # (r'/favicon.ico', tornado.web.StaticFileHandler),
        (r'/static/', tornado.web.StaticFileHandler),
    ], **settings)

    http_server = tornado.httpserver.HTTPServer(application)
    port = int(os.environ.get("PORT", 5000))
    http_server.listen(port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()

