import web
from controllers.utils import adminauth, logger

class add:

    def GET(self):
        
        adminauth(web)

        db, render = web.ctx.gctx
        
        state = {}
        for entry in db.select("gamestate").list():
            state[entry.key] = entry.value
            
        return render.add(started=state.get("started"))


    def POST(self):
        
        adminauth(web)

        db, render = web.ctx.gctx
        
        state = {}
        for entry in db.select("gamestate").list():
            state[entry.key] = entry.value
            
        if state.get("started") == True:
            raise web.seeother("/add")
            
        error = ""

        if web.ctx.env["CONTENT_TYPE"] != "application/x-www-form-urlencoded":
            raise web.badrequest("Invalid request")
        
        register_id = web.input().get("register_id")
        player_name = web.input().get("player_name")
        
        if register_id == "":
            error = "registration id can't be empty"
            return render.add(error, started=state.get("started"), register_id=register_id, player_name=player_name)
        elif register_id is None:
            raise web.seeother("/add")

        if player_name == "":
            error = "player name can't be empty"
            return render.add(error, started=state.get("started"), register_id=register_id, player_name=player_name)
        elif player_name is None:
            raise web.seeother("/add")
            
        if len(db.where("scoreboard", player_id=register_id).list()) > 0:
            error = "player already exists"
            return render.add(error, started=state.get("started"), register_id=register_id, player_name=player_name)
        
        db.insert("scoreboard", player_id=register_id, player_name=player_name, time=None, partner_id=None, flag=None, verified=False, banned=False)
        logger.info(f"player <{register_id}> with name <{player_name}> was added")
        raise web.seeother("/admin")