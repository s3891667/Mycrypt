from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.conf import settings
from django.template import loader
from .models import *


def index(request):
    return render(request, 'mycrypt/index.html')


def home(request):
    if not request.user.is_authenticated:
        return render(request, 'mycrypt/index.html')
    else:
        return redirect('mycrypt/home.html')


def logIn(request):
    userName = request.POST['username']
    pw = request.POST['password']
    user = authenticate(request, userName=userName, pw=pw)

    if user is not None:
        login(request, user)
        return redirect('mycrypt/home.html')
    else:
        return HttpResponse("Please check your account again! ")


def logOut(request):
    logout(request)
    return redirect('mycrypt/index.html')


def signUp(request):
    print("helloworld")
