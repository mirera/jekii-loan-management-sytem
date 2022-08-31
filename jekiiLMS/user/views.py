from django.shortcuts import render


def user_login(request):
    return render (request, 'user/auth-login.html')

def user_signup(request):
    return render (request, 'user/auth-register.html')
