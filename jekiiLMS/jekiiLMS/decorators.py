from functools import wraps
from django.shortcuts import render

def has_permission(user):
    # Check if the user has the required permission
    if user.is_authenticated and user.is_active:
        user_permissions = user.user_permissions.all() #get all user permissions
        for user_permission in user_permissions:
            permission = user_permission.content_type.app_label + '.' + user_permission.codename
            if user.has_perm(permission):
                return True
        return False

def permission_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if has_permission(request.user):
            # User has the permission, allow access to the view
            return view_func(request, *args, **kwargs)
        else:
            # User does not have the permission, restrict access and show appropriate message via HttpResponse
            return render(request, 'error/access_denied.html')        
    return _wrapped_view
