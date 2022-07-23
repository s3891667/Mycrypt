from django.shortcuts import render
from django.contrib.auth import authenticate,login
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def logIn(request):
    userName = request.POST['username']
    pw = request.POST['password']
    user = authenticate(request,userName = userName,pw = pw)
    
    if user is not None : 
        login(request,user)
        
# def logout(request):
# def signUp(request):

