from django.urls import path
from . import views


urlpatterns = [
    path('create-member', views.createMember, name='create-member'),
    path('edit-member/<str:pk>', views.editMember, name='edit-member'),
    path('view-member/<str:pk>', views.viewMember, name='view-member'),
    path('members', views.listMembers, name='members'),
    path('blacklisted-members', views.blacklisted_members, name='blacklisted-members'),
    path('delete-member/<str:pk>', views.deleteMember, name='delete-member'), 
    path('sms-member/<str:pk>', views.sms_member, name='sms-member'),    

]


