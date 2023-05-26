from company.models import Organization
from user.models import CompanyStaff, Notification
from django.contrib.auth.models import User

#-- custome context processor for login organization --
def get_organization(request):
    if request.user.is_authenticated and request.user.is_active:
        try:
            user = CompanyStaff.objects.get(username=request.user.username) 
            organization = user.company 
            return {"organization" :organization}
        except Organization.DoesNotExist:
            pass
    return {}  

def get_user(request):
    if request.user.is_authenticated and request.user.is_active:
        try:
            user = CompanyStaff.objects.get(username=request.user.username)
            return {"user" :user}
        except CompanyStaff.DoesNotExist:
            pass
    return {}

def get_company_currency(request):
    if request.user.is_authenticated and request.user.is_active:
        try:
            user = CompanyStaff.objects.get(username=request.user.username)
            organization = user.company
            company_currency = organization.currency
            return {"company_currency" :company_currency}
        except CompanyStaff.DoesNotExist:
            pass
    return {}

def get_company_phone_code(request):
    if request.user.is_authenticated and request.user.is_active:
        try:
            user = CompanyStaff.objects.get(username=request.user.username)
            organization = user.company
            company_phone_code = organization.phone_code
            return {"company_phone_code" :company_phone_code}
        except CompanyStaff.DoesNotExist:
            pass
    return {}

def get_user_notifications(request):
    if request.user.is_authenticated and request.user.is_active:
        try:
            user = CompanyStaff.objects.get(username=request.user.username)
            notifications = Notification.objects.filter(recipient=user, is_read=False).order_by('-timestamp')[:3]
            return {"notifications" :notifications}
        except CompanyStaff.DoesNotExist:
            pass
    return {}