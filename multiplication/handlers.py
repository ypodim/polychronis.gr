import tornado.web


class MainHandler(tornado.web.RequestHandler):
    def get(self, gid=None):
        self.render("index.html", gid=gid)

def get_app():
	settings = dict(template_path="multiplication/html", static_path="static", debug=True)
	return tornado.web.Application([(r"/(.*)", MainHandler)], **settings)
