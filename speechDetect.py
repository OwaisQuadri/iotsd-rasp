import json
import requests
import base64
import picamera
import time
import RPi.GPIO as GPIO
import random
from time import sleep
import dotenv
from twilio.rest import Client
import os
import speech_recognition as spr
import pyttsx3
LOCK_NAME = "lock1"
speaker=pyttsx3.init()
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
# GPIO pin setup
pushbuttonGPIO = 18
redLED = 14
greenLED = 15
lockGPIO = 23
# GPIO connection setup and direction
GPIO.setup(redLED, GPIO.OUT)
GPIO.setup(greenLED, GPIO.OUT)
GPIO.setup(lockGPIO, GPIO.OUT)
GPIO.setup(pushbuttonGPIO, GPIO.IN)
# load env variables
# .env file should include:
# SID=
# AUTH_TOKEN=
# USER_PHONE=
# FROM_PH=
# API_KEY=
# API_SECRET=
# configure twillio
api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")
user_sid = os.getenv("SID")
auth_token = os.getenv("AUTH_TOKEN")
user_phone = os.getenv("USER_PHONE1")
twilio_phone = os.getenv("FROM_PH")
# sign in with api_key and secret password
client = Client(username=api_key, password=api_secret, account_sid=user_sid)
# create speechrecog obj
r = spr.Recognizer()

dotenv.load_dotenv()
# while true loop
#   listen for button press
#   run get request to lock status every 10 secs
# if status = locked -> lock(True)
# if status = unlocked -> lock(False)
# if button pressed:
# check from camera which user is at the door
# take picture
# encode to base64
# send json with picture encoded to API
# if returns a blank message -> do nothing or turn on red light
# else if a phone number is also returned with the name, store phone number in variable for furhter use


# get random password from file


def encode():
    with open('test.png', 'rb') as img:
        encoded_img = base64.standard_b64encode(img.read())
        print(encoded_img)
        return encoded_img


def faceDetect(img):
    url = 'http://validation--api.herokuapp.com/?format=json'
    payload = {
        "face": img,
        "known": False
    }
    cred = os.getenv("FACE_API_BASIC")
    headers = {
        'Authorization': f"Basic {cred}"
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.status_code, response.text)
    response.close()
    return response.text
# mine


def getRandomWord():
    f = open("words.txt", "r")
    line_number = random.choice(range(6800))
    for i, line in enumerate(f):
        if i == line_number:
            return line.replace("\n", "")
# define toggle lock function


def lock(locked):
    # if lock physical position == locked && locked==True do nothing
    # if lock physical position == unlocked && locked ==False do nothing
    # if lock physical position == locked && locked == False unlock the lock and update physical position
    # if lock physical position == unlocked && locked ==True lcok the lock and update physical position
    # toggle lock
    # send lock status to API as well as who triggered lock and when
    #
    if locked:
        print('lock')
        toggleLED(True,'red')
        toggleLED(False,'green')
    else:
        print('unlocked')
        toggleLED(False,'red')
        toggleLED(False,'green')


def toggleLED(bool, color):
    if color.lower() == 'red':
        GPIO.output(redLED, bool)
    elif color.lower() == 'green':
        GPIO.output(greenLED, bool)

# function to listen
def listenFor():
    total = ""
    # if True:
    #     return "password"
    with spr.Microphone() as mic:
        ###########SAY IT NOW###########
        r.adjust_for_ambient_noise(mic, duration=.2)
        audio = r.listen(mic)
        text = ""
        try:
            text = r.recognize_google(audio)
        except spr.UnknownValueError:
            print("an error occurred: spr.UnknownValueError")
        except spr.RequestError:
            print("an error occurred: spr.RequestError")
        except Exception as err:
            print(f"an error occurred: {err=}: {type(err)=}")
        text = text.lower()
        total += text

    return text


def checkLockStatus(lock_name):
    url = f'http://validation--api.herokuapp.com/status/{lock_name}'
    cred = os.getenv("FACE_API_BASIC")
    headers = {
        'Authorization': f"Basic {cred}"
    }
    response = requests.request("GET", url, headers=headers)
    reply = json.loads(response.text)
    print(response.status_code, reply["status"])
    if response.status_code == 200:
        if reply["status"] == True:
            lock(True)
        else:
            lock(False)
    response.close()


def setLockStatus(lock_name, status, recogName=None):
    url = f'http://validation--api.herokuapp.com/status/'
    cred = os.getenv("FACE_API_BASIC")
    headers = {
        'Authorization': f"Basic {cred}"
    }
    if recogName is not None:
        payload = {
            "lock_name": lock_name,
            "status": status,
            "changed_by": recogName,
        }
    else:
        payload = {
            "lock_name": lock_name,
            "status": status,
        }
    response = requests.request("POST", url, headers=headers, data=payload)
    reply = response.text
    print(response.status_code, reply)
    if "true" in reply:
        lock(True)
    else:
        lock(False)
    response.close()
# start script


# handle interrupt
try:
    counter = 0
    while True:
        # every 100000 ticks check the lock status
        if counter == 100000:
            checkLockStatus(LOCK_NAME)
            counter = 0
        # listen for button presses every tick
        if GPIO.input(pushbuttonGPIO):
            pass
        else:
            os.system(
                "libcamera-still -e png -o test.png --width 200 --height 200")
            # encode to 64 and store names
            faces_detected = faceDetect(encode())
            detectedJSON = json.loads(faces_detected)

            if faces_detected == '""':
                print("No verified individuals detected")
                setLockStatus(LOCK_NAME, True, "Unauthorized User Detection")
                lock(True)
            else:
                user_phone = detectedJSON[0]['phone']
                user_name = detectedJSON[0]['name']
                # ask the user to say their 2FA pw
                print("A password was sent to your registered phone, wait 10 seconds...")
                # the password is a random word taken from a list of 6800 commonly used nouns (could be a combo in future)
                pswd = getRandomWord()
                # print(pswd) # test
                # send message to user's phone that was fetched from django API
                client.messages.create(to=user_phone,
                                       from_=twilio_phone,
                                       body="Your 2FA password is: " +
                                       pswd)
                # after 10 seconds:
                sleep(10)
                toggleLED(True,'green')  # turn on light
                # check if password matches voice input
                inputText = listenFor()
                # turn off light
                toggleLED(False,'green')
                # print(inputText)
                if pswd in inputText:
                    setLockStatus(LOCK_NAME, False, recogName=user_name)

                    # hardware based reCaptcha
                    #make the speaker say something
                    ################REPEAT AFTER ME#################
                    ans = 'unlock'
                    user_ans = listenFor()
                    if ans in user_ans:
                        lock(False)

                else:
                    ###########DOOR LOCKED###########
                    print(f"the password was incorrect: '{pswd}'")
                    lock(True)
                    setLockStatus(LOCK_NAME, True)

        counter += 1
except KeyboardInterrupt:
    print("^C Detected: Exiting ...")
    toggleLED(False,'green')
    toggleLED(False,'red')
