def main():
    import time, os, sys, socket, threading, struct, binascii,secrets
    import modules.raknet as raknet
    os.system('cls')
    startTime = time.time()

    class bcolors:
        HEADER = '\033[95m'
        OKBLUE = '\033[94m'
        OKCYAN = '\033[96m'
        OKGREEN = '\033[92m'
        WARNING = '\033[93m'
        FAIL = '\033[91m'
        ENDC = '\033[0m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'


    version = '1.19.1'

    def printf(a):
        b = time.time() - startTime
        print(f"{bcolors.OKBLUE}[{b}] {bcolors.ENDC}{a}{bcolors.ENDC}")

    directory = dir_list = os.listdir('plugins')
    c = 0
    printf(f'Importing Plugins...')
    while c < len(directory):
        d = directory[c].replace('.py', '')
        exec(f'import plugins.{d}')
        c += 1


    listener = b'06705523625395936369'

    def resetSeed():
        num = ['06','70','55','23','62','69','63','59','93','53']
        global listener
        listener = ''.join(secrets.choice(num) for i in range(10))

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    localhost = socket.gethostbyname(socket.gethostname())

    primes = [11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97]

    connections = []

    def ping():
        printf(f'{bcolors.OKBLUE}Server opened to LAN')
        while 1:
            raknet.ping(b'\x01', b'\x00\xff\xff\x00\xfe\xfe\xfe\xfe\xfd\xfd\xfd\xfd\x12\x34\x56\x78', raknet.getUptime(), (localhost, 19132))
            time.sleep(1)

    def serverIndex():
        printf("Server Started")

    def web():
        import webpage
        printf("Started Webserver")

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
        printf(f"Supported IPV4 port: {port}")

        threads = int(keys["max-threads"])

        i = 0
        t = threading.Thread(target=serverIndex)
        #t.start()
        w = threading.Thread(target=web)
        #w.start()
        d = threading.Thread(target=ping)
        # d.start()

        motd = str(keys["server-name"])
        name = str(keys["level-name"])
        gamemode = str(keys["gamemode"]).capitalize()

        try:
            raknet.bind('', port)
        except ValueError:
            printf(f"{bcolors.WARNING}The server couldn't be started. You may have another server running on the same port, or you might need to change your firewall settings.")
            sys.exit()

        printf(f"{bcolors.OKGREEN}Server Started")
        players = 0
        playerInfo = {}
        while 1:
            message, address = raknet.recv(2048)
            packetID = message[0]

            print(message)

            if packetID == 1: # When a client pings the server
                payload = bytes(f'MCPE;{motd};527;{version};{players};{max};{listener};{name};{gamemode};1;{port};{port};', 'utf-8')
                raknet.pong(message[1:9], b'\x00\xff\xff\x00\xfe\xfe\xfe\xfe\xfd\xfd\xfd\xfd\x12\x34\x56\x78', payload, address)


            elif packetID == 5: # Open connection request

                raknet.reply(b'\x00\xff\xff\x00\xfe\xfe\xfe\xfe\xfd\xfd\xfd\xfd\x12\x34\x56\x78', address)
            elif packetID == 7:

                playerGuid = message[17:]
                playerInfo.update({playerGuid: address})
                raknet.reply2(b'\x00\xff\xff\x00\xfe\xfe\xfe\xfe\xfd\xfd\xfd\xfd\x12\x34\x56\x78', address)

            elif len(message) > 8:
                if message[10] == 9:
                    raknet.accept(address)

if __name__ == "__main__":
    main()
