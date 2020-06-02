import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

try:
    text=input('Enter New Data To Write on Card: ')
    print("Now place tag to write")
    reader.write(text)
    print("Data Written Successfully")
finally:
    GPIO.cleanup()


