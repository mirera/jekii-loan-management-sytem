from functools import wraps
from django.shortcuts import render

def has_permission(user, required_permission):
    # Check if the user has the required permission
    if user.is_authenticated and user.is_active:
        return user.has_perm(required_permission)
    return False

def permission_required(required_permission):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if has_permission(request.user, required_permission):
                # User has the permission, allow access to the view
                return view_func(request, *args, **kwargs)
            else:
                # User does not have the permission, restrict access and show appropriate message via HttpResponse
                return render(request, 'error/access_denied.html')        
        return _wrapped_view
    return decorator


'''
def has_permission(user):
    # Check if the user has the required permission
    if user.is_authenticated and user.is_active:
        user_permissions = user.user_permissions.all() #get all user permissions
        print(f'user permissions {user_permissions}')
        for user_permission in user_permissions:
            permission = user_permission.content_type.app_label + '.' + user_permission.codename
            print(f'after first for loop  {user.has_perm(permission)}')
            if user.has_perm(permission):
                return True
        return False

def permission_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        print(f'second function {has_permission(request.user)}')
        if has_permission(request.user):
            # User has the permission, allow access to the view
            return view_func(request, *args, **kwargs)
        else:
            # User does not have the permission, restrict access and show appropriate message via HttpResponse
            return render(request, 'error/access_denied.html')        
    return _wrapped_view
'''