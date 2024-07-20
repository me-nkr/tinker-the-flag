#!/usr/bin/python

import os, shutil, subprocess, pwd, json, random, grp

inpipe="/home/control/ttfmessageinpipe"
outpipe="/home/control/ttfmessageoutpipe"

response = ""

while True:
    with open(inpipe, "r") as call:
        for command in call:
            if command:

                print(command)

                if command == "start":

                    try:
                        if grp.getgrnam("public"):
                            pass
                    except KeyError:
                        subprocess.run(["groupadd", "public"])

                    if os.path.exists("/home/lobby"):
                        shutil.rmtree("/home/lobby")

                    os.mkdir("/home/lobby", 0o750)
                    os.chown("/home/lobby", pwd.getpwnam("gamemaster").pw_uid, grp.getgrnam("public").gr_gid)

                    subprocess.run(["install",
                                   "-o", "gamemaster",
                                   "-g", "public",
                                   "-m", "640",
                                   "-t", "/home/lobby",
                                   "/etc/skel/.bashrc", "/etc/skel/.bash_logout", "/etc/skel/.profile"])

                    with open("/home/lobby/.profile", "a") as profile:
                        profile.write("\nclear\necho \"\\n\\n\\nWelcome to the playground of Tinker The Flag, you are in the lobby\\n\\n\\n\"")

                    subprocess.run(["install",
                                   "-o", "gamemaster",
                                   "-g", "public",
                                   "-m", "600",
                                   "/dev/null", "/home/lobby/.hushlogin"])

                    # create user arena with a password
                    
                    try:
                        if pwd.getpwnam("arena"):
                            subprocess.run(["userdel", "arena"])
                    except KeyError:
                        pass
                    finally:
                        arena_pass = subprocess.run(["openssl", "passwd", "thisarenaisofflimits"], capture_output=True, encoding="utf-8").stdout.strip()

                        subprocess.run(["useradd", "-MN",
                                        "-p", arena_pass,
                                        "arena"])

                    # destroy and generate arena
                    
                    if os.path.exists("/home/arena"):
                        shutil.rmtree("/home/arena")

                    os.mkdir("/home/arena", 0o750)
                    os.chown("/home/arena", pwd.getpwnam("gamemaster").pw_uid, grp.getgrnam("public").gr_gid)

                    arena = ""

                    with open("arena.json") as arenadata:
                        arena = json.load(arenadata)

                    for spot in list(arena.keys()):

                        subprocess.run(["install",
                                        "-o", "gamemaster",
                                        "-g", "public",
                                        "-m", "750",
                                        "-d", f"/home/arena/{spot}"])

                        for item in arena[spot]:
                            
                            subprocess.run(["install",
                                            "-o", "arena",
                                            "-g", "gamemaster",
                                            "-m" "060",
                                            "/dev/null", f"/home/arena/{spot}/{item}"])

                        # clear images directory
                        if os.path.exists("/home/control/web-server/images"):
                            shutil.rmtree("/home/control/web-server/images")

                        os.mkdir("/home/control/web-server/images", 0o700)
                        os.chown("/home/control/web-server/images", pwd.getpwnam("gamemaster").pw_uid, grp.getgrnam("gamemaster").gr_gid)
                        
                    with open(outpipe, "w") as res:
                        res.write("done")
                        res.flush()

                elif command == "end":
                    with open(outpipe, "w") as res:
                        res.write("done")
                        res.flush()
                        exit()
                else:
                        # input is username:password:flag
                        username, password, flag = command.split(":")

                        try:
                            if pwd.getpwnam(username):
                                subprocess.run(["userdel", username])
                        except KeyError:
                            pass
                        encrypted_password = subprocess.run(["openssl", "passwd", password], capture_output=True, encoding="utf-8").stdout.strip()

                        create_user_action = subprocess.run(["useradd", "-MN",
                                   "-d", "/home/lobby",
                                   "-g", "public",
                                   "-s", "/bin/bash",
                                   "-p", encrypted_password,
                                   username])

                        if create_user_action.returncode == 0:

                            flagfile = ""
                            used_files = [] 

                            while True:

                                random_dir = random.choice(os.listdir("/home/arena"))
                                random_files = os.listdir("/home/arena" + "/" + random_dir)

                                for file in used_files:
                                    _, _, _, dir, filename = file.split("/")
                                    if random_dir == dir:
                                        random_files.remove(filename)

                                flagfile = "/home/arena" + "/" + random_dir + "/" + random.choice(random_files)

                                if pwd.getpwuid(os.stat(flagfile).st_uid).pw_name == "arena":
                                    with open(flagfile, "w") as file:
                                        file.write(flag + "\n")

                                    os.chown(flagfile, pwd.getpwnam(username).pw_uid, -1)
                                    os.chmod(flagfile, 0o460)
                                    break
                                else:
                                    used_files.append(flagfile)

                            with open(outpipe, "w") as res:
                                res.write("done")
                                res.flush()

                        else:
                            with open(outpipe, "w") as res:
                                res.write("can't create user")
                                res.flush()

                        # use that to create user and flag file
                
