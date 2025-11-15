from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def welcome(request):
    return HttpResponse('<h1>Welcome to SokoHub!</h1>')
def login(request):
    return HttpResponse('<h1>This is login Page</h1>')