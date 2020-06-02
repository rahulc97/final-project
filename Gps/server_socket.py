### first run cli_soc.py  progrm in p3 thonny
### next run server_socket.py in p2 terminal
import binascii
import socket
import struct
import sys


import serial
import time
import string
import pynmea2


# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 10000)
sock.connect(server_address)
while True:
    port="/dev/ttyAMA0"
    ser=serial.Serial(port, baudrate=9600, timeout=0.5)
    dataout = pynmea2.NMEAStreamReader()
    newdata=ser.readline()
    if newdata[0:6] == "$GPRMC":
        print("hasi")
        newmsg=pynmea2.parse(newdata)
        lat=newmsg.latitude
        lng=newmsg.longitude
        gps = "Latitude=" + str(lat) + "and Longitude=" + str(lng)
        print(gps)
        i=0
        while i<1000000:
           i+=1
        values = (lat,lng)
        packer = struct.Struct('f f')
        packed_data = packer.pack(*values)

        #try:
            
        # Send data
        print >>sys.stderr, 'sending "%s"' % binascii.hexlify(packed_data), values
        sock.sendall(packed_data)

       # finally:
           # print >>sys.stderr, 'closing socket'
            #sock.close()
