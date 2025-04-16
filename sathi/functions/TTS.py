from gtts import gTTS
import pygame
import os
import time
from PyPDF2 import PdfReader
from pathlib import Path

pygame.init()

def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text
    return text

def mp3(text, filename="output.mp3"):
    tts = gTTS(text=text, lang='en')
    tts.save(filename)

def speak(filename):
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    os.remove(filename)

def extract_filenames(folder_path="teacher"):
    folder = Path(folder_path)
    folder.mkdir(parents=True, exist_ok=True)  # Create the folder if it doesn't exist

    file_list = [f.name for f in folder.iterdir() if f.is_file() and f.suffix == ".pdf"]
    return len(file_list), file_list


def makemp3():
    folder_path = "teacher"
    file_count, file_names = extract_filenames(folder_path)
    
    for name in file_names:
        file_path = os.path.join(folder_path, name)
        print(f"Processing: {file_path}")
        text = extract_text_from_pdf(pdf_path=file_path)
        
        if text.strip():
            mp3_filename = file_path.replace(".pdf", ".mp3")
            mp3(text=text, filename=mp3_filename)
            print(f"Saved: {mp3_filename}")
        else:
            print(f"No text found in {file_path}")

makemp3()
