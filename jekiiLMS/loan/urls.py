from django.urls import path
from . import views


urlpatterns = [
    # path('list', views.listLoanProduct, name='list'),
    path('create', views.createLoanProduct, name='create'),
    # path('edit/<str:pk>', views.editLoanProduct, name='edit'),
    # path('view/<str:pk>', views.viewLoanProduct, name='view'),
    # path('delete/<str:pk>', views.deleteLoanProduct, name='delete'),
]