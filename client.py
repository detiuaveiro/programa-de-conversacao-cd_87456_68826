# Echo client program
import socket
import json
import time

HOST = 'localhost'      # Address of the host running the server  
PORT = 5000             # The same port as used by the server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    msg = {"op": "register", "user": "Jasmim"}
    s.sendall(json.dumps(msg).encode('utf-8'))
    time.sleep(1)
    msg = {"op": "message", "data": "Olá bom dia"}
    s.sendall(json.dumps(msg).encode('utf-8'))
    time.sleep(1)
    msg = {"op": "deregister"}
    s.sendall(json.dumps(msg).encode('utf-8'))
