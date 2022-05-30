import socket
rak = b'\x34\x56\x78\x00\x05'
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def bind(host, port):
    s.bind((host, port))
    return 1

def send(id, payload, address):
    s.sendto(id + rak + payload, address)
    return 1

def recv(byte):
    return s.recvfrom(byte)