import tornado.web


class MainHandler(tornado.web.RequestHandler):
    def get(self, gid=None):
        self.render("job.html", answer="Not right now.", color="")

def get_app():
	settings = dict(template_path="html", static_path="static", debug=True)
	return tornado.web.Application([(r"/(.*)", MainHandler)], **settings)
