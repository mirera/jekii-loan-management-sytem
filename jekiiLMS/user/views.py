# from email import message
# import email

from multiprocessing import context
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm
from django.contrib import messages


#---user login in logic starts here---

def user_login(request):
    #preventing logged in useres from logging in again
    if request.user.is_authenticated:
        return redirect('home')

    #extracting login credential from login form
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        #raise username do not exist in our databse error
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'This username does not exist on our database!')

        # check if email and password match to autheticate
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            #return error message
            messages.error(request, 'The username or password is incorrect')
            
    return render (request, 'user/auth-login.html')

#---user login in logic ends here---


#---user register  logic starts here---

def user_signup(request):
    form = CustomUserCreationForm()
    if request.method == 'POST':

        #binding data from fields to the form
        form = CustomUserCreationForm(request.POST)

        #performing validation
        if form.is_valid():

            #save user but no commit before lowercasing the username
            user = form.save(commit=False)
            # user.username = user.username.lower()
            user.save()
            login(request, user)
            messages.success(request, 'User created successfully!')
            return redirect('home')
        else:
            #return error message
            messages.error(request, 'An error occured during regetration, please try again!')

    context= {form:'form'}

    return render (request, 'user/auth-register.html', context)

#---user register  logic ends here---

def password_reset(request):
    return render(request, 'user/auth-reset.html')

def user_logout(request):
    logout(request)
    return redirect('home')
 