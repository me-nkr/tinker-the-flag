import web
from controllers.home import home
from controllers.submit import submit
from controllers.logout import logout
from controllers.admin import admin

# Notes
# error 0xf0 is clue file not found, check if the file exist


web.config.debug = False

urls = (
    "/", home,
    "/submit", submit,
    "/logout", logout,
    "/admin", admin,
    )

app = web.application(urls, locals())
render = web.template.render("templates/", base="layout")
db = web.database(dbn="sqlite", db="ttf.db")
db.insert("gamestate", key="started", value=False) # Initialize gamestate

def load_gctx():
    web.ctx.gctx = (db, render)
    web.template.Template.globals["baseurl"] = web.ctx.env["HTTP_HOST"]
    
app.add_processor(web.loadhook(load_gctx))

if __name__ == "__main__":
    app.run()
