import sys
import socket
import selectors
import traceback
import types

sel = selectors.DefaultSelector()

def accept_wrapper(sock):
    conn, addr = sock.accept()
    print("accepted connection from", addr)
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)


# this routine is called when a client is ready to read or write data

def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)
        if recv_data:
            data.outb += recv_data
        else:
            print("closing connection to", data.addr)
            try:
                sel.unregister(sock)
            except Exception as e:
                print(
                    f"error: selector.unregister() exception for",
                    f"{data.addr}: {repr(e)}",
                )
            try:
                sock.close()
            except OSError as e:
                print(
                    f"error: socket.close() exception for",
                    f"{data.addr}: {repr(e)}",
                    )
            finally:
                # Delete reference to socket object for garbage collection
                sock = None
    if mask & selectors.EVENT_WRITE:
        if data.outb:
            print("Sending response to", data.addr)
            sent = sock.send(b"This is the server's response")
            data.outb = data.outb[sent:]

if len(sys.argv) != 3:
    print("usage:", sys.argv[0], "<host> <port>")
    sys.exit(1)

host, port = sys.argv[1], int(sys.argv[2])
    

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
                accept_wrapper(key.fileobj)
            else:
                try:
                    service_connection(key, mask)
                except Exception:
                    print(
                        "main: error: exception for",
                        f"{key.data.addr}:\n{traceback.format_exc()}",
                    )
except KeyboardInterrupt:
    print("caught keyboard interrupt, exiting")
finally:
    sel.close()