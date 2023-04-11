from django.urls import path
from . import views

urlpatterns = [
    path('login', views.user_login, name='login'),
    path('register', views.user_signup, name='register'),
    path('password_reset', views.password_reset, name='password_reset'),
    path('logout', views.user_logout, name='logout'),

    #adding user
    path('add-staff', views.addStaff, name='add-staff'),
    path('staffs', views.listStaff, name='staffs'),
    path('user-profile', views.update_user_profile, name='profile'),
]
