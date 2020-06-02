### run this progrm in p3 thonny
### next run server_socket.py in p2 terminal

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


import time
import binascii
import socket
import struct
import sys



# Use a service account
cred = credentials.Certificate('custom-location-fe592-5da198800f20.json')
firebase_admin.initialize_app(cred)
db = firestore.client()
doc_ref = db.collection(u'location').document(u'current_location')

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 10000)
sock.bind(server_address)
sock.listen(1)

unpacker = struct.Struct('f f')

while True:
    print (sys.stderr)
    connection, client_address = sock.accept()
    #try:
    while True:
        data = connection.recv(unpacker.size)
        #print ( binascii.hexlify(data))

        unpacked_data = unpacker.unpack(data)
        lat=unpacked_data[0]
        long=unpacked_data[1]
        
        print(unpacked_data[0],unpacked_data[1])
        doc_ref.set({
                u'latitude': lat,
                u'longitude': long

                })
        print("Successfully updated")
        time.sleep(3)
    
    #finally:
     #   connection.close()