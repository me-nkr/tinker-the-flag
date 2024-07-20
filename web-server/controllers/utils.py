from PIL import Image, ImageDraw, ImageFont
from netpbmfile import imwrite
import numpy as np

def userauth(web, db, render, state, home=False):

    register_id = web.cookies().get("register_id")
    
    player_record = db.where("scoreboard", what="player_name", player_id=register_id).list()
    
    if not register_id or len(player_record) < 1:
        if home:
            web.setcookie("register_id", None, expires=0)
            return {"status": False, "data": render.home(status="new", started=state.started)}
        else:
            raise web.seeother("/")
    
    player_name = player_record[0].get("player_name")

    if not player_name:
        if home:
            return {"status":False, "data": render.home(status="onboard", started=state.started, register_id=register_id)}
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
