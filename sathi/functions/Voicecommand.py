import speech_recognition as sr
from fuzzywuzzy import fuzz, process
from .TTS import speak  # Make sure TTS.py has a speak(text) function
import pygame

# Initialize audio player
pygame.mixer.init()

def listen_and_respond(command, threshold=80):
    command = command.lower()
    
    options = {
        "MakeNotes": ["make note", "make notes"],
        "ReturnHome": ["home", "go back", "return home"],
        "ListenNotes": ["listen", "read note", "play note"],
        "AskQuestion": ["ask", "question", "ask question"]
    }

    best_match = None
    best_score = 0

    for action, phrases in options.items():
        for phrase in phrases:
            score = fuzz.partial_ratio(command, phrase)
            if score > best_score:
                best_match = action
                best_score = score

    if best_score >= threshold:
        return best_match
    else:
        return "UnknownCommand"
