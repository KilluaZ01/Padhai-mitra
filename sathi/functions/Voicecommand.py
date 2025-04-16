import speech_recognition as sr
import pygame
import os
from pdf_to_mp3 import makemp3  # Import the function to ensure MP3s are generated

pygame.init()

def speak(filename):
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    os.remove(filename)

def recognize_speech():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()                     

    print("Listening for a command...")

    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        # Recognize the speech using Google Web Speech API
        command = recognizer.recognize_google(audio).lower()
        print(f"You said: {command}")
        return command
    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio.")
        return None
    except sr.RequestError:
        print("Sorry, I'm having trouble connecting to the speech recognition service.")
        return None

def play_mp3_from_command():
    # First, let's make the MP3 files if they don't already exist
    makemp3()
    
    # Ask the user for a file name using voice command
    command = recognize_speech()

    if command:
        mp3_folder = "mp3"
        # Construct the mp3 filename from the command
        mp3_filename = os.path.join(mp3_folder, f"{command}.mp3")

        # Check if the file exists
        if os.path.exists(mp3_filename):
            print(f"Playing: {mp3_filename}")
            speak(mp3_filename)
        else:
            print(f"File '{command}.mp3' not found.")
    else:
        print("No valid command received.")

# Run the function to listen for the command and play the corresponding MP3
if __name__ == "__main__":
    play_mp3_from_command()
