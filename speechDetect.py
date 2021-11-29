import speech_recognition as spr
import os
from twilio.rest import Client
import dotenv
from time import sleep
import random
# load env variables
# .env file should include:
# SID=
# AUTH_TOKEN=
# USER_PHONE=
# FROM_PH=
# API_KEY=
# API_SECRET=
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
    print("toggle")


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

# function to listen


def listenFor():
    total = ""
    # if True:
    #     return "password"
    with spr.Microphone() as mic:
        #r.adjust_for_ambient_noise(mic, duration=3)
        audio = r.listen(mic)
        text = ""
        try:
            text = r.recognize_google(audio)
        except spr.UnknownValueError:
            print("an error occurred: spr.UnknownValueError")
        except spr.RequestError:
            print("an error occurred: spr.RequestError")
        except:
            print("an error occurred: idk")
        text = text.lower()
        total += text

    return text


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
