from termcolor import colored
from django.http import HttpResponseForbidden
from django.core.exceptions import PermissionDenied, RequestAborted
from django.shortcuts import get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth.models import Permission

def logout_required(func):
    def wrapper(request):
        if request.user.is_authenticated:
            return redirect('medidas:index')
        return func(request)
    return wrapper

def model_owned_required(model):
    def decorator(func):
        def wrapper(request, pk):
            model_instance = get_object_or_404(model, pk=pk)
            if request.user.get_opticuser() != model_instance.optic:
                raise PermissionDenied()
            return func(request, pk)
        return wrapper
    return decorator

def roles_required(allowed_roles=[]):
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            if request.user.user_type == 'OPTIC':
                return func(request, *args, **kwargs)
            else:
                if request.user.groups.exists():
                    for role in allowed_roles:
                        if request.user.groups.filter(name=role).exists():
                            return func(request, *args, **kwargs)
            raise PermissionDenied()
        return wrapper
    return decorator

# def permissions_required(allowed_permissions=[]):
#     def decorator(func):
#         def wrapper(request, *args, **kwargs):
#             if request.user.user_type == 'OPTIC':
#                 return func(request, *args, **kwargs)
#             else:
#                 user = request.user
#                 user_permissions = Permission.objects.filter(Q(user=user) | Q(group__user=user)).distinct().values_list('codename', flat=True)
#                 . 
#         return wrapper
#     return decorator