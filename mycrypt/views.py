from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.conf import settings
from django.template import loader
from mycrypt.forms import UserForm
from mycrypt.validators import NumberValidator
from .models import User
from django.contrib.auth.hashers import make_password
from passlib.handlers.django import django_pbkdf2_sha256
from django.views.decorators.clickjacking import xframe_options_deny
from . import *

# To protect the website from being emmbed


@xframe_options_deny
def view_one(request):
    return HttpResponse("Stop doing this !")


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
        return redirect('/mycrypt/login/')


def signUp(request):
    if request.method == 'POST':
        uname = request.POST.get('uname')
        pwd = request.POST.get('pwd')
        rl = request.POST.get('role')
        pwd2 = request.POST.get('pwd2')
        if User.objects.filter(userName=uname).count() > 0:
            return HttpResponse('userName already exists.')
        if pwd != pwd2:
            return HttpResponse('passWord does not match.')
        else:
            user = User(userName=uname, passWord=make_password(pwd), role=rl)
            user.save()
            return redirect('/mycrypt/login/')
    else:
        return render(request, 'mycrypt/signup.html')


def logIn(request):
    if request.method == 'POST':
        uname = request.POST.get('uname')
        pwd = request.POST.get('pwd')
        userCheck = User.objects.get(userName=uname)
        if (userCheck.userName == uname) and (django_pbkdf2_sha256.verify(pwd, userCheck.passWord)):
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
