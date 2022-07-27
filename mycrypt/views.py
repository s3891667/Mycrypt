from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.template import loader
from .models import *
from django.contrib.auth.hashers import make_password
from passlib.handlers.django import django_pbkdf2_sha256


def index(request):
    if 'user' in request.session:
        return redirect('home/')
    else:
        return render(request, 'mycrypt/index.html')


def home(request):
    if 'user' in request.session:
        current_user = request.session['user']
        param = {'current_user': current_user}
        return render(request, 'mycrypt/home.html', param)
    else:
        # return redirect('/mycrypt/')
        return redirect('login/')
    return render(request, 'mycrypt/login.html')


def signUp(request):
    if request.method == 'POST':
        uname = request.POST.get('uname')
        pwd = request.POST.get('pwd')
        # print(uname, pwd)
        if User.objects.filter(userName=uname).count() > 0:
            return HttpResponse('userName already exists.')
        else:
            user = User(userName=uname, passWord=make_password(pwd))
            user.save()
            return redirect('/mycrypt/login/')
    else:
        return render(request, 'mycrypt/signup.html')


def logIn(request):
    if request.method == 'POST':
        uname = request.POST.get('uname')
        pwd = request.POST.get('pwd')
        # hash_verify = django_pbkdf2_sha256.verify()
        check_user = User.objects.filter(
            userName=uname, passWord=make_password(pwd))
        if check_user:
            request.session['user'] = uname
            return redirect('/mycrypt/home/')
        else:
            return HttpResponse('Please enter valid userName or passWord.')

    return render(request, 'mycrypt/login.html')


def logOut(request):
    try:
        del request.session['user']
    except:
        return redirect('/login/')
    return redirect('/mycrypt/login/')
