from functools import wraps
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse
from user.models import CompanyStaff

def has_permission(user):
    # Check if the user has the required permission based on their role
    if user.is_authenticated and user.is_active:
        try:
            companystaff = CompanyStaff.objects.get(username=user.username)
            role = companystaff.staff_role  # Assuming 'staff_role' is the related field name for Role in CompanyStaff model
            permissions = role.permissions.all()
            for permission in permissions:
                if user.has_perm(permission.codename):
                    return True
        except CompanyStaff.DoesNotExist:
            pass
    return False

def role_required(view_func):
    """
    Custom decorator to check if the user has the required role permission.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if has_permission(request.user):
            # User has the permission, allow access to the view
            return view_func(request, *args, **kwargs)
        else:
            # User does not have the permission, restrict access and show appropriate message via HttpResponse
            return HttpResponse("Access Denied")
    return _wrapped_view
