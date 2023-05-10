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
    path('view-loan/<str:pk>/write-off', views.writeOff, name='write-off'),

    #repayment urls
    path('repayments', views.listRepayments, name='repayments'),
    path('create-repayment', views.createRepayment, name='create-repayment'),
    path('edit-repayment/<str:pk>', views.editRepayment, name='edit-repayment'),
    path('delete-repayment/<str:pk>', views.deleteRepayment, name='delete-repayment'),

    path('view-loan/<str:pk>/add-repayment', views.addRepayment, name='add-repayment'),

    #guarantor urls
    path('view-loan/<str:pk>/add-guarantor', views.addGuarantor, name='add-guarantor'),
    path('view-loan/<str:pk>/remove-guarantor/<str:guarantor_id>', views.removeGuarantor, name='remove-guarantor'),

    #collateral urls
    path('view-loan/<str:pk>/add-collateral', views.addCollateral, name='add-collateral'),
    path('edit-collateral/<str:pk>', views.editCollateral, name='edit-collateral'),
    path('view-loan/<str:pk>/remove-collateral/<str:collateral_id>', views.removeCollateral, name='remove-collateral'),

    #mpesa Statment urls
    path('view-loan/<str:pk>/add-statement', views.addStatement, name='add-statement'),
    path('view-loan/<str:pk>/analyse-statement', views.analyseStatement, name='analyse-statement'),

    #loan calculator url
    path('loancalculator', views.loan_calculator, name='loancalculator'), 

    # daraja  api url
    path('api/b2c-result', views.b2c_result, name='b2c-result'),
    path('api/b2c-timeout', views.b2c_timeout, name='b2c-timeout'), 
    path('api/repayment-callback', views.repayment_callback, name='repayment-callback'),



] 
