from django.contrib.auth import authenticate, logout, login
from django.contrib.sessions.backends import file
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from django.template import loader

from voluntariat.models import User


def login_view(request):
    if request.method == 'POST':
        # User.objects.create_user('antal', 'crgroot97@gmail.com', '1234', age=20)
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            return redirect('voluntariat:index')
        else:
            return render(request, 'login.html', {
                'message': 'Invalid credentials'
            })
    # No backend authenticated the credentials
    return render(request, 'login.html', {})

def signup(request):
    if request.method == 'POST':
        # User.objects.create_user('antal', 'crgroot97@gmail.com', '1234', age=20)
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        age = request.POST['age']

        # TODO validations etc
        try:
            user = User.objects.create_user(username, email, password, age=age)
            return HttpResponse('OK')
        except Exception as why:
            return HttpResponse("Not OK")

    return render(request, 'signup.html', {})

def index(request):
    return render(request, 'board_index.html', {
        'user': request.user
    })

def logout_view(request):
    logout(request)
    return redirect('voluntariat:index')
