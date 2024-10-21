import sys
import socket
import selectors
import traceback
import types
import libserver
import gamestate

sel = selectors.DefaultSelector()

def accept_wrapper(sock, game):
    conn, addr = sock.accept()
    print("accepted connection from", addr)
    conn.setblocking(False)
    message = libserver.Message(sel, conn, addr, game)
    sel.register(conn, selectors.EVENT_READ, data=message)


if len(sys.argv) != 3:
    print("usage:", sys.argv[0], "<host> <port>")
    sys.exit(1)

host, port = sys.argv[1], int(sys.argv[2])
game = gamestate.Game()

# set up the listening socket and register it with the SELECT mechanism

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.bind((host, port))
lsock.listen()
print("listening on", (host, port))
lsock.setblocking(False)
sel.register(lsock, selectors.EVENT_READ, data=None)

# the main event loop
try:
    while True:
        events = sel.select(timeout=None)
        for key, mask in events:
            if key.data is None:
                accept_wrapper(key.fileobj, game)
            else:
                message = key.data
                try:
                    message.process_events(mask)
                except Exception:
                    print(
                        "main: error: exception for",
                        f"{key.data.addr}:\n{traceback.format_exc()}",
                    )
except KeyboardInterrupt:
    print("caught keyboard interrupt, exiting")
finally:
    sel.close()