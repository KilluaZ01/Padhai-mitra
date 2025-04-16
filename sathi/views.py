# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import User
from django.contrib import messages

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

        user = User(name=name, email=email, user_type='teacher')
        user.set_password(password)
        user.save()
        login(request, user)
        return redirect('login')

    return render(request, 'register.html')

def login_student_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('Homepage')
        else:
            messages.error(request, "Invalid credentials.")
            return redirect('login')

    return render(request, 'login_student.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('login')
        else:
            messages.error(request, "Invalid credentials.")
            return redirect('dashboard')

    return render(request, 'login.html')


def dashboard_view(request):
    return render(request, 'teacher_dashboard.html', {'user': request.user})


def logout_view(request):
    logout(request)
    return redirect('login')
