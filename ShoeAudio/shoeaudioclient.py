import socket               # Import socket module
from subprocess import call

s = socket.socket()         # Create a socket object
host =  '192.168.43.35' # Get local machine name
port = 12345                # Reserve a port for your service.
print(host)
s.connect((host, port))
while True:
    msg=s.recv(1024).decode()
    print(msg)
    cmd_beg= 'espeak -s130 ' 
    cmd_end= ' 2>/dev/null'
    text = msg.replace(' ', '_')

    #Calls the Espeak TTS Engine to read aloud a Text
    call([cmd_beg+text+cmd_end], shell=True)
    
s.close()    