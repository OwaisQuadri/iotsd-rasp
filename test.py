import RPi.GPIO as GPIO
import time
#setup gpio
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
#led
ledGPIO=18
led2GPIO=23
GPIO.setup(ledGPIO, GPIO.OUT)
GPIO.setup(led2GPIO, GPIO.OUT)
#lock
lockGPIO=21
GPIO.setup(lockGPIO, GPIO.OUT)
#button
pushbuttonGPIO=8
GPIO.setup(pushbuttonGPIO, GPIO.IN)#maybe 20/25

#run
#accept inputs
while True:
    #make light and lock False
    GPIO.output(ledGPIO, False)
    GPIO.output(led2GPIO, False)
    GPIO.output(lockGPIO, False)
    if GPIO.input(pushbuttonGPIO):
        print("button pressed")




