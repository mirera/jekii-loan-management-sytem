from django.urls import path
from . import views


urlpatterns = [
    path('members', views.listMembers, name='members'),
    path('create-member', views.createMember, name='create-member'),
    path('edit-member/<str:pk>', views.editMember, name='edit-member'),
    path('view-member/<str:pk>', views.viewMember, name='view-member'),
    path('delete-member/<str:pk>', views.deleteMember, name='delete-member'),
]