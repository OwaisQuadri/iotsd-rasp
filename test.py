import RPi.GPIO as GPIO
import time
import pyttsx3
#setup speech synthesis
synthesizer=pyttsx3.init()
# setup gpio
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
# led
ledGPIO = 18
led2GPIO = 23
GPIO.setup(ledGPIO, GPIO.OUT)
GPIO.setup(led2GPIO, GPIO.OUT)
# lock
lockGPIO = 21
GPIO.setup(lockGPIO, GPIO.OUT)
# button
pushbuttonGPIO = 25
GPIO.setup(pushbuttonGPIO, GPIO.IN)  # maybe 20/25

# run
# accept inputs
try:
    synthesizer.say("Here we go")
    synthesizer.runAndWait()
    synthesizer.stop()
    while True:
        # make light and lock False
        GPIO.output(ledGPIO, True)
        GPIO.output(led2GPIO, True)
        GPIO.output(lockGPIO, )
        if GPIO.input(pushbuttonGPIO):
            print("button pressed")
except:
    GPIO.output(ledGPIO, False)
    GPIO.output(led2GPIO, False)
    GPIO.output(lockGPIO, False)
