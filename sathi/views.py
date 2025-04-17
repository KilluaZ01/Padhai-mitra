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
from .functions.Voicecommand import listen_and_respond
from .functions.TTS import speak
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

import uuid
import time
import os
from django.http import JsonResponse

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


def notes_view_student(request):
    notes = [
        {'date': '04 Apr 2025', 'subject': 'Science', 'title': 'Vertebrates & Invertebrates'},
        {'date': '04 Apr 2025', 'subject': 'Social', 'title': 'Raja Hatyakanda'},
        {'date': '04 Apr 2025', 'subject': 'English', 'title': 'Pronouns'},
    ]
    return render(request, 'student_notes.html', {'notes': notes})

def dashboard_view_student(request):
    return render(request, 'student_dashboard.html')

def make_notes_view_student(request):
    return render(request, 'student_make_notes.html')

def ask_view_student(request):
    return render(request, 'student_ask.html')

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