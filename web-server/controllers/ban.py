import web
from controllers.utils import adminauth, logger

class ban:

    def GET(self):

        adminauth(web)

        db, render = web.ctx.gctx
        
        state = {}
        for entry in db.select("gamestate").list():
            state[entry.key] = entry.value

        player_id = web.input().get("player_id")
        
        if not player_id or len(db.where("scoreboard", player_id=player_id, verified=True, banned=False).list()) < 1: 
            raise web.seeother("/admin")

        return render.confirm(started=state.get("started"), action="ban", player_id=player_id)

    def POST(self):

        adminauth(web)

        db, render = web.ctx.gctx
        
        state = {}
        for entry in db.select("gamestate").list():
            state[entry.key] = entry.value
            
        ban = web.input().get("ban")
        player_id = web.input().get("player_id")
        
        if ban is not None and ban == "ban" and player_id is not None and player_id != "":
            if len(db.where("scoreboard", player_id=player_id, verified=True).list()) < 1:
                raise web.seeother("/admin")
            else:
                db.update("scoreboard", vars={"id": player_id}, where="player_id = $id", banned=True)
                logger.info(f"player <{player_id}> was banned")
            
        raise web.seeother("/admin")
 