import speech_recognition as spr
import os
from twilio.rest import Client
import dotenv
from time import sleep
import random
import RPi.GPIO as GPIO
import time
import picamera
import base64
import requests

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(25, GPIO.IN)
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
    with open('test.jpg', 'rb') as img:
        encoded_img = base64.standard_b64encode(img.read())
        print(encoded_img)
        return encoded_img


def faceDetect(img):
    url = 'http://validation--api.herokuapp.com/?format=json'
    payload = {
        "face": img,
        "known": False
    }
    cred=os.getenv("FACE_API_BASIC")
    headers = {
        'Authorization': f"Basic {cred}"
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.status_code, response.text)
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
        GPIO.output(18, True)
    else:
        print('unlocked')
        GPIO.output(18, False)


# function to listen


def listenFor():
    total = ""
    # if True:
    #     return "password"
    with spr.Microphone() as mic:
        print('say it now:')
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


while True:
    if GPIO.input(25):
        GPIO.output(18, False)
    else:
        GPIO.output(18, True)
        os.system("libcamera-jpeg -o test.jpg --width 200 --height 200")
        GPIO.output(18, False)
        # encode to 64

        faces_detected = faceDetect(encode())
        if len(faces_detected) == 0:
            print("No faces_detected")
        else:
            # ask the user to say their 2FA pw
            print("A password was sent to your registered phone, wait 5 seconds...")
            # the password is a random word taken from a list of 6800 commonly used nouns (could be a combo in future)
            pswd = getRandomWord()
            # print(pswd) # test
            # send message to user's phone that was fetched from django API
            client.messages.create(to=user_phone,
                                   from_=twilio_phone,
                                   body="Your 2FA password is: " +
                                   pswd)
            # after 5 seconds:
            sleep(5)
            print("Please say the password:")

            # check if password matches voice input
            inputText = listenFor()
            # print(inputText)
            if pswd in inputText:
                # toggle lock
                print("toggle lock")
                lock(False)
            else:
                print(f"the password was incorrect: '{pswd}'")
                lock(True)
            break
