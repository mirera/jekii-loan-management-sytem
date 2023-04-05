from company.models import Organization

def get_organization(request):
  # you might need this line for unit tests
  if request.user.is_authenticated and request.user.is_active:
    user = request.user
    organization = Organization.objects.get(admin=user)
    return {"organization" :organization}