from django.urls import path
from . import views

urlpatterns = [
    path('login', views.user_login, name='login'),
    path('register', views.user_signup, name='register'),
    path('password_reset', views.password_reset, name='password_reset'),
    path('logout', views.user_logout, name='logout')


]
