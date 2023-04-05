from django.urls import path
from . import views


urlpatterns = [
    #organization urls
    path('update/<str:pk>', views.updateOrganization, name='update-organization'),
] 