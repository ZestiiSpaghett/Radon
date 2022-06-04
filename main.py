import time, os, sys, socket, threading, struct, binascii,secrets, random, keyboard
import modules.raknet as raknet
#     from plugins import *

seed = b'06705523625395936369'

keyboard.add_hotkey('a', lambda: resetSeed())

def resetSeed():
    global seed
    seed = ''.join(secrets.choice(num) for i in range(20))

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

localhost = socket.gethostbyname(socket.gethostname())

os.system('cls')
num = ['0','1','2','3','4','5','6','7','8','9']

primes = [11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97]

connections = []

def ping():
    print('Server opened to LAN')
    while 1:
        raknet.ping(b'\x01', b'\x00\xff\xff\x00\xfe\xfe\xfe\xfe\xfd\xfd\xfd\xfd\x12\x34\x56\x78', raknet.getUptime(), (localhost, 19132))
        time.sleep(1)
        
def serverIndex():
    print("Server Started")

def web():
    import webpage
    print("Started Webserver")
    
if __name__ == "__main__":

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
    #d.start()

    motd = str(keys["server-name"])
    name = str(keys["level-name"])
    gamemode = str(keys["gamemode"]).capitalize()

    raknet.bind('', port)
    print("Server Started")
    players = 0
    playerInfo = {}
    while 1:
        message, address = raknet.recv(2048)
        packetID = message[0]
        print('\n')
        print(message)
        if packetID == 1: # When a client pings the server
            payload = bytes(f'MCPE;{motd};503;1.18.32;{players};{max};{seed};{name};{gamemode};1;{port};{port};', 'utf-8')
            raknet.send(b'\x1c', message[1:9], b'\x00\xff\xff\x00\xfe\xfe\xfe\xfe\xfd\xfd\xfd\xfd\x12\x34\x56\x78', payload, address)
    

        elif packetID == 5: # Open connection request
            raknet.reply(b'\x06', b'\x00\xff\xff\x00\xfe\xfe\xfe\xfe\xfd\xfd\xfd\xfd\x12\x34\x56\x78', address)
        elif packetID == 7:
            playerGuid = message[17:]
            playerInfo.update({playerGuid: address})
            raknet.reply2(b'\x08', b'\x00\xff\xff\x00\xfe\xfe\xfe\xfe\xfd\xfd\xfd\xfd\x12\x34\x56\x78', address)
