import socket
import threading
import gamestate
import json
import sys
import argparse

connect4 = gamestate.Game()

def start_connections(server, clients):
    client, addr = server.accept()
    clients.append((client, addr))
    threading.Thread(target = handle_connection, args = (client, addr)).start()

def handle_connection(client, addr):
    print("Accepted client", client)
    try:
        while True:
            data = client.recv(1024)
            if not data:
                break
            message = json.loads(data.decode('utf-8'))
            print("Recieved message", message, "from", addr)
            response = process_message(message, addr)
            if (response == connect4.board):
                for cli in clients:
                    cli[0].send(json.dumps(response).encode('utf-8'))
            else:
                client.send(json.dumps(response).encode('utf-8'))
    except KeyboardInterrupt:
        print("caught keyboard interrupt, exiting")
    finally:
        client.close()

def process_message(message, addr):
    try:
        split = message.split()
        action = split[0]
        value = int(split[1])
        if(action == "place"):
            if (connect4.drop_token(value, addr)):
                return connect4.board
            else:
               return "Invalid move"
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
server.listen(2)
clients = []

while len(clients) < 2:
    start_connections(server, clients)

connect4.start_game(clients)
print("Server full")