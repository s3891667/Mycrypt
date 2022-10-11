from django.db.models import Q
from django.shortcuts import redirect, render
from django.http import Http404, HttpResponse
from django.contrib.sessions.backends.base import *
from django.contrib.auth.hashers import make_password
# from passlib. import django_pbkdf2_sha256
from passlib.handlers.django import django_pbkdf2_sha256
from django.views.decorators.clickjacking import xframe_options_deny
from mycrypt.forgot import ForgotForm
import requests
import json
from . import *
from .models import Coin, Content, User
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from mycrypt.token import *
import datetime
from django.core.paginator import Paginator


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
            else:
                symbol = request.POST.get('symbol')
                coinName = request.POST.get('coinName')
                coinImg = request.POST.get('coinImg')
                if not userCheck.coin.filter(name=coinName).exists():
                    coin = Coin(symbol=symbol, name=coinName, icon=coinImg)
                    coin.save()
                    userCheck.coin.add(coin)
                    userCheck.save()
        # Pagination
        coins = coinData(default_period)
        paginator = Paginator(coins, 25)
        page_number = request.GET.get('page')
        page_object = paginator.get_page(page_number)
        return render(request, 'mycrypt/home.html', {
            'current_user': current_user, 'icon': page_object,
            'period': default_period, 'role': userCheck.role,
            'userCheck': userCheck, 'verified': userCheck.verified,
            'favorite': userCheck.coin.values_list('name', flat=True)
        })
    else:
        return redirect('/mycrypt/login/')


def remove(request):
    if request.method == "POST":
        name = request.POST.get('coin')
        delCoin = Coin.objects.get(name=name)
        delCoin.delete()
    return redirect('/mycrypt/home/')


def post(request):
    if 'user' in request.session:
        current_user = request.session['user']
        current_user = User.objects.get(userName=current_user)
        if request.method == 'POST':
            title = request.POST.get('title')
            body = request.POST.get('body')
            source = request.POST.get('url')
            user = request.session['user']
            date = datetime.datetime.now().date()
            post = Content(title=title, body=body, source=source, status="d",
                           author=user, date=date)
            post.save()
        return render(request, 'mycrypt/post.html', {'current_user': current_user,
                                                     'role': current_user.role,
                                                     'verified': current_user.verified})
    else:
        redirect('mycrypt/login/')


def coins(request, coin_name):
    current_user = request.session['user']
    current_user = User.objects.get(userName=current_user)
    param = {'current_user': request.session['user'],
             'coin_name': coin_name,
             'role': current_user.role,
             'verified': current_user.verified
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
                pwd), role=rl, email=mail, verified=False)
            user.save()
            return redirect('/mycrypt/login/')
    else:
        return render(request, 'mycrypt/signup.html',)


def logIn(request):
    if request.method == 'POST':
        uname = request.POST.get('uname')
        pwd = request.POST.get('pwd')
        if User.objects.filter(userName=uname).exists() | User.objects.filter(email=uname).exists():
            userCheck = User.objects.get(Q(userName=uname) | Q(email=uname))
            if django_pbkdf2_sha256.verify(pwd, userCheck.passWord):
                request.session['user'] = userCheck.userName
                return redirect('/mycrypt/home/', {
                    'user_name': uname,
                })
            return render(request, 'mycrypt/login.html', {"message": "Wrong pass"})
        return render(request, 'mycrypt/login.html', {"message": "Account does not existed"})
    if 'user' in request.session:
        return redirect('/mycrypt/home/')
    return render(request, 'mycrypt/login.html')


def resetPass(request):
    if 'account' in request.session:
        if request.method == 'POST':
            account = request.session['account']
            pwd = request.POST.get('pwd')
            user = User.objects.get(userName=account)
            user.passWord = make_password(pwd)
            user.save()
            request.session.flush()
            return redirect('/mycrypt/login/')
        return render(request, 'mycrypt/reset.html')
    else:
        raise Http404("This site is restricted ! ")


def link(request, uidb64, token):
    try:
        id = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(userName=id)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and tokenGener.check_token(user, token):
        request.session['account'] = user.userName
        return redirect('/mycrypt/reset/')


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
        current_user = request.session['user']
        current_user = User.objects.get(userName=current_user)
        contents = Content.objects.filter(status='p').all().values()
        return render(request, 'mycrypt/learn.html',
                      {'contents': contents,
                       'current_user': current_user,
                       'role': current_user.role,
                       'verified': current_user.verified})
    return redirect('/mycrypt/login/')


def watchlist(request):
    if 'user' in request.session:
        current_user = request.session['user']
        userCheck = User.objects.get(userName=current_user)
        if(request.method == 'POST'):
            if 'period' in request.POST:
                period = request.POST.get('period')
                default_period = period
        return render(request, 'mycrypt/watchlist.html', {
            'current_user': current_user,
            'favorite': userCheck.coin.all(),
            'role': userCheck.role,
            'verified': userCheck.verified
        })
    else:
        return redirect('/mycrypt/login/')


def logOut(request):
    try:
        request.session.flush()
    except:
        return redirect('/login/')
    return redirect('/mycrypt/login/')
