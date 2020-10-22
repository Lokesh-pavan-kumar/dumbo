from django.shortcuts import render, redirect
from .admin import DumboUserCreationForm
from .forms import DumboUserLoginForm
from django.contrib.auth import login, logout


# Create your views here.
def register(request):  # This view is used to register new users into the application
    if request.method == 'POST':
        form = DumboUserCreationForm(request.POST)  # The form used for saving/creating the new users
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')  # Get the username, can be used later to display a message
            print(f'Registration successful for {username}')
            return redirect('login')  # Redirect to the login page after a successful registration
    else:
        form = DumboUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = DumboUserLoginForm(request.POST)  # The form used to authenticate our users
        if form.is_valid():
            user_object = form.cleaned_data.get('user_object')
            print(f'Login successful for {user_object}')
            # Users can be authenticated into the site either by using
            # their email and username since for a user both are unique
            # and can be used to identified the user
            login(request, user_object, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('landingpage')
    else:
        form = DumboUserLoginForm()
    return render(request, 'accounts/login.html', {'form': form})
