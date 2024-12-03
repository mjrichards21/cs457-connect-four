import socket
import threading
import gamestate
import json
import argparse
import logging

players = {}
games = {}
logging.basicConfig(filename='server.log', level=logging.INFO)

#This function is called when the client request hosts, and creates a game object with a code
def host_game(addr, client, code):
    if(addr not in players and code not in games):
        game = gamestate.Game()
        games[code] = game
        player = game.add_player(addr, client, code)
        players[addr] = player
        return True
    return False

#This function is called when the client requests join, and lets the client join the game if they have the code
def join_game(addr, client, code):
    if (code in games and addr not in players and len(games[code].players) < 2):
        game = games[code]
        player = game.add_player(addr, client, code)
        players[addr] = player
        if (len(game.players) == 2):
            game.start_game()
        return True
    return False

#This function is called when there is a winner
def end_game(addr):
    player_addr = []
    for player in players[addr].game.players:
        player_addr.append(player.addr)
        player.client.close()
    for address in player_addr:
        players[addr].game.remove_player(players[addr])
        del players[address]
    game_code_to_delete = None
    for code in games:
        if (len(games[code].players) == 0):
            game_code_to_delete = code
    del games[game_code_to_delete]

#This function is called for each client     
def start_connections(server, clients):
    client, addr = server.accept()
    clients.append((client, addr))
    threading.Thread(target = handle_connection, args = (client, addr)).start()

#This function handles client connections
def handle_connection(client, addr):
    print("Accepted client", client)
    logging.info(f"Accepted client: {client}")
    try:
        while True:
            data = client.recv(1024)
            if not data:
                break
            message = json.loads(data.decode('utf-8'))
            print("Recieved message", message, "from", addr)
            logging.info(f"{client} message: {message}")
            response = process_message(message, addr, client)
            if (addr in players and response == players[addr].game.board):
                for player in players[addr].game.players:
                    player.client.send(json.dumps(response).encode('utf-8'))
            elif (response == "You won!"):
                for player in players[addr].game.players:
                    player.client.send(json.dumps(players[addr].game.board).encode('utf-8'))
                client.send(json.dumps(response).encode('utf-8'))
                end_game(addr)
            else:
                client.send(json.dumps(response).encode('utf-8'))
    except Exception:
        print("Client Disconnected")
    finally:
        client.close()

#This function processes the client message
def process_message(message, addr, client):
    try:
        split = message.split()
        action = split[0]
        value = int(split[1])
        if(action == "place"):
            game = players[addr].game
            game_info = game.drop_token(value, addr)
            token_dropped = game_info[0]
            is_winner = game_info[1]
            if (token_dropped and not is_winner):
                return game.board
            elif (token_dropped and is_winner):
                return "You won!"
            else:
                return "Invalid move"
        elif(action == "host"):
            if(host_game(addr, client, value)):
                return "Game has been created"
            else: 
                return "Unable to create game"
        elif(action == "join"):
            if(join_game(addr, client, value)):
                return "Game has been joined"
            else:
                return "Unable to join game"
        else:
            return "Unknown request"
    except Exception:
        return "Unknown request"

parser = argparse.ArgumentParser(
                    prog='server',
                    description='To run, supply a port number',
                    )
parser.add_argument('-p', '--port', required = True)
args = vars(parser.parse_args())
host = '0.0.0.0'
port = int(args['port'])
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()
clients = []

while True:
    start_connections(server, clients)
