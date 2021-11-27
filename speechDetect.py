import speech_recognition as spr
import os
from twilio.rest import Client
import dotenv
from time import sleep
import random
#load env variables
dotenv.load_dotenv()

#load random words

words = []
try:
    while True:
        word = f.readline()
        if word == "":
            break
        words.append(word)
except:
    pass


def getRandomWord():
    f = open("words.txt", "r")
    line_number = random.choice(range(6800))
    for i, line in enumerate(f):
        if i == line_number:
            return line


#configure twillio
account_sid = os.getenv("SID")
auth_token = os.getenv("AUTH_TOKEN")
to_PN = os.getenv("TO_PH")
from_PN = os.getenv("FROM_PH")
client = Client(account_sid, auth_token)

r = spr.Recognizer()


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


#ask the user to say their password
print("Please say the password that was sent to your registered phone")
pswd = getRandomWord().replace("\n", "")
# print(pswd)

client.messages.create(to=to_PN,
                       from_=from_PN,
                       body="Your 2-Factor Authentication password is: " +
                       pswd)
#after 5 seconds:
sleep(5)
print("go:")

#check if password matches voice input
inputText = listenFor()
# print(inputText)
if pswd in inputText:
    #toggle lock
    print("toggle lock")
else:
    print(f"the password was incorrect: '{pswd}'")
