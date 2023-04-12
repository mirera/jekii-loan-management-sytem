"""jekiiLMS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from django.conf import settings 
from django.conf.urls.static import static  
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('loan/', include('loan.urls')),
    path('member/', include('member.urls')),
    path('user/', include('user.urls')),
    path('branch/', include('branch.urls')),
    path('company/', include('company.urls')),
    path('',views.homepage, name='home'),  #path('companyadmin/dashboard/', views.companyadmin_dashboard, name='companyadmin_dashboard'),

    #dashboards
    path('superadmin/dashboard', views.superadmin_dashboard, name='superadmin_dashboard'),
    #path('staff/dashboard', views.staff_dashboard, name='staff_dashboard'), --- moved to user urls
]
#extend the url pattern to cater for media urls
urlpatterns += static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
