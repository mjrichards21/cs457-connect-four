import sys
import socket
import selectors
import types

sel = selectors.DefaultSelector()

# this routine is called to create each of the many ECHO CLIENTs we want to create

def start_connections(host, port):
    server_addr = (host, port)
    print("starting connection to", server_addr)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setblocking(False)
    sock.connect_ex(server_addr)
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    data = types.SimpleNamespace(
        recv_total=0,
        message= [b"This is a request"],
        outb=b"",
    )
    sel.register(sock, events, data=data)

# this routine is called when a client triggers a read or write event

def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)
        if recv_data:
            print("received", repr(recv_data))
            data.recv_total += len(recv_data)
            print("closing connection")
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if not data.outb and data.message:
            data.outb = data.message.pop(0)
        if data.outb:
            print("sending", repr(data.outb), "to connection")
            sent = sock.send(data.outb)
            data.outb = data.outb[sent:]


if len(sys.argv) != 3:
    print("usage:", sys.argv[0], "<host> <port>")
    sys.exit(1)


host, port = sys.argv[1], int(sys.argv[2])
start_connections(host, port)

# the event loop

try:
    while True:
        events = sel.select(timeout=1)
        if events:
            for key, mask in events:
                service_connection(key, mask)
        if not sel.get_map():
            break
except KeyboardInterrupt:
    print("caught keyboard interrupt, exiting")
finally:
    sel.close()