from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.sessions.backends.base import *
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password
from passlib.handlers.django import django_pbkdf2_sha256
from django.views.decorators.clickjacking import xframe_options_deny
import requests
import json
from . import *
from .models import User


def coinData(period):
    output = []
    for i in range(1, 3):
        response_API = requests.get(
            'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=100&page='
            + str(i) + '&sparkline=false&price_change_percentage=' + period)
        data = response_API.text
        parse_json = json.loads(data)
        output.extend(parse_json)
    return output

hiiii
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
        default_period = "24h"
        current_user = request.session['user']
        userCheck = User.objects.get(userName=current_user)
        if(request.method == 'POST'):
            if 'period' in request.POST:
                period = request.POST.get('period')
                default_period = period
        return render(request, 'mycrypt/home.html', {
            'current_user': current_user,
            'icon': coinData(default_period),
            'period': default_period,
            'role': userCheck.role
        })
    else:
        return redirect('/mycrypt/login/')


def coins(request,coin_name):
    param = {'current_user': request.session['user'],
             }
    return render(request, 'mycrypt/coins.html', param)


def signUp(request):
    if request.method == 'POST':
        uname = request.POST.get('uname')
        pwd = request.POST.get('pwd')
        rl = request.POST.get('role')
        if User.objects.filter(userName=uname).count() > 0:
            return render(request, 'mycrypt/signup.html', {
                'message': "The account has been registered"})
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
    if 'user' in request.session:
        return redirect('/mycrypt/home/')
    return render(request, 'mycrypt/login.html')


def forgot(request):
    if request.method == 'POST':
        send_mail(
            'Forgot password',
            'Message',
            fail_silently=False,
        )
    return render(request, 'mycrypt/forgot.html')


def learn(request):
    return render(request, 'mycrypt/learn.html')


def watchlist(request):
    return render(request, 'mycrypt/watchlist.html')


def logOut(request):
    try:
        request.session.flush()
    except:
        return redirect('/login/')
    return redirect('/mycrypt/login/')
