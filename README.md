# Accessibility Application for Visually Impaired Students

## Project overview

An accessibility-focused web application built during a 42-hour hackathon to help visually impaired students access course notes, navigate the student dashboard using voice, and convert documents into spoken audio. The project provides speech-to-text, text-to-speech, fuzzy voice-command recognition, and utilities for saving and managing notes via voice.

## Key features

- Voice navigation: press the spacebar to record a short voice command in the browser, which triggers server-side transcription and fuzzy command matching to navigate the app (make notes, go home, read notes, ask questions, read specific subject PDFs).
- Speech-to-text: backend audio conversion and transcription for uploaded or recorded audio files.
- Text-to-speech: PDF and text extraction to MP3 using gTTS with playback via pygame.
- Notes management: save transcribed audio as text notes under `media/notes`, list/delete notes from the student UI.
- (Prototype) Face authentication: face encoding pipeline and a scaffolded face-auth module using `face_recognition`/OpenCV.

## Tech stack / languages

- Backend: Django (Python 3.x)
- Frontend: ES6 JavaScript, HTML5, CSS
- Database: SQLite (development)

## Primary libraries & components

- Speech recognition: `speech_recognition` Python library with `recognize_google` (Google Web Speech API) for transcription.
- Audio processing: `pydub` for file format conversion and sampling rate normalization.
- Text-to-speech: `gTTS` for MP3 generation and `pygame` for playback.
- PDF/text extraction: `PyPDF2` for extracting text from PDF files.
- Voice command parsing: `fuzzywuzzy` for fuzzy matching of transcribed text to supported actions.
- Frontend recorder: MediaRecorder API + `fetch` POST to `/upload_audio/` (CSRF-protected) located in `sathi/static/js/voice_recorder.js`.
- Optional/prototype: `face_recognition` and OpenCV-based face encoding/storage (CSV) in `sathi/functions/face/`.

## High-level architecture

- Frontend: user presses the spacebar to start/stop audio capture; the audio blob is POSTed to `/upload_audio/`.
- Server-side `/upload_audio/`: converts incoming audio to 16kHz mono WAV (via `pydub`), runs `speech_recognition` to transcribe, passes transcript to the fuzzy command matcher in `sathi/functions/Voicecommand.py`.
- Command routing: recognized commands map to actions such as redirecting to `make_notes`, `dashboard_student`, `student_notes`, or `student_ask` endpoints; TTS feedback is provided using `gTTS` + `pygame`.
- Notes pipeline: endpoint `save_note_audio` converts audio→text and writes note files into `media/notes` for later reading / batch MP3 generation.

## Repository layout (important files)

- `manage.py` — Django entrypoint
- `padhaisathi/` — Django project settings and WSGI/ASGI
- `sathi/` — primary application containing views, models, templates, static assets
- `sathi/functions/STT.py` — STT helper, audio conversion utilities
- `sathi/functions/TTS.py` — TTS helper, PDF/text extraction and MP3 creation
- `sathi/functions/Voicecommand.py` — fuzzy command matching and voice navigation logic
- `sathi/static/js/voice_recorder.js` — browser recorder and upload flow
- `media/notes/` — transcribed notes saved by the app

## Setup & development

Prerequisites: Python 3.8+ (3.10 recommended), pip, virtualenv (optional).

1. Create and activate a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies

```powershell
pip install -r requirements.txt
```

3. Run migrations and create a superuser

```powershell
python manage.py migrate
python manage.py createsuperuser
```

4. Run the development server

```powershell
python manage.py runserver
```

## Usage notes

- To use voice navigation from the student UI: focus the page and press the spacebar to start recording; release the spacebar to submit audio. The client uploads the recording to `/upload_audio/` which will return a JSON redirect on success.
- To generate spoken MP3s for all notes, see the TTS batch functions in `sathi/functions/TTS.py`.
- Transcriptions are saved into `media/notes` by default — ensure your `MEDIA_ROOT` settings are correct for production.

## Documentation

This repository includes detailed documentation covering architecture diagrams, API behaviors, deployment notes, and accessibility testing results. See the project's documentation folder for design decisions, developer guides, and testing reports.

## Contributing

- Open issues or pull requests against this repository for bug fixes or feature work.
- For large changes, please open an issue describing your plan before submitting code.

## License

Check the repository's `LICENSE` file if present.

## Contact / Authors

Project created during a 42‑hour hackathon. For questions or collaboration, open an issue in the repository.

# Padhai-Sathi
