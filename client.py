import socket
import threading
import json
import argparse

#This function prints the connect 4 board if the server returns it
def print_board(board):
    col_nums = ['1', '2', '3', '4', '5', '6', '7']
    print()
    print(col_nums)
    for row in board:
        print(row)

#This function handles the client connection with the server
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
    except Exception:
        print("Client socket closed")
    finally:
        client.close()

parser = argparse.ArgumentParser(
                    prog='client',
                    description='To run, start the server script then give the ip and port number, valid actions are host, join, and place',
                    )
parser.add_argument('-i', '--ip', required = True)
parser.add_argument('-p', '--port', required = True)
args = vars(parser.parse_args())
host = args['ip']
port = int(args['port'])

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))
threading.Thread(target = handle_connection, args = (client,)).start()

#Main event loop
try:
    while True:
        message = input("What would you like to do (host, join, place), message format:(action, value): ")
        try:
            client.send(json.dumps(message).encode('utf-8'))
        except Exception:
            print("Disconnected from server")
            break
except KeyboardInterrupt:
    print("caught keyboard interrupt, exiting")
finally:
    client.close()
