import web, hashlib, time
from controllers.utils import userauth, logger

class submit: 
    
    def GET(self):

        db, render = web.ctx.gctx

        state = {}
        for entry in db.select("gamestate").list():
            state[entry.key] = entry.value

        
        if not state.get("started"):
            raise web.seeother("/")
        
        auth = userauth(web, db, render, state)
        if not auth["status"]:
            return auth["data"]
        else:
            register_id, player_name = auth["data"]

        results = db.where("scoreboard", what="flag, time", player_id=register_id).list()[0]
        
        if not results.get("flag") or not results.get("time"):
            return render.submit(player_name=player_name)
    
        return render.submit(status=True, player_name=player_name)


    def POST(self):
        
        db, render = web.ctx.gctx

        state = {}
        for entry in db.select("gamestate").list():
            state[entry.key] = entry.value

        error = ""

        if web.ctx.env["CONTENT_TYPE"] != "application/x-www-form-urlencoded":
            raise web.badrequest("Invallid request")
            
        auth = userauth(web, db, render, state)
        if not auth["status"]:
            return auth["data"]
        else:
            register_id, player_name = auth["data"]

        results = db.where("scoreboard", what="flag, time", player_id=register_id).list()[0]
        
        if results.get("flag") and results.get("time"):
            raise web.seeother("/submit")


        partner_id = web.input().get("partner_id")
        username = web.input().get("username")
        password = web.input().get("password")
        flag = web.input().get("flag")
        
        if not partner_id or len(db.where("scoreboard", partner_id=register_id, player_id=partner_id).list()) < 1:
            error = "invalid partner id"
            return render.submit(error, partner_id=partner_id, username=username, password=password, flag=flag, player_name=player_name)
        
        playerset = sorted((register_id, partner_id))
        
        if not username or username != hashlib.shake_128((playerset[0] + "mix the users" + playerset[1]).encode("ascii")).hexdigest(3):
            error = "invalid username"
        elif not password or password != hashlib.shake_128((username + "salty password").encode("ascii")).hexdigest(4):
            error = "invalid password"
        elif not flag or flag != hashlib.shake_256((username + "tinker the flag" + password).encode("ascii")).hexdigest(8):
            error = "invalid flag"
        
        if error:
            return render.submit(error, partner_id=partner_id, username=username, password=password, flag=flag, player_name=player_name)

        db.update("scoreboard", vars={"reg_id": register_id, }, where="player_id = $reg_id", flag=flag, time=time.time())
        logger.info(f"player <{register_id}> submitted the flag")
        raise web.seeother("/submit")
            
