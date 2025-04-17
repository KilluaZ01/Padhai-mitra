# views.py
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from .models import User
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from .functions.STT import transcribe_audio_file,convert_to_wav
from .functions.Voicecommand import listen_and_respond,listen_and_respond_pdf
from .functions.TTS import speak,extract_filenames
import speech_recognition as sr
from pydub import AudioSegment
import speech_recognition as sr
import os
from django.urls import reverse
from django.conf import settings
import os
import time
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from .models import User
from django.contrib import messages
from .functions.face.auth import is_face_authenticated
import face_recognition
import pygame

def test(request):
    return render(request,"test.html")


@csrf_exempt
def upload_audio(request):
    if request.method == 'POST' and request.FILES.get('audio_file'):
        audio_file = request.FILES['audio_file']
        tomp3 = None
        try:
            tomp3 = convert_to_wav(audio_file)
            texts = transcribe_audio_file(tomp3)
            textlast = listen_and_respond(command=texts)
            print(textlast)

            if textlast == "MakeNotes":
                return JsonResponse({'redirect': '/make_notes/'})
            elif textlast == "ReturnHome":
                speak("Back to dashboard")
                return JsonResponse({'redirect': '/dashboard_student/'})
            elif textlast == "ListenNotes":
                speak("say notes name")
                return JsonResponse({'redirect': '/student_notes/'})
            elif textlast == "AskQuestion":
                speak("ask question")
                return JsonResponse({'redirect': '/student_ask/'})
            else:
                return JsonResponse({'error': 'No valid command recognized'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        finally:
            if tomp3 and os.path.exists(tomp3):
                time.sleep(5)  # Delay 5 seconds before deletion
                os.remove(tomp3)

    return JsonResponse({'error': 'No audio file received'}, status=400)





import os
import time
import uuid
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt  # Optional if CSRF token isn't handled on frontend
def save_note_audio(request):
    if request.method == 'POST' and request.FILES.get('audio_file'):
        audio_file = request.FILES['audio_file']
        tomp3 = None
        try:
            # Convert audio file to WAV format if necessary
            tomp3 = convert_to_wav(audio_file)

            # Transcribe audio to text
            texts = transcribe_audio_file(tomp3)

            # Generate a unique file name using uuid and time
            unique_filename = f"note_{int(time.time())}.txt"

            # Define the path for the text file
            text_file_path = os.path.join('media/notes', unique_filename)

            # Save the transcribed text to the file
            with open(text_file_path, 'w') as text_file:
                text_file.write(texts)

            return JsonResponse({'success': True, 'message': 'Audio processed and text saved successfully.'})
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        
        finally:
            if tomp3 and os.path.exists(tomp3):
                time.sleep(5)  # Delay 5 seconds before deletion
                os.remove(tomp3)

    return JsonResponse({'error': 'No audio file received'}, status=400)

# views.py
import base64
import os
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def save_image(request):
    if request.method == 'POST':
        try:
            # Get the image data from the request
            data = request.body.decode('utf-8')
            image_data = base64.b64decode(data.split(',')[1])  # Get the image part of the base64 string
            
            # Define the folder where images will be saved
            folder = os.path.join(settings.MEDIA_ROOT, 'captured_images')
            os.makedirs(folder, exist_ok=True)

            # Create a unique filename
            filename = f"student+{time.now}.jpg"
            file_path = os.path.join(folder, filename)

            # Write the image to a file
            with open(file_path, 'wb') as file:
                file.write(image_data)

            return JsonResponse({'message': 'Image saved successfully', 'filename': filename}, status=200)

        except Exception as e:
            return JsonResponse({'message': str(e)}, status=500)

    return JsonResponse({'message': 'Invalid request'}, status=400)

# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import User
from django.contrib import messages

User = get_user_model()

def teacher_student(request):
    search_query = request.GET.get("search", "")
    students = User.objects.filter(user_type="student")

    if search_query:
        students = students.filter(first_name__icontains=search_query)

    return render(request, "teacher/student_detail.html", {
        "students": students
    })
def landing(request):
    return render(request, 'index.html')

def register_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_type = request.POST.get('user_type')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect('login')

        user = User(name=name, email=email, user_type=user_type)
        user.set_password(password)
        user.save()
        login(request, user)
        return redirect('dashboard')  # Redirect to dashboard after registration

    return render(request, 'register.html')

@login_required
def register_student(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")

        # Check if the user already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect('teacher_student')

        # Create the user with user_type=student (you may be using a custom user model)
        user = User.objects.create(
            name=name,
            email=email,
            password=make_password("student123"),  # Default password
            user_type="student"
        )
        messages.success(request, "Student registered successfully.")
        return redirect('teacher_student')
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages

def login_student_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        print("Login attempt:", email, password)

        user = authenticate(request, username=email, password=password)

        if user is not None:
            print("User found:", user)
            if user.user_type == 'student':
                login(request, user)
                return redirect('dashboard_student')
            else:
                messages.error(request, "Access denied. Only students can log in here.")
        else:
            print("Authentication failed")
            messages.error(request, "Invalid email or password.")

    return render(request, 'login_student.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')  # This works now
        else:
            messages.error(request, "Invalid credentials.")
            return redirect('login')

    return render(request, 'login.html')

import os
import time
from django.http import JsonResponse

import os
import time
from django.shortcuts import render
from django.http import JsonResponse

def notes_view_student(request):
    file_count, filenmaes = extract_filenames(folder_path="sathi/functions/teacher")
    context = {'notes': filenmaes}
    print(context)

    if request.method == 'POST' and request.FILES.get('audio_file'):
        audio_file = request.FILES['audio_file']
        tomp3 = None
        try:
            # Convert uploaded file to WAV
            tomp3 = convert_to_wav(audio_file)

            # Transcribe the audio
            texts = transcribe_audio_file(tomp3)

            # Find what command it matches
            commands = listen_and_respond_pdf(texts)

            folder_path = "sathi/functions/mp3"
            matching_file = None

            # List all files in folder and match with command
            for file in os.listdir(folder_path):
                filename_without_ext = os.path.splitext(file)[0]
                if filename_without_ext.lower() == commands.lower():
                    matching_file = os.path.join(folder_path, file)
                    break

            if matching_file:
                speak(matching_file)
                context['success'] = True
                context['message'] = f'Found and read file: {os.path.basename(matching_file)}'
            else:
                context['success'] = False
                context['error'] = 'No matching file found for the command.'

        except Exception as e:
            context['success'] = False
            context['error'] = str(e)

        finally:
            if tomp3 and os.path.exists(tomp3):
                time.sleep(5)
                os.remove(tomp3)

        # After processing, render a template with context
        return render(request, 'student_notes.html', context)

    # If GET request or no file uploaded
    context['success'] = False
    context['error'] = 'No audio file received.'
    return render(request, 'student_notes.html', context)

@csrf_exempt
def stop_music(request):
    if request.method == 'POST':
        try:
            pygame.mixer.music.stop()
            return JsonResponse({'success': True, 'message': 'Music stopped.'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request'}, status=400)


def dashboard_view_student(request):
    return render(request, 'student_dashboard.html')

def make_notes_view_student(request):
    return render(request, 'student_make_notes.html')





from .models import Question
from django.contrib.auth.decorators import login_required

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse
import os, time

@login_required
def ask_view_student(request):
    if request.method == 'POST' and request.FILES.get('audio_file'):
        audio_file = request.FILES['audio_file']
        tomp3 = None
        try:
            # Convert audio file to WAV format if necessary
            tomp3 = convert_to_wav(audio_file)

            # Transcribe audio to text
            texts = transcribe_audio_file(tomp3)
            print("done")

            # Save the transcribed text to the Question model
            Question.objects.create(
                user=request.user,
                name=request.user.name,  # or any name you want
                question=texts
            )

            return JsonResponse({'success': True, 'message': 'Audio processed, text saved successfully, and question saved to database.'})
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        
        finally:
            if tomp3 and os.path.exists(tomp3):
                time.sleep(5)  # Delay 5 seconds before deletion
                os.remove(tomp3)
    
    else:
        
        return render(request, 'student_ask.html')  # ➔ your template



def get_all_questions(request):
    questions = Question.objects.filter(user=request.user).values('name', 'question')
    print(questions)
    return JsonResponse(list(questions), safe=False)

@login_required
def dashboard_view(request):
    return render(request, 'teacher_dashboard.html', {'User': request.user})

def teacher_student_add_view(request):
    return render(request, 'teacher_add.html')

def teacher_notes(request):
    return render(request, 'teacher_notes.html')

def logout_view(request):
    logout(request)
    return redirect('login')