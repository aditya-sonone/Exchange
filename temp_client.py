import socket

with open("order.bin", "rb") as f:
    data = f.read()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect(("127.0.0.1", 9000))

s.sendall(data)

s.close()