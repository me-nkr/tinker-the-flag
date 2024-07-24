# Tinker The Flag

This is the pilot challenge created for ttf

## Steps to take to setup the server
- [ ] create user gamemaster
    - [ ] move gamemaster's home to /home/control
    - [ ] restrict permissions for all available directories to secure the server
    - [ ] /home/control only accessible for gamemaster drwx------ gamemaster gamemaster
    - [ ] all in /home/control also accessible for gamemaster only
- [ ] install dependencies
    - [ ] python3
    - [ ] pip3
- [ ] clone challenge code
- [ ] create message pipes
    - [ ] /home/control/ttfmessageinpipe
    - [ ] /home/control/ttfmessageoutpipe
- [ ] install server dependencies
    - [ ] create venv (env/)
    - [ ] install reqirements in venv
- [ ] run the game
    - [ ] initialize database
    - [ ] run initgame in background with stdout and stderr to either logfile or /dev/null
    - [ ] run as superuser
- [ ] start web server

## Next steps
- [ ] automate possible steps in the above list
- [ ] send logs to proper logfiles
- [ ] setup a scoreboard
    - [ ] should only show the people who completed the game, this eliminates the problem of incomplete participants getting the clue from here
- [ ] make initgame daemon if needed ( low priority )
- [ ] update hardcoded stuff in the whole codebase
- [ ] create pipes in initgame script
- [ ] shut server with error if any of the following is ready
    - [ ] pipes
    - [ ] db
- [ ] move to webserver and initgame directory in-script when starting
