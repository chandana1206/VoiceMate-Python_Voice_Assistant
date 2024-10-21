import subprocess
import wolframalpha
import pyttsx3
import tkinter
import json
import random
import operator
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import winshell
import pyjokes
# import feedparser
import smtplib
import ctypes
import time
import requests
import shutil
from twilio.rest import Client
# from clint.textui import progress
from ecapture import ecapture as ec
from bs4 import BeautifulSoup
import win32com.client as wincl
from urllib.request import urlopen

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


def wishMe():
    hour = int(time.strftime("%H"))
    if 0 <= hour < 12:
        greeting = "Good Morning!"
    elif 12 <= hour < 18:
        greeting = "Good Afternoon!"
    else:
        greeting = "Good Evening!"
    
    speak(greeting)


def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()

assname =("Voice Mate")

def takeCommand():
    r = sr.Recognizer()  
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1  
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')  
        print(f"User said: {query}\n")
        return query
    except Exception as e:
        speak("Sorry, I didn't catch that. Could you please repeat?")
        return None 
    return query

def getWeather(city):
    api_key = '41cb32ec6904a65c1cb44e865234e40f'  
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}q={city}&appid={api_key}&units=metric"
    
    response = requests.get(complete_url)
    data = response.json()
    
    if data['cod'] == 200:
        main = data['main']
        weather_desc = data['weather'][0]['description']
        temp = main['temp']
        speak(f"The temperature in {city} is {temp} degrees Celsius with {weather_desc}.")
    else:
        speak("City not found. Please check the name and try again.")

def sendEmail(to, content):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.ehlo()  

        sender_email = os.getenv('SENDER_EMAIL')
        sender_password = os.getenv('SENDER_PASSWORD')

        server.login(sender_email, sender_password) 
        server.sendmail(sender_email, to, content)
        server.close()
        return True
    except Exception as e:
        print(e)
        return False

how_are_you=False

def handleCommand(query):
    query=query.lower()
    global how_are_you
    if 'wikipedia' in query:
        speak("Searching Wikipedia...")
        query = query.replace("wikipedia", "")
        results = wikipedia.summary(query, sentences=2)  
        speak("According to Wikipedia")
        speak(results)

    elif 'open youtube' in query:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")
        exit()
    
    elif 'open google' in query:
        speak("Opening Google\n")
        webbrowser.open("google.com")
        exit()
    
    elif 'open spotify' in query:
        speak("Opening Spotify")
        webbrowser.open("https://www.spotify.com")
        exit()

    elif 'weather' in query:
        speak("Please tell me the city name.")
        city = takeCommand()
        if city:
            getWeather(city)
        
    elif 'mail' in query or 'email' in query:
        try:
            speak("Please type in the recipient's email address:")
            to = input()  # Get the recipient's email

            speak("What should I say?")
            content = takeCommand()  # Get the content of the email

            if sendEmail(to, content):
                speak("Email has been sent successfully!")
            else:
                speak("I was unable to send the email.")
        except Exception as e:
            print(e)
            speak("There was an error. Please try again.")

    elif 'date' in query.lower():
        today = datetime.datetime.now().strftime("%B %d, %Y")
        speak(f"Today's date is {today}.")

    elif 'time' in query:
        strTime = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"The time is {strTime}")

    elif 'how are you' in query:
        speak("I am fine, Thank you. How are you?")
        how_are_you=True
    elif ('fine' in query or "good" in query) and how_are_you:
        speak("It's good to hear that.")
        how_are_you=False
    
    elif " your name" in query or "who are you" in query:
            speak(f"My name is {assname}. I am your voice assistant.")

    elif 'joke' in query:
            speak(pyjokes.get_joke())

    elif 'thanks' in query or 'thank you' in query :
            speak("You are welcome!")
            exit()

    elif 'exit' in query or 'stop' in query or 'bye' in query:
            speak("Bye. See you later!!")
            exit()
    else:
        speak("I'm sorry, I can't do that yet.")

if __name__ == "__main__":

    clear = lambda: os.system('cls')
     
    clear()
    wishMe()
    speak("I am your voice assistant. How can I help you today?")
    
    while True:
        query = takeCommand()

        if query:
            handleCommand(query)
            
