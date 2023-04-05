from company.models import Organization

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