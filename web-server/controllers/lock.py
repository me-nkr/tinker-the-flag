import web
from controllers.utils import adminauth, logger

class lock:

    def GET(self):

        adminauth(web)

        db, render = web.ctx.gctx
        
        state = {}
        for entry in db.select("gamestate").list():
            state[entry.key] = entry.value

        if state.get("started"):
            raise web.seeother("/admin")

        return render.confirm(started=state.get("started"), action="lock", locked=state.get("login_locked"), ended=state.get("ended"))

    def POST(self):

        adminauth(web)

        db, render = web.ctx.gctx
        
        state = {}
        for entry in db.select("gamestate").list():
            state[entry.key] = entry.value
            
        if state.get("started") == True or state.get("login_locked") == True:
            raise web.seeother("/lock")
        
        lock = web.input().get("lock")
        
        if lock is not None and lock == "lock":
            db.update("gamestate", where="key = 'login_locked'", value=True)
            logger.info(f"player login locked")
            
        raise web.seeother("/admin")
        