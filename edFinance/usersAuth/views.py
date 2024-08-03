# views.py
from django.contrib.auth import logout
from django.shortcuts import redirect, render
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login

def registerUser(request):
    if request.method == "POST":
        registerForm = CustomUserCreationForm(request.POST)
        if registerForm.is_valid():
            user = registerForm.save()
            auth_login(request, user)  # Use the correct login function
            return redirect('home')
    else:
        # Handle the case where authentication fails
        registerForm = CustomUserCreationForm()
        context = {'register_form': registerForm}
        return render(request, 'usersAuth/register_user.html', context)

def loginUser(request):
    if request.method == "POST":
        usernameEntered = request.POST.get("username")
        passwordEntered = request.POST.get("password")
        user = authenticate(request, username=usernameEntered, password=passwordEntered)
        if user is not None:  # Check if authentication was successful
            auth_login(request, user)
            return redirect('home')
        else:
            # Handle the case where authentication fails
            context = {'error': 'Invalid username or password'}
            return render(request, 'usersAuth/login_user.html', context)
    return render(request, 'usersAuth/login_user.html')


def logoutUser(request):
    logout(request)
    return redirect('home')
