import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
from openai import OpenAI
from gtts import gTTS 
import pygame
import os
from dotenv import load_dotenv

# pip install pygame- mp3 library which is used to play mp3files
# pip install gTTS -# google text to speech - needs google cloud paid subscription
# pip install requests
# pip install pocketsphinx
# pip install openai

# Load environment variables from the .env file
load_dotenv()

recognizer=sr.Recognizer()
engine=pyttsx3.init()
newsapi=os.getenv("NEWS_API_KEY")

def aiProcess(command):
    client = OpenAI(api_key=os.getenv("OPEN_AI_KEY"))

    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a vitual assistant named Jaris skilled in general tasks like Alexa and Google Cloud. Give short responses please."},
        {
            "role": "user",
            "content": command
        }
    ])
    return (completion.choices[0].message.content)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def speak_new(text):
    # makes an Mp3 of the text using google text to speech
    tts=gTTS(text)
    tts.save("temp.mp3") 
    # Initialize the mixer module
    pygame.mixer.init()

    # Load the MP3 file
    pygame.mixer.music.load("temp.mp3") 
    # if it doesnt work then first use unload(), to unload the file, and then use load again in the code in the same way as above, it should work

    # Play the MP3 file
    pygame.mixer.music.play()

    # Keep the script running to allow the music to play
    while pygame.mixer.music.get_busy():
        continue  # Keep looping while music is playing
    os.remove("temp.mp3")


def processCommand(c):
        # print(c)
        # pass
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open instagram" in c.lower():
        webbrowser.open("https://instagram.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif c.lower().startswith("play"):
        song=c.lower().split(" ")[1]
        link= musicLibrary.music[song]
        webbrowser.open(link)
    elif "news" in c.lower():
        r=requests.get("https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
        if r.status_code==200:
            data=r.json()

            articles=data.get('articles',[])
            for article in articles:
                speak(article['title'])
    else:
        # let openAi handle the request
        output=aiProcess(c)
        speak(output)


if __name__ == "__main__":
    speak("Initializing Jarvis...")
    while True:
        # Listen for the wake work "Jarvis"
        r=sr.Recognizer()
        
        print("Recognizing...")
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio=r.listen(source, timeout=2, phrase_time_limit=1)
            word=r.recognize_google(audio)
            if(word.lower()=="jarvis"):
                speak("Ya")
                # Listen for command
                with sr.Microphone() as source:
                    print("Jarvis active...")
                    audio=r.listen(source, timeout=2, phrase_time_limit=1)
                    command=r.recognize_google(audio)

                    processCommand(command)
        except Exception as e:
            print(f"Error: {e}")