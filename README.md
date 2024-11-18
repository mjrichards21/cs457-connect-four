This is a simple Connect 4 game implemented using Python and sockets.
**New This Sprint**
1.**Game Logic** Players can take turns dropping tokens into the Connect 4 grid, and a winner will be announced once one player reaches 4 in a row.
2.**Arguments** The client takes two args: -i and -p, corresponding to server IP and port. The Server takes one arg, -p, for port number. Additionally, for both scripts a -h option is available.
   
**How to run:**
1. **Start the server:** Run the `server.py` script, give -p port as arg.
2. **Connect clients:** Run the `client.py` script, give -i address and -p port as args.
3. **Currently the server will only accept two clients, enough to run one game**
4. **Play the game:** Players take turns dropping one token into a grid. The first to get 4 of their tokens in a row, horizontally, vertically, or diagnally, wins!
5. **How To place:** If it is your turn, type "place" followed by a number, from 1 through 7, and if a space is available, your token will drop into the board.

**Current game message protocol:**
1. **place:** Drops a token in the designated column (1-7)
   
**These will be available during final build, once I extend the server to being able to run multiple games:**
1. **join:** Allows the client to join the game
2. **quit:** Allows the client to leave the game

**Technologies used:**
* Python
* Sockets

**Additional resources:**
* [Link to sockets tutorial](https://docs.python.org/3/howto/sockets.html)
