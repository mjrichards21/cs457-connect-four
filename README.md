This is a simple Connect 4 game implemented using Python and sockets.

**New This Sprint:**
1. **Multiple games** Server can run multiple games with different clients without them interfering with each other
2. **End game state** Server tells client if they won then disconnects the players
   
**How to run:**
1. **Start the server:** Run the `server.py` script, give -p port as arg.
2. **Connect clients:** Run the `client.py` script, give -i address and -p port as args.
3. **Starting a game:** For a client to create a game, they need to type "host", followed by a numeric code
4. **Joining a game:** Once a client creates a game with a code, another client can join it by typing join followed by the same code
5. **Play the game:** Players take turns dropping one token into a grid. The first to get 4 of their tokens in a row, horizontally, vertically, or diagnally, wins!
6. **How To place:** If it is your turn, type "place" followed by a number, from 1 through 7, and if a space is available, your token will drop into the board. The host player will always start first.

**Current game message protocol:**
1. **place:** Drops a token in the designated column (1-7)
2. **join:** Allows the client to join the game by code
3. **host:** Allows the client to create a game with a code

**Security/Risk Evaluation:**
1. **No encryption:** Requests and responses are not encrypted when being sent, potentially allowing a user to intercept a game code. Some form of encryption could handle this issue.
2. **No client/game limit:** The server allows any number of users to join and any number of games to be played, making it vulnerable to being overwhelmed with some form of dos attack. This could be addressed by adding a limit to the number of clients and a limit to number of requests a client can send in a given time period.
3. **No authentication or verification:** The server does not check who a client is, and there is no verification method such as a password when joining, this could be fixed by having the server need some sort of code in order for the client to join.

**Roadmap:**
If I were to continue the project, the next thing I would add would definitely be some form of UI for the clients. This is because I think the current method of starting and playing a game of connect 4 could be much more streamlined if a client didn't have to type what they wanted to do for each turn. In addition, I would probably also add a new message option "help", which when sent to the server, will return instructions to the client about how to start and play a game. Alternatively, I could instead include it as a part of client UI if it seems more convenient. I would also like to add the ability for players to set their own usernames and chat with each other. 

**Retrospective:**
Overall, I'm quite happy with how my project turned out. The game mechanics and method in which games are handled I thought went pretty well. The game is accurate to Connect 4 and the server can properly keep track of multiple games happening at once. I think the code is also well modularized and easy to read and explain. I am also quite happy with my solution on running multiple games, having games needing a code. I'm also overall happy with my implementation of error handling in the game, as I think most if not all of the common errors to occur are caught. For what could be improved on, I think I could've started working a lot earlier. While I'm happy with the final product, for the first couple of sprints, I was a little behind and unsure of how to implement the client-server architecture. Additionally, I think the UI could be improved. Even without a proper UI, just using text, I think the program could be a lot easier to understand for a client if there was a more informative help message. I also think there are ways of perhaps streamlining the message protocol, or at least making it more clear. I'd also want to have the server provide more feedback to the clients, for example, telling them that a game started and who's turn it is.

**Technologies used:**
* Python
* Sockets

**Additional resources:**
* [Link to sockets tutorial](https://docs.python.org/3/howto/sockets.html)
