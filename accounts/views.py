from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

from accounts.forms import LoginForm
from accounts.models import UserRoles


def register(request):
    if request.method == 'POST':
        data = request.POST
        user_form = UserCreationForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            profile = user.profile
            profile.full_name = data['name']
            profile.marital_status = data['marital_status']
            profile.gender = data['gender']
            profile.phone_number = data['phone_number']
            profile.date_of_birth = data['date_of_birth']
            profile.save()
            # messages.success(request, 'Account created successfully')
            return redirect("login")
        else:
            pass
            # messages.warning(request, user_form.errors)
    return render(request, 'accounts/register.html')


def police_login(request):
    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )

            if user and user.profile.role == UserRoles.POLICE:
                login(request, user)
                messages.success(request, 'Login successful')
                # messages.info(request, f'Welcome back {user.username}')
                return redirect('police-dashboard')
            else:
                pass
                messages.warning(request, 'Invalid username or password for police account')

    return render(request, 'accounts/police-login.html', {'form': form})
