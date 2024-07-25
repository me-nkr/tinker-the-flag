import web, re, base64, random, hashlib
from controllers.utils import generate_steganograph_image_pair, logger


class admin:

    def GET(self):
        
        db, render = web.ctx.gctx

        state = {}
        for entry in db.select("gamestate").list():
            state[entry.key] = entry.value

        auth()
        
        # interface requirements
            # start game [ ]
            # stats
                # player count ( important ) [x]
                # unique images downloaded
                # unique logins
                # flag file opens
                # flag submissions ( important ) [x]
        
        player_count = len(db.select("scoreboard").list())
        flag_submission_count = len(db.select("scoreboard", where="flag not null").list())
        
        return render.admin(state.get("started"), player_count, flag_submission_count)


    def POST(self):

        db, render = web.ctx.gctx

        state = {}
        for entry in db.select("gamestate").list():
            state[entry.key] = entry.value

        auth()
        
        start = web.input().get("start")
        
        if not state.get("started") and start is not None and start == "game":

            if not state.get("debug"):

                inpipe = "/home/control/ttfmessageinpipe"
                outpipe = "/home/control/ttfmessageoutpipe"
                
                with open(inpipe, "w") as call:
                    call.write("start")
                    call.flush()
                
                with open(outpipe, "r") as res:
                    for line in res:
                        if not line == "done":
                            logger.error(line)
                            return render.admin(False, 0, 0, error="Unexpected return from daemon: " + line)

                players = db.select("scoreboard", what="player_id").list()
                pairs = []

                while len(players):
                    item = players.pop(random.randrange(len(players)))
                    pair = players.pop(random.randrange(len(players)))
                    pairs.append(sorted([item.player_id, pair.player_id]))
                    
                pair_index = 0
                    
                for pair in pairs:
                    db.update("scoreboard", vars={"reg_id": pair[0]}, where="player_id = $reg_id", partner_id=pair[1])
                    db.update("scoreboard", vars={"reg_id": pair[1]}, where="player_id = $reg_id", partner_id=pair[0])
                    
                    username = hashlib.shake_128((pair[0] + "mix the users" + pair[1]).encode("ascii")).hexdigest(3)
                    password = hashlib.shake_128((username + "salty password").encode("ascii")).hexdigest(4)
                    flag = hashlib.shake_256((username + "tinker the flag" + password).encode("ascii")).hexdigest(8)

                    with open(inpipe, "w") as call:
                        call.write(f"{username}:{password}:{flag}")
                        call.flush()

                    with open(outpipe, "r") as res:
                        for line in res:
                            if not line == "done":
                                logger.error(line)
                                return render.admin(False, 0, 0, error="Unexpeccted reply from daemon" + line)
                
                    logger.info(f"ctf box user <{username}> with password <{password}> and flag <{flag}> created for players <{pair[0]}> and <{pair[1]}>")

                    generate_steganograph_image_pair(pair, pair_index, username, password)
                    logger.info(f"clue images generated for players <{pair[0]}> and <{pair[1]}>")

                    pair_index += 1

                
                with open(inpipe, "w") as call:
                    call.write("end")
                    call.flush()

                with open(outpipe, "r") as res:
                    for line in res:
                        if not line == "done":
                            logger.error(line)
                            return render.admin(False, 0, 0, error="Unexpeccted reply from daemon" + line)
                    
            db.update("gamestate", vars={"key": "started"}, where="key = $key", value=True)
            logger.info("game started")

        web.header("Authorization", "Basic " + base64.b64encode("gamemaster:letthegamesbegin".encode("ascii")).decode("ascii"))
        raise web.seeother("/admin")


def validate_creds(creds):
    
    allowed = ("gamemaster", "letthegamesbegin")

    auth = re.sub("^Basic ", "", creds)
    username, password = base64.b64decode(auth).decode("ascii").split(":")
    
    return True if (username, password) == allowed else False

def auth():

    creds = web.ctx.env.get("HTTP_AUTHORIZATION")

    if not creds or not validate_creds(creds):
        web.header("WWW-Authenticate", "Basic realm=\"ttf admin\"")
        raise web.unauthorized()
