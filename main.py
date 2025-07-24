import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
from openai import OpenAI
from gtts import gTTS
import pygame
import os

# pip install pocketsphinx

recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = "d093053d72bc40248998159804e0e67d"

def speak_old(text):
    engine.say(text)
    engine.runAndWait()

def speak(text):
    
    tts = gTTS(text)
    tts.save('temp.mp3')

    # Initialize the mixer module
    pygame.mixer.init()

    # Load the MP3 file
    pygame.mixer.music.load("temp.mp3")  # Replace with your actual file name

    # Play the MP3
    pygame.mixer.music.play()

    # Keep the script running while music is playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.music.unload()
    os.remove("temp.mp3")
    print(text)


def aiProcess(command):
    client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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"
    )
    completion = client.chat.completions.create(
        model = "deepseek/deepseek-chat-v3-0324:free",
        messages=[
            {"role": "system", "content": "You are a virtual assistent named jarvis skilled in general tasks like Alexa and Google Cloud. Give short responses please"},
            {"role": "user", "content": command}
            
        ]
            
    )

    return completion.choices[0].message.content


def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")

    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
        
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")

    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")

    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musicLibrary.music[song]
        webbrowser.open(link)

    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}")
        if r.status_code == 200:
            #parse the JSON response

            data = r.json()

            #Extract the articles
            articles = data.get('articles', [])

            #print the headlines
            for article in articles:
                speak(article['title'])
                print(article['title'])

    else:
        output = aiProcess(c)
        speak(output)
        print(output)
 

if __name__ == "__main__":
    speak("Initializing Jarvis....")
    while True:
        # Listen for the wake work "Voxa"
        # obtain audio from the microphone
        r = sr.Recognizer()

        print("recognizing...")
        # recognize speech
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source, timeout=5, phrase_time_limit=3)
            word = r.recognize_google(audio)

            
                
            if(word.lower() == "jarvis"):
                speak("Yes, how can I help you?")

            while True:       
                try:
                        # listen for command
                    with sr.Microphone() as source:
                        print("Jarvis Active...")
                        audio = r.listen(source)
                        command = r.recognize_google(audio)

                        if command.lower() in ["bye bye", "bye", "exit", "goodbye"]:
                            speak("Ba bye, have a good day!")
                            print("Jarvis: Exiting...")
                            exit()  # You can also use `break` if needed

                        processCommand(command)

                    

                except Exception as e:
                    print("Somthing Went wrong {0}".format(e))
        
        except Exception as e:
            print("Error; {0}".format(e)) 