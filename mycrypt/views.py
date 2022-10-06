from django.shortcuts import redirect, render
from django.http import Http404, HttpResponse
from django.contrib.sessions.backends.base import *
from django.contrib.auth.hashers import make_password
from passlib.handlers.django import django_pbkdf2_sha256
from django.views.decorators.clickjacking import xframe_options_deny
from mycrypt.forgot import ForgotForm
import requests
import json
from . import *
from .models import Content, User
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from mycrypt.token import *
import datetime


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


def post(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        body = request.POST.get('body')
        source = request.POST.get('url')
        status = request.POST.get('status')
        user = request.session['user']
        date = datetime.datetime.now().date()
        post = Content(title=title, body=body, source=source,
                       status=status, author=user, date=date)
        post.save()
    return render(request, 'mycrypt/post.html',)


def coins(request, coin_name):
    param = {'current_user': request.session['user'],
             }
    return render(request, 'mycrypt/coins.html', param)


def signUp(request):
    if request.method == 'POST':
        uname = request.POST.get('uname')
        pwd = request.POST.get('pwd')
        pwd2 = request.POST.get('pwd2')
        rl = request.POST.get('role')
        mail = request.POST.get('email')
        if User.objects.filter(userName=uname).exists() | User.objects.filter(email=mail).exists():
            return render(request, 'mycrypt/signup.html', {
                'message': "The account has been registered, please use different Email or user name"})
        if pwd != pwd2:
            return render(request, 'mycrypt/signup.html', {
                'message': 'The password are not the same'})
        else:
            user = User(userName=uname, passWord=make_password(
                pwd), role=rl, email=mail)
            user.save()
            return redirect('/mycrypt/login/')
    else:
        return render(request, 'mycrypt/signup.html',)


def logIn(request):
    if request.method == 'POST':
        uname = request.POST.get('uname')
        pwd = request.POST.get('pwd')
        if User.objects.filter(userName=uname).exists():
            userCheck = User.objects.get(userName=uname)
            if (django_pbkdf2_sha256.verify(pwd, userCheck.passWord)):
                request.session['user'] = uname
                return redirect('/mycrypt/home/', {
                    'user_name': uname,
                })
            return render(request, 'mycrypt/login.html', {"message": "Wrong pass"})
        return render(request, 'mycrypt/login.html', {"message": "Account does not existed"})
    if 'user' in request.session:
        return redirect('/mycrypt/home/')
    return render(request, 'mycrypt/login.html')


def resetPass(request, uid64, token):
    if 'account' in request.session:
        if request.method == 'POST':
            account = request.session['account']
            pwd = request.POST.get('pwd')
            user = User.objects.get(userName=account)
            user.passWord = make_password(pwd)
            user.save()
            request.session.flush()
    else:
        return Http404('This page is restricted !')
    return render(request, 'mycrypt/reset.html')


def link(request, uidb64, token):
    try:
        id = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(userName=id)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and tokenGener.check_token(user, token):
        request.session['account'] = user.userName
        return render(request, 'mycrypt/reset.html', {
            'uidb64': uidb64, 'token': token,
            'user': user.userName
        })


def forgot(request):
    if request.method == 'POST':
        form = ForgotForm(request.POST)
        current_site = get_current_site(request)
        if form.is_valid():
            form.send(current_site)
            return render(request, 'mycrypt/login.html')
    else:
        form = ForgotForm()
    return render(request, 'mycrypt/forgot.html', {'form': form})


def learn(request):
    if 'user' in request.session:
        return render(request, 'mycrypt/learn.html')
    return redirect('/mycrypt/login/')


def watchlist(request):
    if 'user' in request.session:
        default_period = "24h"
        current_user = request.session['user']
        userCheck = User.objects.get(userName=current_user)
        if(request.method == 'POST'):
            if 'period' in request.POST:
                period = request.POST.get('period')
                default_period = period
        return render(request, 'mycrypt/watchlist.html', {
            'current_user': current_user,
            'icon': coinData(default_period),
            'period': default_period,
            'role': userCheck.role
        })
    else:
        return render(request, 'mycrypt/watchlist.html')


def logOut(request):
    try:
        request.session.flush()
    except:
        return redirect('/login/')
    return redirect('/mycrypt/login/')
