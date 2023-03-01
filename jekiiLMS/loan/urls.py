from django.urls import path
from . import views


urlpatterns = [
    path('loan-products', views.listLoanProducts, name='loan-products'),
    path('create-loan-product', views.createLoanProduct, name='create-loan-product'),
    # path('edit/<str:pk>', views.editLoanProduct, name='edit'),
    path('view-loan-product/<str:pk>', views.viewLoanProduct, name='view-loan-product'),
    # path('delete/<str:pk>', views.deleteLoanProduct, name='delete'),
]