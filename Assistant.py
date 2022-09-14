
# Ayush speech assistant
import glob
from stat import S_IWGRP
from this import s
from urllib import response
from winsound import PlaySound
import dotenv
import speech_recognition as sr # recognise speech
import playsound # to play an audio file
from gtts import gTTS # google text to speech
import random
from time import ctime # get time details
import webbrowser # open browser
import ssl
import certifi
import time
import os # to remove created audio files
from PIL import Image
import subprocess
import pyautogui #screenshot
import pyttsx3
import bs4 as bs
import urllib.request
import requests
import datetime
import smtplib
from dotenv import load_dotenv
load_dotenv()


class loc:
    ipApi = os.getenv('ipApi')
    Ip_info = requests.get('https://api.ipdata.co?api-key='+ ipApi).json()
    cur_loc = Ip_info['region']

class temp:
    owUrl = os.getenv('owUrl') + loc.cur_loc
    
    response = requests.get(owUrl)

    x = response.json()
    if x["cod"] != "404":
        y = x["main"]
        current_temperature = round(y["temp"] - 273.15)
        min_temp = round(y["temp_min"] - 273.15)
        max_temp = round(y["temp_max"] -273.15)
        current_pressure = y["pressure"]
        current_humidity = y["humidity"]
        z = x["weather"]
        weather_description = z[0]["description"]

class person:
    name = dotenv.get_key(".env",'name')
    def setName(self, name):
        dotenv.set_key(".env","name", name)
        self.name = name

class asis:
    name = dotenv.get_key(".env",'asis_name')
    def setName(self, name):
        dotenv.set_key(".env","asis_name", name)
        self.name = name

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty("voice", voices[0].id)

def there_exists(terms):
    for term in terms:
        if term in voice_data:
            return True

def there_exists_in(terms, data):
    for term in terms:
        if term in data:
            return True

def there_exists_all(terms):
    exists = False
    for term in terms:
        if term in voice_data:
            exists = True
        else:
            exists = False
    return exists

def engine_speak(text):
    text = str(text)
    engine.say(text)
    engine.runAndWait()

r = sr.Recognizer() # initialise a recogniser
# listen for audio and convert it to text:
def record_audio(ask=""):
    with sr.Microphone() as source: # microphone as source
        if ask:
            engine_speak(ask)
        else:
            print("Listening...")
        audio = r.listen(source, 5, 5)  # listen for the audio via source
        print("Done Listening")
        voice_data = ''
        try:
            voice_data = r.recognize_google(audio)  # convert audio to text
        except sr.UnknownValueError: # error: recognizer does not understand
            engine_speak('could you please say it again?')
        except sr.RequestError:
            engine_speak('Sorry, the service is down') # error: recognizer is not connected
        print(">>", voice_data.lower()) # print what user said
        return voice_data.lower()

# get string and make a audio file to be played
def engine_speak(audio_string):
    audio_string = str(audio_string)
    tts = gTTS(text=audio_string, lang='en-in') # text to speech(voice)
    r = random.randint(1,20000000)
    audio_file = 'audio' + str(r) + '.mp3'
    tts.save(audio_file) # save as mp3
    playsound.playsound(audio_file) # play the audio file
    print(asis_obj.name + ":", audio_string) # print what app said
    os.remove(audio_file) # remove audio file

def sendEmail(to, content):
    s_email = os.getenv('senders_email')
    s_pswrd = os.getenv('password')

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(s_email,s_pswrd)
    print(s_email, s_pswrd)
    server.sendmail(s_email,to,content)
    server.close()

def respond(voice_data):
    # 1: send email

    if there_exists_all(["send", "email"]):
        try:
            voice_data = record_audio("What should i say")
            engine_speak("please write receivers email address: ")
            to = input("Email address: ")
            sendEmail(to,voice_data)
            engine_speak("Email has been sent")
        except Exception as er:
            print(er)
            engine_speak("sorry mail couldn't be sent")

    # 2: name
    if there_exists(["can you do"]):
        engine_speak("I can send emails, take screenshots, check weather, your location, et cetera")
    if there_exists(["what is your name","what's your name","tell me your name", "what should i call you"]):

        if person_obj.name:
            engine_speak(f"you can call me {asis_obj.name},... {person_obj.name}") #gets users name from voice input
        else:
            res = record_audio(f"you can call me {asis_obj.name}. what's your name?")

            if there_exists_in(["my name is"], res):
                person_name = res.split("is")[-1].strip()
                engine_speak("okay, i will remember that " + person_name)
                person_obj.setName(person_name)
            elif(len(res.split()) ==1):
                person_name = res
                engine_speak("okay, i will remember that " + person_name)
                person_obj.setName(person_name)
             #incase you haven't provided your name.

    if there_exists(["my name is"]):
        person_name = voice_data.split("is")[-1].strip()
        engine_speak("okay, i will remember that " + person_name)
        person_obj.setName(person_name) # remember name in person object

    if there_exists(["what is my name"]):
        if(person_obj.name!= ""):
            engine_speak("Your name must be " + person_obj.name)
        else:
            res = record_audio("Sorry, I don't know your name? So, What is your name ? ") 
            if there_exists_in(["my name is"], res):
                person_name = res.split("is")[-1].strip()
                engine_speak("okay, i will remember that " + person_name)
                person_obj.setName(person_name)
            elif(len(res.split()) ==1):
                person_name = res
                engine_speak("okay, i will remember that " + person_name)
                person_obj.setName(person_name)    
    
    if there_exists(["can i call you", "should i call you"]):
        asis_name = voice_data.split("you ")[-1].strip()
        engine_speak("okay, i will remember that my name is " + asis_name)
        asis_obj.setName(asis_name) # remember name in asis object

    if there_exists(["repeat after me", "say after me", "repeat this"]):
        response = record_audio("Okay")
        engine_speak(response)
    if there_exists(["clear trash", "remove trash", "remove junks", "delete trash", "delete audio", "remove bin"]):
        os.chdir('./')
        for file in glob.glob('audio*.mp3'):
            os.remove(file)

    # 3: greeting
    if there_exists(["how are you","how are you doing"]):
        engine_speak("I'm very well, thanks for asking " + person_obj.name)
    
    # 4: time
    if there_exists(["what's the time","tell me the time","what time is it","what is the time"]):
        time = ctime().split(" ")[3].split(":")[0:2]
        if time[0] == "00":
            hours = '12'
        else:
            hours = time[0]
        minutes = time[1]
        time = hours + " hours and " + minutes + "minutes"
        engine_speak(time)

    # 5: search google
    if there_exists(["search for"]) and 'youtube' not in voice_data:
        search_term = voice_data.split("for")[-1]
        url = "https://google.com/search?q=" + search_term
        webbrowser.get().open(url)
        engine_speak("Here is what I found for" + search_term + "on google")
    
    if there_exists(["search"]) and 'youtube' not in voice_data:
        search_term = voice_data.replace("search","")
        url = "https://google.com/search?q=" + search_term
        webbrowser.get().open(url)
        engine_speak("Here is what I found for" + search_term + "on google")

    # 6: search youtube
    if there_exists(["youtube"]):
        search_term = voice_data.split("for")[-1]
        search_term = search_term.replace("on youtube","").replace("search","")
        url = "https://www.youtube.com/results?search_query=" + search_term
        webbrowser.get().open(url)
        engine_speak("Here is what I found for " + search_term + "on youtube")

     #7: get stock price
    if there_exists(["price of"]):
        search_term = voice_data.split("for")[-1]
        url = "https://google.com/search?q=" + search_term
        webbrowser.get().open(url)
        engine_speak("Here is what I found for " + search_term + " on google")
    


     #8 time tableṇ
    if there_exists(["show my time table"]):
        im = Image.open(r"D:\WhatsApp Image 2019-12-26 at 10.51.10 AM.jpeg")
        im.show()
    
     #9 weather
    if there_exists(["weather"]):
        search_term = voice_data.split("for")[-1]
        url = "https://www.google.com/search?sxsrf=ACYBGNSQwMLDByBwdVFIUCbQqya-ET7AAA%3A1578847393212&ei=oUwbXtbXDN-C4-EP-5u82AE&q=weather&oq=weather&gs_l=psy-ab.3..35i39i285i70i256j0i67l4j0i131i67j0i131j0i67l2j0.1630.4591..5475...1.2..2.322.1659.9j5j0j1......0....1..gws-wiz.....10..0i71j35i39j35i362i39._5eSPD47bv8&ved=0ahUKEwiWrJvwwP7mAhVfwTgGHfsNDxsQ4dUDCAs&uact=5"
        webbrowser.get().open(url)
        engine_speak("Here is what I found for on google")
    if there_exists(["temperature"]):
        engine_speak("Current temperature in " + loc.cur_loc+ " is " + str(temp.current_temperature) + " degree celcius")
        response = record_audio("Should I tell you all weather information ?")
        if(response=="yes"):
            engine_speak("Minimum Temperature will be " + str(temp.min_temp) + "degree celcius whereas maximum temperature will be "+ str(temp.max_temp) + "degree celcius")
     
     #10 stone paper scisorrs
    if there_exists(["game"]):
        voice_data = record_audio("choose among rock paper or scissor")
        moves=["rock", "paper", "scissor"]
    
        cmove=random.choice(moves)
        pmove=voice_data
        

        engine_speak("The computer chose " + cmove)
        engine_speak("You chose " + pmove)
        #engine_speak("hi")
        if pmove==cmove:
            engine_speak("the match is draw")
        elif pmove== "rock" and cmove== "scissor":
            engine_speak("Player wins")
        elif pmove== "rock" and cmove== "paper":
            engine_speak("Computer wins")
        elif pmove== "paper" and cmove== "rock":
            engine_speak("Player wins")
        elif pmove== "paper" and cmove== "scissor":
            engine_speak("Computer wins")
        elif pmove== "scissor" and cmove== "paper":
            engine_speak("Player wins")
        elif pmove== "scissor" and cmove== "rock":
            engine_speak("Computer wins")

     #11 toss a coin
    if there_exists(["toss","flip","coin"]):
        moves=["head", "tails"]   
        cmove=random.choice(moves)
        engine_speak("The computer chose " + cmove)

     #12 calc
    if there_exists(["plus","minus","multiply","divide","power","+","-","*","/"]):
        opr = voice_data.split()[1]

        if opr == '+':
            engine_speak(int(voice_data.split()[0]) + int(voice_data.split()[2]))
        elif opr == '-':
            engine_speak(int(voice_data.split()[0]) - int(voice_data.split()[2]))
        elif opr == 'multiply' or 'x':
            engine_speak(int(voice_data.split()[0]) * int(voice_data.split()[2]))
        elif opr == 'divide':
            engine_speak(int(voice_data.split()[0]) / int(voice_data.split()[2]))
        elif opr == 'power':
            engine_speak(int(voice_data.split()[0]) ** int(voice_data.split()[2]))
        else:
            engine_speak("Wrong Operator")
        
     #13 screenshot
    if there_exists(["capture","my screen","screenshot"]):
        myScreenshot = pyautogui.screenshot()
        myScreenshot.save('C:/Users/hp/Pictures/Screenshots/screen.png')
    
    
     #14 to search wikipedia for definition
    if there_exists(["definition of"]):
        definition=voice_data.split("of ")[-1]
        url=urllib.request.urlopen('https://en.wikipedia.org/wiki/'+definition)
        soup=bs.BeautifulSoup(url,'lxml')
        definitions=[]
        for paragraph in soup.find_all('p'):
            definitions.append(str(paragraph.text))
        if definitions:
            if definitions[0]:
                engine_speak('im sorry i could not find that definition, please try a web search')
            elif definitions[1]:
                engine_speak('here is what i found '+definitions[1])
            else:
                engine_speak ('Here is what i found '+definitions[2])
        else:
                engine_speak("im sorry i could not find the definition for "+definition)


    if there_exists(["exit", "quit", "goodbye","bye"]):
        engine_speak("bye")
        exit()

    # Current city or region
    if there_exists(["where am i"]):
        engine_speak(f"You must be somewhere in {loc.cur_loc}")    
   
   # Current location as per Google maps
    if there_exists(["what is my exact location"]):
        url = "https://www.google.com/maps/search/Where+am+I+?/"
        webbrowser.get().open(url)
        engine_speak("You must be somewhere near here, as per Google maps")    

   # Save unrecognised commands

    if there_exists(["save a memo", "save a note", "listen it"]):
        voice_data = record_audio("Okay! You may speak whatever you want to save")
        requested_commands = open("Notepad.txt","a+")
        current_time = datetime.datetime.now()
        requested_commands.write(f"Note saved at {current_time} \n{voice_data} \n\n\n")
        requested_commands.close()
    
    if there_exists(["play music"]):
        songs_folder = 'E:\\music'
        songs = os.listdir(songs_folder)
        os.startfile(os.path.join(songs_folder, songs[0]))
        engine_speak("Enjoy")
        exit()



time.sleep(1)

person_obj = person()
asis_obj = asis()


def greets():
    greetings = ["hey, how can I help you " + person_obj.name, "hey, what's up?, " + person_obj.name, "I'm listening " + person_obj.name, "how can I help you? " + person_obj.name, "hello " + person_obj.name, person_obj.name + " Kaise ho aap ?"]
    greet = greetings[random.randint(0,len(greetings)-1)]
    engine_speak(greet)

if __name__ == "__main__":
    greets()
    while(1):
        voice_data = record_audio("") # get the voice input
        print("Done")
        # print("Q:", voice_data)
        respond(voice_data) # respond

