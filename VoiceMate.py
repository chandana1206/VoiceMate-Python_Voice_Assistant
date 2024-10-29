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
from googletrans import Translator


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


def wishMe():
    hour = int(time.strftime("%H"))
    if hour < 12:
        greeting = "Good Morning!"
    elif 12 <= hour < 17:
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
    try:
        api_key = '41cb32ec6904a65c1cb44e865234e40f'
        base_url = "http://api.openweathermap.org/data/2.5/weather?"
        complete_url = f"{base_url}q={city}&appid={api_key}&units=metric"
        
        response = requests.get(complete_url)
        data = response.json()

        if data.get("cod") == 200:
            main = data['main']
            weather_desc = data['weather'][0]['description']
            temp = main['temp']
            speak(f"The temperature in {city} is {temp} degrees Celsius with {weather_desc}.")
        else:
            speak("City not found. Please check the name and try again.")
    except Exception as e:
        speak("Sorry, I couldn't fetch the weather information at the moment.")
        print("Weather Error:", e)

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

def getNews():
    api_key = "825734b0b3fd4001b4d0fddea99f87dd"
    url = f"http://newsapi.org/v2/top-headlines?country=in&apiKey={api_key}"
    response = requests.get(url).json()
    
    if response["status"] == "ok":
        articles = response["articles"][:5] 
        speak("Here are the top news headlines.")
        for article in articles:
            speak(article["title"])
    else:
        speak("Sorry, I couldn't fetch the news at the moment.")

def translateText(text, target_language="en"):
    translator = Translator()
    try:
        translated = translator.translate(text, dest=target_language)
        speak(f"The translation is: {translated.text}")
    except Exception as e:
        speak("I'm sorry, I couldn't translate the text.")


how_are_you=False

def handleCommand(query):
    query=query.lower()
    global how_are_you
    if 'wikipedia' in query:
        speak("Searching Wikipedia...")
        query = query.replace("wikipedia", "")
        try:
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            speak(results)
        except wikipedia.exceptions.DisambiguationError:
            speak("There are multiple results for that query. Please be more specific.")
        except wikipedia.exceptions.PageError:
            speak("I couldn't find a matching page on Wikipedia.")


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
    
    elif "your name" in query or "who are you" in query:
            speak(f"My name is {assname}. I am your voice assistant.")

    elif 'joke' in query:
            speak(pyjokes.get_joke())
    
    elif 'translate' in query:
        speak("What would you like me to translate?")
        text = takeCommand()
        if text:
            speak("Which language should I translate it to?")
            target_language = takeCommand().lower()
            lang_code = {
                "spanish": "es", "french": "fr", "german": "de",
                "hindi": "hi", "japanese": "ja", "english": "en"
            }.get(target_language, "en") 
            translateText(text, lang_code)
    
    elif 'news' in query:
        getNews()

    elif 'thanks' in query or 'thank you' in query :
            speak("You are welcome!")
            exit()

    elif 'exit' in query or 'stop' in query or 'bye' in query:
            speak("Bye. See you later!!")
            exit()
    else:
        speak("I'm sorry, I can't do that yet.")
        
    speak("What else can I do for you?")


if __name__ == "__main__":

    clear = lambda: os.system('cls')
     
    clear()
    wishMe()
    speak("I am your voice assistant. How can I help you today?")
    
    while True:
        query = takeCommand()

        if query:
            handleCommand(query)
            