import sys
import socket
import selectors
import traceback
import types
import libclient
sel = selectors.DefaultSelector()

def create_request(action, value):
    if action == "place" or action == "join" or action == "quit":
        return dict(
            type="text/json",
            encoding="utf-8",
            content=dict(action=action, value=value),
        )
    else:
        return dict(
            type="binary/custom-client-binary-type",
            encoding="binary",
            content=bytes(action + value, encoding="utf-8"),
        )

def start_connections(host, port, request):
    server_addr = (host, port)
    print("starting connection to", server_addr)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setblocking(False)
    sock.connect_ex(server_addr)
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    message = libclient.Message(sel, sock, server_addr, request)
    sel.register(sock, events, data= message)


if len(sys.argv) != 5:
    print("usage:", sys.argv[0], "<host> <port> <action> <value>")
    sys.exit(1)


host, port = sys.argv[1], int(sys.argv[2])
action, value = sys.argv[3], sys.argv[4]
request = create_request(action, value)
start_connections(host, port, request)

# the event loop

try:
    while True:
        events = sel.select(timeout=1)
        if events:
            for key, mask in events:
                message = key.data
                try:
                    message.process_events(mask)
                except Exception:
                    print(
                    "main: error: exception for",
                    f"{message.addr}:\n{traceback.format_exc()}",
                )
            if not sel.get_map():
                break
except KeyboardInterrupt:
    print("caught keyboard interrupt, exiting")
finally:
    sel.close()