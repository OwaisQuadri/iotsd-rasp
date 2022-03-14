import RPi.GPIO as GPIO
#setup gpio
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
#led
ledGPIO=18
led2GPIO=23
GPIO.setup(ledGPIO, GPIO.OUT)
#lock
lockGPIO=21
GPIO.setup(lockGPIO, GPIO.OUT)
#button
pushbuttonGPIO=25
GPIO.setup(pushbuttonGPIO, GPIO.IN)#maybe 20/25

#run
#accept inputs
while True:

    if GPIO.input(pushbuttonGPIO):
        print("button pressed")

