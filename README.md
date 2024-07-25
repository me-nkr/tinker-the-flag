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
- [ ] create config.py
    - create in root directory
    - structure
    ```py
    config = {
        "arena_password": "<arena_password>",
        "admin_username": "<admin_username>",
        "admin_password": "<admin_password>"
    }
    ```
- [ ] run the game
    - [ ] initialize database
    - [ ] run initgame in background with stdout and stderr to either logfile or /dev/null
    - [ ] run as superuser
- [ ] start web server

Please check the `game.log` file for errors and stuff

## Next steps
- [ ] implement ban and it's sideeffects
    - [ ] ban process
        - as long as they don't violate T&C there is no ban
            - that is if the player left with the blessing of the pair, there is no problem
            - it is encouraged to report the players who leave the team in middle or do somthing not good at any time
    - [ ] what happens when ban before start
        - don't count users who got banned, even it out with user's who's not banned, or volunteers
    - [ ] what happens when ban after start
- [ ] setup a scoreboard
    - [ ] should only show the people who completed the game, this eliminates the problem of incomplete participants getting the clue from here
    - [ ] show pair names and time, but if someone is banned in between, show the standing player only
    - [ ] if both players got banned they won't be shown
- [ ] add options to lock registration and end game
- [ ] gamestart limitation
    - should not start without game being locked
    - should not start without even number of players
    - should not start without all users verified
- [ ] game state limitaions
    - can't submit if game not started or ended
- [ ] add https so others won't be able to intercept communication in between
- [ ] automate possible steps in the above list
    - [ ] create pipes in initgame script
    - [ ] reset database when initializing database, not needed just delete the database file
- [ ] make initgame daemon if needed ( low priority )
    - [ ] move to webserver and initgame directory in-script when starting