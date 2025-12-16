from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout, get_user_model
from django.contrib import messages
from .forms import RegistrationForm, LoginForm
from django.contrib.auth.decorators import login_required

User = get_user_model()


def welcome(request):
    return render(request, 'base.html')


def logout_view(request):
    auth_logout(request)
    return redirect('home_page')


def login_view(request):
    form = LoginForm(request.POST or None)
    error = None
    if request.method == 'POST' and form.is_valid():
        identifier = form.cleaned_data['email']
        password = form.cleaned_data['password']

        # allow login via username or email
        try:
            user_obj = User.objects.filter(email__iexact=identifier).first()
            username = user_obj.username if user_obj else identifier
        except Exception:
            username = identifier

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            # redirect based on role
            if getattr(user, 'user_type', '') == 'vendor':
                return redirect('products:product_list')
            else:
                return redirect('products:product_list')
        else:
            error = 'Invalid credentials. Please try again.'

    return render(request, 'login.html', {'form': form, 'error': error})


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
                    password=password,
                )
                user.user_type = user_type
                user.phone = phone
                user.location = location
                user.save()

                # auto-login and redirect based on role
                auth_login(request, user)
                if user.user_type == 'vendor':
                    return redirect('products:product_list')
                return redirect('products:product_list')

            except Exception as e:
                messages.error(request, f'An error occurred during registration: {e}')
    else:
        form = RegistrationForm()
    return render(request, 'registration.html', {'form': form})


@login_required
def profile_view(request):
    from .forms import ProfileForm
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            u = request.user
            u.username = form.cleaned_data['username']
            u.email = form.cleaned_data['email']
            u.phone = form.cleaned_data.get('phone', '')
            u.location = form.cleaned_data.get('location', '')
            u.save()
            messages.success(request, 'Profile updated.')
            return redirect('accounts:profile')
    else:
        form = ProfileForm(initial={
            'username': request.user.username,
            'email': request.user.email,
            'phone': getattr(request.user, 'phone', ''),
            'location': getattr(request.user, 'location', ''),
        })
    return render(request, 'profile.html', {'form': form})




