from django.urls import path
from . import views


urlpatterns = [
    path('loan-products', views.listLoanProducts, name='loan-products'),
    path('create-loan-product', views.createLoanProduct, name='create-loan-product'),
    path('edit-loan-product/<str:pk>', views.editLoanProduct, name='edit-loan-product'),
    path('view-loan-product/<str:pk>', views.viewLoanProduct, name='view-loan-product'),
    path('delete-loan-product/<str:pk>', views.deleteLoanProduct, name='delete-loan-product'),
]