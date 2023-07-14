from django.urls import path
from . import views

urlpatterns = [
    path('', views.apiEndpoints),
    path('members', views.getMembers),
    path('loans', views.getLoans),
    path('companies', views.getCompanies),
    path('loans/<int:company_id>/', views.getCompanyLoans),
    path('company/sms-templates/<int:company_id>/', views.getCompanySmsTemplates),
    path('members/<int:company_id>/', views.getCompanyMembers),
    path('expenses/<int:company_id>/', views.getCompanyExpense),
    path('income-expense/<int:company_id>/', views.getCompanyIncomExpense),
    path('loans-repayment/<int:company_id>/', views.getCompanyLoansRepayments),
    path('disbursement-data/<int:company_id>/', views.getCompanyLoansDisbursement), 
] 