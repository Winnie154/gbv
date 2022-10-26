from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect


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
            messages.success(request, 'Account created successfully')
            return redirect("login")
        else:
            messages.warning(request, user_form.errors)
    return render(request, 'accounts/register.html')
