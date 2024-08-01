# Tinker The Flag

This is the pilot challenge created for ttf

## Steps to take to setup the server
- [ ] create user gamemaster
    - [ ] move gamemaster's home to /home/control
    - [ ] restrict permissions for all available directories to secure the server
    - [ ] /home/control only accessible for gamemaster drwx------ gamemaster gamemaster
    - [ ] all in /home/control also accessible for gamemaster only
- [ ] install dependencies
    - [ ] python3.10
    - [ ] python3.10-venv
    - [ ] python3-pip
    - [ ] python-is-python3
- [ ] clone challenge code
- [ ] create message pipes
    - [ ] /home/control/tinkertheflag/ttfmessageinpipe
    - [ ] /home/control/tinkertheflag/ttfmessageoutpipe
- [ ] install server dependencies
    - [ ] create venv (env/)
    - [ ] install reqirements in venv
- [ ] generate ssl key pair
    - `openssl req -x509 -newkey rsa:4098 -keyout privatekey.pem -out sslcert.pub -days 365 -noenc`
- [ ] create config.py
    - create in root directory
    - structure
    ```py
    config = {
        "arena_password": "<arena_password>",
        "admin_username": "<admin_username>",
        "admin_password": "<admin_password>",
        "ssl_private_key": "../privatekey.pem",
        "ssl_cert": "../sslcert.out",
    }
    ```
- [ ] run the game
    - [ ] initialize database
    - [ ] run initgame in background with stdout and stderr to either logfile or /dev/null
    - [ ] run as superuser
- [ ] start web server

Please check the `game.log` file for errors and stuff

- [-] redirect http request to https
- [ ] automate possible steps in the above list
    - [ ] create pipes in initgame script
    - [ ] reset database when initializing database, not needed just delete the database file
- [ ] make initgame daemon if needed ( low priority )
    - [ ] move to webserver and initgame directory in-script when starting

## Test Observations
- [ ] find pbm file viewer for windows
    - it's hard, the closest I can get is filehelper.com, but still with edge smoothening
    - bitberry file opener does the job well
- [ ] better clue, or a way for the clue to make sense
