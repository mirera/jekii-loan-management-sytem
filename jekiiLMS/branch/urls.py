from django.urls import path
from . import views


urlpatterns = [
    path('list', views.list_branches, name='list'),
    path('create', views.createBranch, name='create'),
    # path('branch/edit', views.registerPage, name='edit'),
    # path('branch/delete', views.registerPage, name='delete'),
]