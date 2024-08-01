import web
from controllers.utils import userauth, logger

class home:

    def GET(self):
        
        db, render = web.ctx.gctx
        
        state = {}
        for entry in db.select("gamestate").list():
            state[entry.key] = entry.value

        error = ""
        clue_data = ""
        
        auth = userauth(web, db, render, state, home=True)
        if not auth["status"]:
            return auth["data"]
        else:
            register_id, player_name = auth["data"]

        if state.get("started"):
            try:
                with open("images/" + register_id + ".pbm", "r") as clue:
                    clue_data = clue.read()
            except FileNotFoundError:
                error = "error 0xf0, please contact the organizer"
                logger.warn(f"missing image file for player <{register_id}>")

        return render.home(error, "registered", state.get("started"), clue_data, register_id, player_name)


    def POST(self):

        db, render = web.ctx.gctx

        state = {}
        for entry in db.select("gamestate").list():
            state[entry.key] = entry.value

        error = ""

        if web.ctx.env["CONTENT_TYPE"] != "application/x-www-form-urlencoded":
            raise web.badrequest("Invalid request")
        
        register_id = web.cookies().get("register_id")
        reg_in =  web.input().get("register_id")

        register_id = reg_in if reg_in is not None else register_id
        player_name = web.input().get("player_name")
        
        if register_id == "":
            error = "empty registration id"
            web.setcookie("register_id", None, expires=0)
            return render.home(error, "new", state.get("started"))
        elif register_id is None:
            raise web.seeother("/") 
        
        player_record = db.where("scoreboard", what="player_name, banned", player_id=register_id).list()

        if len(player_record) < 1:
            if state.get("login_locked"):
                error = "player not registered"
                web.setcookie("register_id", None, expires=0)
                return render.home(error, "new", state.get("started"), register_id=register_id)
            else:
                db.insert("scoreboard", player_id=register_id, player_name=None, time=None, partner_id=None, flag=None, verified=False, banned=False)
                logger.info(f"player <{register_id}> joined")
        
        if len(player_record) > 1 and player_record[0].get("banned"):
            error = "you are banned"
            web.setcookie("register_id", None, expires=0)
            return render.home(error, "new", state.get("started"), register_id=register_id)

        web.setcookie("register_id", register_id, httponly= True, samesite="Strict")
        
        if len(player_record) < 1 or not player_record[0].get("player_name"):
            if player_name is None:
                raise web.seeother("/")
            elif player_name == "":
                error = "name can't be empty"
                return render.home(error, "onboard", state.get("started"), register_id=register_id)
            else:
                db.update("scoreboard", vars={"reg_id": register_id}, where="player_id = $reg_id", player_name=player_name)
                logger.info(f"player <{register_id}> updated their name to <{player_name}>")

        raise web.seeother("/")
