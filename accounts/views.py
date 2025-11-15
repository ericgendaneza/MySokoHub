from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
# Create your views here.

def welcome(request):
    return render(request, 'base.html')
def login(request):
    return render(request,'login.html')