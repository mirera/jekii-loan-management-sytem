from email import message
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import UserCreationFormWithEmail
from django.contrib import messages


#---user login in logic starts here---

def user_login(request):
    #preventing logged in useres from logging in again
    if request.user.is_authenticated:
        return redirect('home')

    #extracting login credential from login form
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        #raise email do not exist in our databse error
        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'This email does not exist on our database!')

        # check if email and password match to autheticate
        user = authenticate(email=email, password=password)

        if user is not None:
            login(request, user)
        else:
            #return error message
            messages.error(request, 'The email or password is incorrect')
            
    return render (request, 'user/auth-login.html')

#---user login in logic ends here---


#---user register  logic starts here---

def user_signup(request):
    form = UserCreationFormWithEmail()
    if request.method == 'POST':

        #binding data from fields to the form
        form = UserCreationFormWithEmail(request.POST)

        #performing validation
        if form.is_valid():

            #save user but no commit before lowercasing the username
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.email = user.email.lower()
            user.save()
            
            login(request, user)
            return redirect('home')
        else:
            #return error message
            messages.error(request, 'An error occured during regetration, please try again!')

    return render (request, 'user/auth-register.html')

#---user register  logic ends here---

def password_reset(request):
    return render(request, 'user/auth-reset.html')

def user_logout(request):
    logout(request)
    return redirect('home')
