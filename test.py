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
# button
pushbuttonGPIO = 18#23
GPIO.setup(pushbuttonGPIO, GPIO.IN)  # maybe 20/25

# run
# accept inputs
try:
    while True:
        # make light and lock False
        GPIO.output(redLED, True)
        GPIO.output(greenLED, True)
        if GPIO.input(pushbuttonGPIO):
            pass
        else:
            print("button pressed")
            synthesizer.say("Nice!")
            synthesizer.runAndWait()
            synthesizer.stop()
            GPIO.output(redLED, False)
            GPIO.output(greenLED, False)
            break
except Exception as e:
    print(e)
