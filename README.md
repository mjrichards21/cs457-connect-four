This is a simple Connect 4 game implemented using Python and sockets.
**New This Sprint**
1. **Gamestate**: Once two clients connect to server game will be initilized.
2. **Player Turn**: Game will only drop player token if it is that player's turn.
3. **Player Token**: Player 1 has an "O" token, player 2 uses "X".
   
**How to run:**
1. **Start the server:** Run the `server.py` script, give host and port as args.
2. **Connect clients:** Run the `client.py` script, give host and port as args.
3. **Play the game:** Players take turns dropping one token into a grid. The first to get 4 of their tokens in a row, horizontally, vertically, or diagnally, wins! (Game not yet implemented)

**Current game message protocol:**
1. **join:** Allows the client to join the game, currently just increments player count of game
2. **quit:** Allows the client to leave the game, currently just decrements player count of game
3. **place:** Drops a token in the designated column (1-7)

**Technologies used:**
* Python
* Sockets

**Additional resources:**
* [Link to sockets tutorial](https://docs.python.org/3/howto/sockets.html)
