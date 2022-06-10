import socket, struct, secrets, time, zlib
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
startTime = time.time()
guid = bytes.fromhex(secrets.token_hex(8)) 

# Custom RakNet module developed by https://github.com/ZestiiSpaghett

localhost = socket.gethostbyname(socket.gethostname())

o = b''

def ack(min, max, address):
    if min == max:
        a = struct.pack('H', min) + b'\x00'
        m = b'\xc0\x00\x01\x01' + a
    else:
        a = struct.pack('H', min) + b'\x00'
        b = struct.pack('H', max) + b'\x00'
        m = b'\xc0\x00\x01\x00' + a + b
    s.sendto(m, address)

def ipToBytes(a):
    c = a.split('.')
    print(a)
    b = struct.pack('B B B B', 255 - int(c[0]), 255 - int(c[1]), 255 - int(c[2]), 255 - int(c[3]))
    print(b)
    return b

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

def recv(byte):
    return s.recvfrom(byte)

def ping(id, offline, client, address):
    m = id + client + guid + offline
    s.sendto(m, address)
    return 1

def pong( client, offline, payload, address ):
    m = b'\x1c' + client + guid + offline + struct.pack('>H',len(payload)) + payload
    s.sendto(m, address)
    return 1

def connectedPong( client, offline, payload, address ):
    m = b'\x1c' + client + guid + offline + struct.pack('>H',len(payload)) + payload
    s.sendto(m, address)
    return 1

def reply( offline, address):
    m = b'\x06' + offline + guid + b'\x00\x05\x78'
    s.sendto(m, address)
    return 1

def reply2( offline, address):
    i, p = address
    i = bytes(map(int, i.split('.')))
    m = b'\x08' + offline + guid + b'\x04' + i + struct.pack('>H', p) + b'\x05\x78\x00'
    s.sendto(m, address)
    return 1

def accept(address):
    s.sendto(b'\xc0\x00\x01\x01\x00\x00\x00', address)
    i, p = address
    print(p)
    a = ipToBytes(i)

    p = struct.pack('>H', p)
    m = b'\x84\x00\x00\x00\x60\x05\xe0\x00\x00\x00\x00\x00\x00\x00\x10\x04'+a+p+b'\x00\x00\x06\x17\x00J\xbc\x00\x00\x00\x00\xfe\x80\x00\x00\x00\x00\x00\x00L\xed\x962g\xc0e(\t\x00\x00\x00\x04?W\xa9\xc5J\xbc\x04\xff\xff\xff\xff\x00\x00\x04\xff\xff\xff\xff\x00\x00\x04\xff\xff\xff\xff\x00\x00\x04\xff\xff\xff\xff\x00\x00\x04\xff\xff\xff\xff\x00\x00\x04\xff\xff\xff\xff\x00\x00\x04\xff\xff\xff\xff\x00\x00\x04\xff\xff\xff\xff\x00\x00\x04\xff\xff\xff\xff\x00\x00\x04\xff\xff\xff\xff\x00\x00\x04\xff\xff\xff\xff\x00\x00\x04\xff\xff\xff\xff\x00\x00\x04\xff\xff\xff\xff\x00\x00\x04\xff\xff\xff\xff\x00\x00\x04\xff\xff\xff\xff\x00\x00\x04\xff\xff\xff\xff\x00\x00\x04\xff\xff\xff\xff\x00\x00\x04\xff\xff\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x96\xaa\x00\x00\x00\x00\x05C\x9ea'
    s.sendto(m, address)
