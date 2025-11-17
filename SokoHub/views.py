from django.shortcuts import render

def home(request):
    return render(request, 'SokoHub/home.html') 
