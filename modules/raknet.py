import socket, struct, secrets, time
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
startTime = time.time()
guid = bytes.fromhex(secrets.token_hex(8)) 

o = b''

def offlineMessageID(a):
    o = a

def getUptime():
    """
    Returns the number of seconds since the program started.
    """
    # do return startTime if you just want the process start time
    return struct.pack('>q',round((time.time() - startTime)*1000))

def bind(host, port):
    s.bind((host, port))
    return 1

def ping(id, offline, client, address):
    m = id + client + guid + offline
    print(m)
    s.sendto(m, address)
    return 1

def reply(id, offline, address):
    m = id + offline+ guid
    print(m)
    s.sendto(m, address)
    return 1

def reply2(id, offline, address):
    m = id + offline+ guid
    print(m)
    s.sendto(m, address)
    return 1

def send(id, client, offline, payload, address):
    m = id + client + guid + offline + struct.pack('>H',len(payload)) + payload
    print(m)
    s.sendto(m, address)
    return 1

def recv(byte):
    return s.recvfrom(byte)