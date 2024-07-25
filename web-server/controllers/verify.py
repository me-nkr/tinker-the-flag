import web
from controllers.utils import adminauth, logger

class verify:

    def GET(self):

        adminauth(web)

        db, render = web.ctx.gctx
        
        state = {}
        for entry in db.select("gamestate").list():
            state[entry.key] = entry.value

        player_id = web.input().get("player_id")
        
        if not player_id or len(db.where("scoreboard", player_id=player_id, verified=False).list()) < 1:
            raise web.seeother("/admin")

        return render.confirm(started=state.get("started"), action="verify", player_id=player_id)

    def POST(self):

        adminauth(web)

        db, render = web.ctx.gctx
        
        state = {}
        for entry in db.select("gamestate").list():
            state[entry.key] = entry.value
            
        if state.get("started") == True:
            raise web.seeother("/verify")
        
        verify = web.input().get("verify")
        player_id = web.input().get("player_id")
        
        if verify is not None and verify == "verify" and player_id is not None and player_id != "":
            if len(db.where("scoreboard", player_id=player_id).list()) < 1:
                raise web.seeother("/admin")
            else:
                db.update("scoreboard", vars={"id": player_id}, where="player_id = $id", verified=True)
                logger.info(f"player <{player_id}> just got verified")
            
        raise web.seeother("/admin")
        