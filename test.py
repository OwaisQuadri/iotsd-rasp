import RPi.GPIO as GPIO
import time
import pyttsx3
# setup speech synthesis
synthesizer = pyttsx3.init()
# setup gpio
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
# led
redLED = 14
greenLED = 15
GPIO.setup(redLED, GPIO.OUT)
GPIO.setup(greenLED, GPIO.OUT)
# lock
lockGPIO = 23
GPIO.setup(lockGPIO, GPIO.OUT)
# button
pushbuttonGPIO = 18
GPIO.setup(pushbuttonGPIO, GPIO.IN)  # maybe 20/25

# run
# accept inputs
try:
    while True:
        # make light and lock False
        GPIO.output(redLED, True)
        GPIO.output(greenLED, True)
        GPIO.output(lockGPIO, True)
        if not GPIO.input(pushbuttonGPIO):
            print("button pressed")
            synthesizer.say("Nice!")
            synthesizer.runAndWait()
            synthesizer.stop()
            break
except Exception as e:
    GPIO.output(redLED, False)
    GPIO.output(greenLED, False)
    GPIO.output(lockGPIO, False)
    print(e)
    synthesizer.runAndWait()
    synthesizer.stop()
