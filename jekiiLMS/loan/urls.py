from django.urls import path
from . import views


urlpatterns = [
    #loan product urls
    path('loan-products', views.listLoanProducts, name='loan-products'),
    path('create-loan-product', views.createLoanProduct, name='create-loan-product'),
    path('edit-loan-product/<str:pk>', views.editLoanProduct, name='edit-loan-product'),
    path('view-loan-product/<str:pk>', views.viewLoanProduct, name='view-loan-product'),
    path('delete-loan-product/<str:pk>', views.deleteLoanProduct, name='delete-loan-product'),

    #loan urls
    path('loans', views.listLoans, name='loans'),
    path('create-loan', views.createLoan, name='create-loan'),
    path('edit-loan/<str:pk>', views.editLoan, name='edit-loan'),
    path('view-loan/<str:pk>', views.viewLoan, name='view-loan'),
    path('delete-loan/<str:pk>', views.deleteLoan, name='delete-loan'),
]
