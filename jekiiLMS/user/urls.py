from django.urls import path
from . import views

urlpatterns = [
    path('login', views.user_login, name='login'),
    path('register', views.user_signup, name='register'),
    path('forgot_password', views.forgot_password, name='forgot_password'),
    path('resetpass_email_send', views.resetpass_email_send, name='resetpass_email_send'),
    path('render_reset_form', views.render_reset_form, name='render_reset_form'),
    path('password_reset/<str:pk>/<str:token>', views.password_reset, name='password_reset'),
    path('logout', views.user_logout, name='logout'), 

    #adding user
    path('add-staff', views.addStaff, name='add-staff'),
    path('staffs', views.listStaff, name='staffs'),
    path('user-profile', views.update_user_profile, name='profile'),
    path('view-staff/<str:pk>', views.view_staff, name='view-staff'),  
    path('delete-staff/<str:pk>', views.deleteStaff, name='delete-staff'), 
    path('update-staff/<str:pk>', views.updateStaff, name='update-staff'), 
    path('deactivate-staff/<str:pk>', views.deactivateStaff, name='deactivate-staff'),
    path('activate-staff/<str:pk>', views.activateStaff, name='activate-staff'),
    path('change-photo', views.change_photo, name='change-photo'),

    #-- roles url
    path('add-role', views.addRole, name='add-role'),
    path('edit-role/<str:pk>', views.editRole, name='edit-role'),
    path('roles-list', views.rolesList, name='roles-list'),
    path('delete-role/<str:pk>', views.deleteRole, name='delete-role'),

    #--notifications
    path('<str:pk>/read-notification', views.mark_notfications_read, name='mark-read'),
]
