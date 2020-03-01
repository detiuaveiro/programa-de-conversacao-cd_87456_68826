import datetime
import socket
import json
import time
import selectors
import sys
import fcntl
import os


HOST = 'localhost'      # Address of the host running the server
PORT = 5000             # The same port as used by the server

username = input("name: ")
sock = {}
sel = selectors.DefaultSelector()
# set sys.stdin non-blocking
orig_fl = fcntl.fcntl(sys.stdin, fcntl.F_GETFL)
fcntl.fcntl(sys.stdin, fcntl.F_SETFL, orig_fl | os.O_NONBLOCK)


def send(dest, msg):
    m = json.dumps(msg).replace("\t", "    ") + "\t"
    dest.sendall(m.encode('utf-8'))


def read(conn, mask):
    raw_msg = ""
    while True:
        data = conn.recv(1).decode()
        if data == "\t":
            break
        else:
            raw_msg = raw_msg + data
    msg = json.loads(raw_msg)
    print(f"{msg['sender']}: {msg['data']}")


def got_keyboard_data(stdin, mask):
    data = stdin.read()
    if data in '\r\n':
        sys.exit(0)
    now = datetime.datetime.now()
    timestamp = str(now.strftime("%Y-%m-%d %H:%M"))
    data[:-1]
    data = timestamp + " - " + data
    msg = {"op": "message", "data": data[:-1]}
    send(sock, msg)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.setblocking(False)
    sel.register(s, selectors.EVENT_READ, read)
    sel.register(sys.stdin, selectors.EVENT_READ, got_keyboard_data)
    send(s, {"op": "register", "user": username})
    sock = s
    while True:
        events = sel.select()
        for key, mask in events:
            callback = key.data
            callback(key.fileobj, mask)
