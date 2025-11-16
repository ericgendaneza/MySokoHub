from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib import messages
from .forms import RegistrationForm 
User = get_user_model()
#from django.contrib.auth.forms import CustomerUserCreationForm
# Create your views here.


def welcome(request):
    return render(request, 'base.html')
def logout(request):
    return render(request, 'base.html')

def login(request):
    if request.method == 'POST':
        form ={'email':request.POST['email'],'password':request.POST['password']}
        if form:
            email = form['email']
            password = form['password']
            user = authenticate(request, username=email, password=password)
            
            if user is not None:
                return redirect('welcome')  
            else:
                message="Invalid email or password. Please try again."
                return render(request,'login.html',{'error':message})
    else:
        return render(request,'login.html')

def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user_type = form.cleaned_data['user_type']
            phone = form.cleaned_data['phone']
            location = form.cleaned_data['location']
            try:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password 
                )
                messages.success(request, 'Registration successful! You can now log in.')
                return redirect('login')
                
            except Exception as e:
                messages.error(request, f'An error occurred during registration: {e}')
    else:
        form = RegistrationForm()
    return render(request, 'registration.html', {'form': form})


        

