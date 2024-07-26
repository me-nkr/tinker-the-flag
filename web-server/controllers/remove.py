import web
from controllers.utils import adminauth, logger

class remove:

    def GET(self):

        adminauth(web)

        db, render = web.ctx.gctx
        
        state = {}
        for entry in db.select("gamestate").list():
            state[entry.key] = entry.value

        player_id = web.input().get("player_id")
        
        if not player_id or len(db.where("scoreboard", player_id=player_id).list()) < 1: 
            raise web.seeother("/admin")

        return render.confirm(started=state.get("started"), action="remove", player_id=player_id, locked=state.get("login_locked"), ended=state.get("ended"))

    def POST(self):

        adminauth(web)

        db, render = web.ctx.gctx
        
        state = {}
        for entry in db.select("gamestate").list():
            state[entry.key] = entry.value
            
        if state.get("started") == True:
            raise web.seeother("/remove")
        
        remove = web.input().get("remove")
        player_id = web.input().get("player_id")
        
        if remove is not None and remove == "remove" and player_id is not None and player_id != "":
            if len(db.where("scoreboard", player_id=player_id).list()) < 1:
                raise web.seeother("/admin")
            else:
                db.delete("scoreboard", vars={"id": player_id}, where="player_id = $id")
                logger.info(f"player <{player_id}> was removed")
            
        raise web.seeother("/admin")
 