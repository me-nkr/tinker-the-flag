import time, re, base64
from PIL import Image, ImageDraw, ImageFont
from netpbmfile import imwrite
import numpy as np

class logger:

    def error(message):
        with open("../game.log", "a") as log:
            log.write(f"[{time.asctime()}] [ERROR]: {message}\n")

    def info(message):
        with open("../game.log", "a") as log:
            log.write(f"[{time.asctime()}] [INFO]: {message}\n")

    def warn(message):
        with open("../game.log", "a") as log:
            log.write(f"[{time.asctime()}] [WARN]: {message}\n")

    def init():
        with open("../game.log", "a") as log:
            log.write(f"\n\n[{time.asctime()}] [INIT]: server initialized\n")



import sys
sys.path.append("..")
try:
    from config import config
except ModuleNotFoundError:
    logger.error("missing config file")
    exit()
    
admin_username = config.get("admin_username") or "gamemaster"
admin_password = config.get("admin_password") or "gamemaster"

def userauth(web, db, render, state, home=False):

    register_id = web.cookies().get("register_id")
    
    player_record = db.where("scoreboard", what="player_name", player_id=register_id).list()
    
    if not register_id or len(player_record) < 1:
        if home:
            web.setcookie("register_id", None, expires=0)
            return {"status": False, "data": render.home(status="new", started=state.get("started"))}
        else:
            raise web.seeother("/")
    
    player_name = player_record[0].get("player_name")

    if not player_name:
        if home:
            return {"status":False, "data": render.home(status="onboard", started=state.get("started"), register_id=register_id)}
        else:
            raise web.seeother("/")

    return {"status":True, "data":(register_id, player_name)}


def write_pbm_image(name, data):
    imwrite(name, data, magicnumber="P1")

    with open(name, 'r+') as pbm:
        header = pbm.readline()
        content =  pbm.read().replace("\n", "")
        pbm.seek(0)
        pbm.truncate()
        pbm.write(header)
        pbm.write(content)


def generate_steganograph_image_pair(player_id_pair, dimension_seed, username, password):
    # Text to pixel array
    
    text = f"username: {username}\npassword: {password}"
    padding = 5
    font = ImageFont.truetype("press-2p.ttf", size=10)

    left, top, right, bottom = ImageDraw.Draw(Image.new("1", (0,0))).multiline_textbbox((padding, padding), text, font=font)
    width = right - left
    height = bottom - top

    image = Image.new("1", [dimension_seed + width + padding * 2, dimension_seed + height + padding * 2])
    draw = ImageDraw.Draw(image)
    draw.text((padding, padding), text, fill=1, font=font)

    imagearr = np.asmatrix(image, "int")
    # Seed and xor arrays - this is given to the participants
    seedarr = np.random.randint(2, size=imagearr.shape)
    xorarr = np.bitwise_xor(seedarr, imagearr)

    write_pbm_image(f"images/{player_id_pair[0]}.pbm", seedarr)
    write_pbm_image(f"images/{player_id_pair[1]}.pbm", xorarr)


def validate_creds(creds):
    
    allowed = (admin_username, admin_password)

    auth = re.sub("^Basic ", "", creds)
    username, password = base64.b64decode(auth).decode("ascii").split(":")
    
    return True if (username, password) == allowed else False

def adminauth(web):

    creds = web.ctx.env.get("HTTP_AUTHORIZATION")

    if not creds or not validate_creds(creds):
        web.header("WWW-Authenticate", "Basic realm=\"ttf admin\"")
        raise web.unauthorized()
