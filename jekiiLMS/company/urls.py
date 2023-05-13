from django.urls import path
from . import views


urlpatterns = [
    #organization urls
    path('update/<str:pk>', views.updateOrganization, name='update-organization'), 
    #path('create-company', views.createCompany, name='create-company'),
    #path('edit-package', views.editPackage, name='edit-package'),
    #path('remove-package', views.removePackage, name='remove-package'),
    path('companies', views.listCompanies, name='companies'),
    path('sms/<str:pk>', views.updateSms, name='update-sms'),
    path('mpesa/<str:pk>', views.updateMpesa, name='update-mpesa'),
    path('email/<str:pk>', views.updateEmail, name='update-email'),
    path('test-email/<str:pk>', views.sendTestEmail, name='test-email'),


    #package urls
    path('create-package', views.createPackage, name='create-package'),
    #path('edit-package', views.editPackage, name='edit-package'),
    #path('remove-package', views.removePackage, name='remove-package'),
    path('packages', views.listPackages, name='packages'),
] 