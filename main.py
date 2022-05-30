import time, os, sys, socket, threading, struct, binascii,secrets, random

#     from plugins import *

localhost = socket.gethostbyname(socket.gethostname())
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
rak = b'\x00\xff\xff\x00\xfe\xfe\xfe\xfe\xfd\xfd\xfd\xfd\x12\x34\x56\x78\x00\x5c'
# Combination above sets the protocol to RakNet

os.system('cls')
num = ['0','1','2','3','4','5','6','7','8','9']

primes = [11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97]

connections = []

def pack():
    return packetID + rak + bytes(str(package), 'utf-8')

def ping():
    while 1:
        time.sleep(1)

        #s.sendto(sessionID, (localhost, 19132))
    

def int2bytes(i):
    hex_string = '%x' % i
    n = len(hex_string)
    return binascii.unhexlify(hex_string.zfill(n + (n & 1)))

def send(payload):
    s.sendto(payload, address)
    pass

def sendTo(player, payload):
    load = int(payload, 16)
    pass

def serverIndex():
    print("Server Started")

def web():
    import webpage
    print("Started Webserver")
    
if __name__ == "__main__":

    print("██████╗  █████╗ ██████╗  ██████╗ ███╗   ██╗\n██╔══██╗██╔══██╗██╔══██╗██╔═══██╗████╗  ██║\n██████╔╝███████║██║  ██║██║   ██║██╔██╗ ██║\n██╔══██╗██╔══██║██║  ██║██║   ██║██║╚██╗██║\n██║  ██║██║  ██║██████╔╝╚██████╔╝██║ ╚████║\n╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝  ╚═════╝ ╚═╝  ╚═══╝")

    separator = "="
    keys = {}
    with open('server.properties') as f:
        for line in f:
            if separator in line:

                # Find the name and value by splitting the string
                name, value = line.split(separator, 1)

                # Assign key value pair to dict
                # strip() removes white space from the ends of strings
                keys[name.strip()] = value.strip()

    #print(keys)

    port = int(keys["port"])
    max = int(keys["max-players"])
    print("Supported IPV4 port: "+str(port))

    print("Starting Server")

    threads = int(keys["max-threads"])

    i = 0
    t = threading.Thread(target=serverIndex)
    #t.start()
    w = threading.Thread(target=web)
    #w.start()
    d = threading.Thread(target=ping)
    d.start()

    motd = str(keys["server-name"])
    name = str(keys["level-name"])
    gamemode = str(keys["gamemode"])

    s.bind(('', port))
    print("Server Started")
    players = 0
    while 1:
        message, address = s.recvfrom(2048)
        id = message[0]
        print(message)
        if id == 1:
            sessionID = ''.join(secrets.choice(num) for i in range(20))
            package = f'MCPE;{motd};503;1.18.32;{players};{max};{sessionID};{name};{gamemode.capitalize()};0;{port};{port+1}'
            packetID = b'\x1c\x00\x00\x00\x00\x00\x00' + message[8:9] + b'\x84\xad\x43\xa1\x4e\xc2\x4e\xb1'
            payload = pack()

            print(payload)
            s.sendto(payload , address)
            
        if id == 28:

            print(payload)
            print('\n')
            s.sendto(payload , address)
            