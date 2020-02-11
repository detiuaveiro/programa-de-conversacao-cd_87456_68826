# Echo client program
import socket

HOST = 'localhost'      # Address of the host running the server  
PORT = 5000             # The same port as used by the server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall('Hello, world'.encode('utf-8'))
    data = s.recv(1024)
print(data.decode())
