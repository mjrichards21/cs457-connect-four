This is a simple Connect 4 game implemented using Python and sockets.

**New This Sprint**
1. **Multiple games** Server can run multiple games with different clients without them interfering with each other
2. **End game state** Server tells client if they won then disconnects the players
   
**How to run:**
1. **Start the server:** Run the `server.py` script, give -p port as arg.
2. **Connect clients:** Run the `client.py` script, give -i address and -p port as args.
3. **Starting a game:** For a client to create a game, they need to type "host", followed by a numeric code
4. **Joining a game:** Once a client creates a game with a code, another client can join it by typing join followed by the same code
5. **Play the game:** Players take turns dropping one token into a grid. The first to get 4 of their tokens in a row, horizontally, vertically, or diagnally, wins!
6. **How To place:** If it is your turn, type "place" followed by a number, from 1 through 7, and if a space is available, your token will drop into the board.

**Current game message protocol:**
1. **place:** Drops a token in the designated column (1-7)
2. **join:** Allows the client to join the game by code
3. **host:** Allows the client to create a game with a code

**Security/Risk Evaluation:**
1. **No encryption:** Requests and responses are not encrypted when being sent, potentially allowing a user to intercept a game code. Some form of encryption could handle this issue.
2. **No client/game limit:** The server allows any number of users to join and any number of games to be played, making it vulnerable to being overwhelmed with some form of dos attack. This could be addressed by adding a limit to the number of clients and a limit to number of requests a client can send in a given time period.
3. **No authentication or verification:** The server does not check who a client is, and there is no verification method such as a password when joining, this could be fixed by having the server need some sort of code in order for the client to join.

**Technologies used:**
* Python
* Sockets

**Additional resources:**
* [Link to sockets tutorial](https://docs.python.org/3/howto/sockets.html)
