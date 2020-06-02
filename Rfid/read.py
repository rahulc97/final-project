from time import sleep
from subprocess import call

import RPi.GPIO as GPIO
#import sys
#from num2words import num2words
from mfrc522 import SimpleMFRC522
reader = SimpleMFRC522()

try:
    while True:
        print("Hold a tag near the reader")
        id, text = reader.read()
        print("ID: %s\nText: %s" % (id,text))
        cmd_beg= 'espeak -s130 ' 
        cmd_end= ' 2>/dev/null' # To dump the std errors to /dev/null

        #cmd_beg= 'espeak '
        #cmd_end= ' | aplay /home/pi/Desktop/Text.wav  2>/dev/null' # To play back the stored .wav file and to dump the std errors to /dev/null
        #cmd_out= '--stdout > /home/pi/Desktop/Text.wav ' # To store the voice file

        text = text.replace(' ', '_')

        #Calls the Espeak TTS Engine to read aloud a Text
        call([cmd_beg+text+cmd_end], shell=True)
        #espeak "Text you wish to hear back" 2>/dev/null
        sleep(1)
except KeyboardInterrupt: #PRESS ctrl+c to execute Keyboard Interrupt
    GPIO.cleanup()
    
