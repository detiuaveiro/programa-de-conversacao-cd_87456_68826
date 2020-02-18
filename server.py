# Echo server program
import socket
import selectors
import json

HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 5000               # Arbitrary non-privileged port
sel = selectors.DefaultSelector()

clients = []


def accept(sock, mask):
    print("connection accepted")
    conn, addr = sock.accept()
    conn.setblocking(False)
    sel.register(conn, selectors.EVENT_READ, read)  # regista nova socket


def read(conn, mask):
    raw_msg = ""
    while True:
        data = conn.recv(1).decode()
        if data == "\t":
            break
        else:
            raw_msg = raw_msg + data

    msg = json.loads(raw_msg)
    print(msg)
    print(raw_msg)
    if msg['op'] == "register":
        register(conn, msg['user'])
    if msg['op'] == "message":
        forward(conn, msg['data'])
    if msg['op'] == "deregister":
        deregister(conn)


def send(dest, msg):
    m = json.dumps(msg).replace("\t", "    ") + "\t"
    dest.sendall(m.encode('utf-8'))


def register(conn, user):
    clients.append({"connection": conn, "username": user})
    print(f"user '{user}' with connection {conn.getpeername()} was registered")


def forward(source, msg):
    src_addr = source.getpeername()
    # get username
    print(clients)
    for c in clients:
        if c["connection"] == source:
            src_username = c['username']
            break
    print(f"recieved message '{msg}' from {src_username} ")
    # forward para todos os restantes clients
    frw = {"op": "message", "sender": src_username, "data": msg}
    for c in clients:
        if c['connection'] is source:
            send(c['connection'], frw)
            print(f"forwarded message to {src_username}")


def deregister(conn):
    for c in clients:
        if c["connection"] == conn:
            clients.remove(c)
            print(f"user {c['username']} was deregistered")
            sel.unregister(conn)
    conn.close()


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(100)
    s.setblocking(False)
    sel.register(s, selectors.EVENT_READ, accept)

    while True:
        events = sel.select()
        for key, mask in events:
            callback = key.data
            callback(key.fileobj, mask)
