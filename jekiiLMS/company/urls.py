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
    path('preferences/<str:pk>', views.updatePreferences, name='preferences'), 
    path('template/<str:pk>', views.updateTemplate, name='update-template'),

    #security settings
    path('disable-2fa/<str:pk>', views.disable_2fa, name='disable-2fa'),
    path('enable-2fa/<str:pk>', views.enable_2fa, name='enable-2fa'),  

    #package urls
    path('create-package', views.createPackage, name='create-package'),
    #path('edit-package', views.editPackage, name='edit-package'),
    #path('remove-package', views.removePackage, name='remove-package'),
    path('packages', views.listPackages, name='packages'),

    #reports and analytics
    path('reports-analytics/loan-portfolio-summary/<str:pk>', views.loan_portfolio_summary, name='loan-portfolio-summary'),
    path('reports-analytics/delinquency-report/<str:pk>', views.delinquency_report, name='delinquency-report'),
    path('reports-analytics/repayment-schedule-report/<str:pk>', views.repayment_schedule_report, name='repayment-schedule-report'),
    path('reports-analytics/loan-application-report/<str:pk>', views.loan_application_report, name='loan-application-report'),
    path('reports-analytics/loan-performance-report/<str:pk>', views.loan_performance_report, name='loan-performance-report'),
    path('reports-analytics/risk-assessment-report/<str:pk>', views.risk_assessment_report, name='risk-assessment-report'),
    path('reports-analytics/interest-income-report/<str:pk>', views.interest_income_report, name='interest-income-report'),
    path('reports-analytics/trends-forecasting/<str:pk>', views.trends_forecasting, name='trends-forecasting'),

]  