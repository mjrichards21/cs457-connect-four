import socket
import threading
import sys
import json
import argparse

def print_board(board):
    for row in board:
        print(row)
def handle_connection(client):
    try:
        while True:
            data = client.recv(1024)
            if not data:
                break
            message = json.loads(data.decode('utf-8'))
            if(type(message) is list):
                print_board(message)
            else:
                print("Recieved message", message, "from server")
    except KeyboardInterrupt:
        print("caught keyboard interrupt, exiting")
    finally:
        client.close()

parser = argparse.ArgumentParser(
                    prog='client',
                    description='To run, start the server script then give the ip and port number',
                    )
parser.add_argument('-i', '--ip', required = True)
parser.add_argument('-p', '--port', required = True)
args = vars(parser.parse_args())
host = args['ip']
port = int(args['port'])

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))
threading.Thread(target = handle_connection, args = (client,)).start()
try:
    while True:
        message = input("Enter a message(action, value): ")
        client.send(json.dumps(message).encode('utf-8'))
except KeyboardInterrupt:
    print("caught keyboard interrupt, exiting")
finally:
    client.close()
