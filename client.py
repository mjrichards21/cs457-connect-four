import socket
import threading
import sys
import json

def handle_connection(client):
    try:
        while True:
            data = client.recv(1024)
            if not data:
                break
            message = json.loads(data.decode('utf-8'))
            print("Recieved message", message, "from server")
    except KeyboardInterrupt:
        print("caught keyboard interrupt, exiting")
    finally:
        client.close()

if len(sys.argv) != 3:
    print("usage:", sys.argv[0], "<host> <port>")
    sys.exit(1)

host, port = sys.argv[1], int(sys.argv[2])
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
