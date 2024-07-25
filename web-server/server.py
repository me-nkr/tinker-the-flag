import web, os
from controllers.home import home
from controllers.submit import submit
from controllers.logout import logout
from controllers.admin import admin
from controllers.utils import logger

import sys
sys.path.append("..")
try:
    from config import config
except ModuleNotFoundError:
    logger.error("missing config file")
    exit()

# Notes
# error 0xf0 is clue file not found, check if the file exist

if not os.path.exists("../ttfmessageinpipe") or not os.path.exists("../ttfmessageoutpipe"):
    logger.error("missing message pipe")
    exit()
if not os.path.exists("ttf.db"):
    logger.error("missing database")
    exit()

logger.init()

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

# Initialize gamestate
if len(db.where("gamestate", key="started").list()) < 1:
    db.insert("gamestate", key="started", value=False)
else:
    db.update("gamestate", where="key = 'started'", value=False)

def load_gctx():
    web.ctx.gctx = (db, render)
    web.template.Template.globals["baseurl"] = web.ctx.env["HTTP_HOST"]
    
app.add_processor(web.loadhook(load_gctx))

if __name__ == "__main__":
    app.run()
