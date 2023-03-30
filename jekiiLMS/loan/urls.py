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

    path('view-loan/<str:pk>/approve', views.approveLoan, name='approve'),
    path('view-loan/<str:pk>/reject', views.rejectLoan, name='reject'),

    #repayment urls
    path('repayments', views.listRepayments, name='repayments'),
    path('create-repayment', views.createRepayment, name='create-repayment'),
    path('edit-repayment/<str:pk>', views.editRepayment, name='edit-repayment'),
    path('delete-repayment/<str:pk>', views.deleteRepayment, name='delete-repayment'),

    #guarantor urls
    path('view-loan/<str:pk>/add-guarantor', views.addGuarantor, name='add-guarantor'),
    path('view-loan/<str:pk>/remove-guarantor', views.removeGuarantor, name='remove-guarantor'),

    #collateral urls
    path('view-loan/<str:pk>/add-collateral', views.addCollateral, name='add-collateral'),
    path('edit-collateral/<str:pk>', views.editCollateral, name='edit-collateral'),
    #path('remove-collateral/<str:pk>', views.removeCollateral, name='remove-collateral'),

    #loan calculator url
    path('loancalculator', views.loan_calculator, name='loancalculator'), 

] 
