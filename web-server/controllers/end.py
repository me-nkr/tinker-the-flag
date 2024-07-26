import web
from controllers.utils import adminauth, logger

class end:

    def GET(self):

        adminauth(web)

        db, render = web.ctx.gctx
        
        state = {}
        for entry in db.select("gamestate").list():
            state[entry.key] = entry.value

        if not state.get("started") or state.get("ended"):
            raise web.seeother("/admin")

        return render.confirm(started=state.get("started"), action="end", locked=state.get("login_locked"), ended=state.get("ended"))

    def POST(self):

        adminauth(web)

        db, render = web.ctx.gctx
        
        state = {}
        for entry in db.select("gamestate").list():
            state[entry.key] = entry.value
            
        if not state.get("started") == True or state.get("ended") == True:
            raise web.seeother("/end")
        
        end = web.input().get("end")
        
        if end is not None and end == "end":
            db.update("gamestate", where="key = 'ended'", value=True)
            logger.info(f"game ended")
            
        raise web.seeother("/admin")
        
