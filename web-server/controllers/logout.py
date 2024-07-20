import web

class logout:

    def GET(self):
        web.setcookie("register_id", None, expires=0)
        raise web.seeother("/")