from company.models import Organization
from user.models import CompanyStaff

#-- custome context processor for login organization --
def get_organization(request):
    if request.user.is_authenticated and request.user.is_active:
        user = request.user
        try:
            organization = Organization.objects.get(admin=user)
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