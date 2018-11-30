from django.contrib.auth import authenticate, logout, login
from django.contrib.sessions.backends import file
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from django.template import loader

from voluntariat.forms import LoginForm, SignUpForm
from voluntariat.models import User


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=raw_password)
            if user is not None:
                login(request, user)
                return redirect('voluntariat:index')
            else:
                return render(request, 'login.html', {
                    'message': 'Invalid credentials',
                    'form': LoginForm()
                }, status=400)
    else:
        form = LoginForm()
    return render(request, 'signup.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('voluntariat:index')
        else:
            return render(request, 'signup.html', {'form': SignUpForm()}, status=400)
    else:
        return render(request, 'signup.html', {'form': SignUpForm()})

def index(request):
    return render(request, 'board_index.html', {
        'user': request.user
    })

def logout_view(request):
    logout(request)
    return redirect('voluntariat:index')
