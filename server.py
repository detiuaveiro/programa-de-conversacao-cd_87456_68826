# Echo server program
import socket

HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 5000               # Arbitrary non-privileged port
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(1)
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if not data: break
            print("RECV: " + data.decode())
            reply = "ECHO " + data.decode() 
            print("SEND: " + reply)
            conn.sendall(reply.encode('utf-8'))
