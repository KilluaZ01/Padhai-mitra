import speech_recognition as sr
from fuzzywuzzy import fuzz, process
from .TTS import speak  # Make sure TTS.py has a speak(text) function
import pygame

# Initialize audio player
pygame.mixer.init()

# Match threshold for fuzzy matching
MATCH_THRESHOLD = 50

# List of predefined commands
commands = [
    "MakeNotes",
    "ListenNotes",
    "AskQuestion",
    "Home",
]

# Fuzzy match the command
def match_command(command):
    return process.extractOne(command, commands, scorer=fuzz.partial_ratio)

# Main loop
def listen_and_respond(command):

    while True:
        try:
            best_match, score = match_command(command)
            print(f"Best match: {best_match} with score {score}")

        except sr.UnknownValueError:
            print("Could not understand audio.")
        except sr.RequestError:
            print("Speech recognition service unavailable.")
            speak("Service unavailable.")

        return best_match
