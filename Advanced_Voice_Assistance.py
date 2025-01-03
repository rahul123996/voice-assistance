import pyttsx3
import speech_recognition as sr
import datetime
import webbrowser
import requests
import smtplib
import schedule
import time


engine = pyttsx3.init()

def speak(text):
    """Function to convert text to speech."""
    engine.say(text)
    engine.runAndWait()

def listen():
    """Function to capture voice commands."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            speak("Sorry, I didn't understand that.")
            return ""
        except sr.RequestError:
            speak("Could not connect to the network.")
            return ""

def tell_time():
    """Function to tell the current time."""
    now = datetime.datetime.now()
    current_time = now.strftime("%I:%M %p")
    speak(f"The time is {current_time}")

def tell_date():
    """Function to tell the current date."""
    today = datetime.datetime.now()
    date = today.strftime("%B %d, %Y")
    speak(f"Today's date is {date}")

def search_web(query):
    """Function to search the web."""
    webbrowser.open(f"https://www.google.com/search?q={query}")

def fetch_weather(city):
    """Function to fetch weather information."""
    api_key = "your_openweathermap_api_key"  
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": api_key, "units": "metric"}
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        temp = data["main"]["temp"]
        description = data["weather"][0]["description"]
        speak(f"The weather in {city} is {description} with a temperature of {temp} degrees Celsius.")
    else:
        speak("I couldn't fetch the weather information. Please check the city name.")

def send_email(to_email, subject, body):
    """Function to send an email."""
    sender_email = "your_email@gmail.com" 
    sender_password = "your_password"      
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            message = f"Subject: {subject}\n\n{body}"
            server.sendmail(sender_email, to_email, message)
            speak("Email sent successfully.")
    except Exception as e:
        speak("I couldn't send the email. Please check your details.")

def set_reminder(task, reminder_time):
    """Function to set a reminder."""
    def remind():
        speak(f"Reminder: {task}")
    schedule.every().day.at(reminder_time).do(remind)
    speak(f"Reminder set for {reminder_time}.")


def main():
    speak("Hello! How can I assist you today?")
    while True:
        command = listen()
        if "time" in command:
            tell_time()
        elif "date" in command:
            tell_date()
        elif "search" in command:
            speak("What should I search for?")
            query = listen()
            search_web(query)
        elif "weather" in command:
            speak("Which city's weather would you like to know?")
            city = listen()
            fetch_weather(city)
        elif "email" in command:
            speak("Who is the recipient?")
            recipient = input("Enter recipient email: ")  
            speak("What is the subject?")
            subject = listen()
            speak("What is the message?")
            message = listen()
            send_email(recipient, subject, message)
        elif "reminder" in command:
            speak("What is the reminder?")
            task = listen()
            speak("At what time? Please specify in HH:MM format.")
            reminder_time = input("Enter time (HH:MM): ") 
            set_reminder(task, reminder_time)
        elif "exit" in command or "bye" in command:
            speak("Goodbye!")
            break
        else:
            speak("I'm not sure how to help with that.")

if __name__ == "__main__":
    main()
