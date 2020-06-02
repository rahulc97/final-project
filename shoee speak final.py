#Libraries
import RPi.GPIO as GPIO
import time
import os
import socket

#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 

             
  
# next create a socket object 
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)          
print ("Socket successfully created")
  
# reserve a port on your computer in our 
# case it is 12345 but it can be anything 
port = 12345                
  
# Next bind to the port 
# we have not typed any ip in the ip field 
# instead we have inputted an empty string 
# this makes the server listen to requests  
# coming from other computers on the network 
s.bind(('', port))         
print( "socket binded to port") 
  
# put the socket into listening mode 
s.listen(5)      
print ("socket is listening"  )          
  
# a forever loop until we interrupt it or  
# an error occurs
msg=""
t=True
while t: 
  
   # Establish connection with client. 
   c, addr = s.accept()      
   print ('Got connection from', addr )
   t=False



 
def distance(a1,a2):
    #set GPIO Pins
    GPIO_TRIGGER = a1
    GPIO_ECHO = a2
 
    #set GPIO direction (IN / OUT)
    GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
    GPIO.setup(GPIO_ECHO, GPIO.IN)
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance
 
if __name__ == '__main__':
    try:
        while True:
            dist2 = distance(2,3) #front
            dist1 = distance(27,22) #left
            dist4 = distance(4,17) # 60
            dist3 = distance(10,9) #right
            print("Distance 1=")
            print(dist1)
            print("Distance 2=")
            print(dist2)
            print("Distance 3=")
            print(dist3)
            print("Distance 4=")
            print(dist4)
            if dist4 <= 10 or dist2 <=10:
                if dist1 <=10 and dist3 <=10:
                    cmd_string='espeak -ven+f3 "{0}" >/dev/null'.format("Cannot move")
                    msg="Cannot move"
                    print(cmd_string)
                    os.system(cmd_string)
                elif dist1 >= 10 and dist3 >=10 :
                    cmd_string='espeak -ven+f3 "{0}" >/dev/null'.format("Turn left or right Obstacle infront to you")
                    msg="Turn left or right Obstacle infront to you"
                    print(cmd_string)
                    os.system(cmd_string)
                elif dist1 <= 10 and dist3 >=10:
                    cmd_string='espeak -ven+f3 "{0}" >/dev/null'.format("Turn right Obstacles are in the front and left")
                    msg="Turn right Obstacles are in the front and left"
                    print(cmd_string)
                    os.system(cmd_string)
                elif dist1 >= 10 and dist3 <=10 :
                    cmd_string='espeak -ven+f3 "{0}" >/dev/null'.format("Turn left Obstacles are in the front and right")
                    msg="Turn left Obstacles are in the front and right"
                    print(cmd_string)
                    os.system(cmd_string)
            
            else :
                print("Free to walk")
                msg="Free to walk"
            if(msg!="Free to walk"):
                c.send(msg.encode())
            time.sleep(1)
 
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
    