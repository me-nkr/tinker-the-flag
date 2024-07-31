import web

class scoreboard:

    def GET(self):
        
        db, render = web.ctx.gctx
        
        state = {}
        for entry in db.select("gamestate").list():
            state[entry.key] = entry.value
            
        scores = db.query("SELECT \
                            t1.player_name || ' and ' || t2.player_name AS team, \
                            ((t1.time + t2.time)/2) AS time \
                          FROM scoreboard t1 \
                          JOIN scoreboard t2 \
                          ON t1.player_id = t2.partner_id \
                          AND t1.partner_id = t2.player_id \
                          AND t1.player_id < t2.player_id \
                          AND t1.time is not null \
                          AND t2.time is not null \
                          ORDER BY (t1.time + t2.time)/2").list()
        scoreboard =  list(map(lambda score: dict(score), scores))

        return render.scoreboard(state.get("start_time"), scoreboard)