import socket   # import socket module 
 
HOST,PORT = '',80
 
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
s.bind((HOST,PORT))
s.listen(1)

while True:
    connection,address = s.accept()
    req = connection.recv(1024).decode('utf-8')
    print(req) # Get print in our python console.
    connection.send('Hello world!'.encode('utf-8'))
    
    string_list = req.split(' ')     # Split request from spaces
 
    method = string_list[0] # First string is a method
    requesting_file = string_list[1] #Second string is reque

    myfile = requesting_file.split('?')[0] # After the "?" symbol not relevent here       
     
    myfile = myfile.lstrip('/')
    if(myfile == '/'):
        myfile = 'index.html'

    try:
        header = 'HTTP/1.1 200 OK\n'
        file = open("{myfile}",'rb')
        response = file.read()
        file.close()

        if(myfile.endswith(".jpg")):
            mimetype = 'image/jpg'
        elif(myfile.endswith(".css")):
            mimetype = 'text/css'
        else:
            mimetype = 'text/html'
            
        response = file.read()
        file.close()
 
        header += 'Content-Type: '+str(mimetype)+'\n\n'
 
    except Exception as e:
        header = 'HTTP/1.1 404 Not Found\n\n'
        response = '<html><body><h3>Error 404: File not found</h3><p>Python HTTP Server</p></body></html>'.encode('utf-8')

    final_response = header.encode('utf-8')
    final_response += response
    connection.send(final_response)
    connection.close()