from django.urls import path
from . import views


urlpatterns = [
    path('list', views.list_branches, name='list'),
    path('create', views.createBranch, name='create'),
    path('edit/<str:pk>', views.editBranch, name='edit'),
    path('view/<str:pk>', views.viewBranch, name='view'),
    path('delete/<str:pk>', views.deleteBranch, name='delete'),
]