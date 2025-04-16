# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import User
from django.contrib import messages

<<<<<<< HEAD
def test(request):
    return render(request,"test.html")


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from .functions.STT import transcribe_audio_file,convert_to_wav
from .functions.Voicecommand import listen_and_respond

from django.urls import reverse


@csrf_exempt
def upload_audio(request):
    if request.method == 'POST' and request.FILES.get('audio_file'):
            audio_file = request.FILES['audio_file']
            tomp3 = convert_to_wav(audio_file)
            texts = transcribe_audio_file(tomp3)
            textlast = listen_and_respond(command=texts)
            print(textlast)
            if textlast == "MakeNotes":
                print("hello")
                return JsonResponse({'redirect': '/Homepage/'})



# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import User
from django.contrib import messages

=======
>>>>>>> a6510effefeb436d93ffaefc27ef1a07b424284b
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

def login_student_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')  # You can change this to a student dashboard if needed
        else:
            messages.error(request, "Invalid credentials.")
            return redirect('login_student')

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