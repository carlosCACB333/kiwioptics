from termcolor import colored
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied, RequestAborted
from django.shortcuts import get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth.models import Permission


def logout_required(func):
    """
    decorador, solo pueden acceder los usuarios no auntenticados
    """
    def wrapper(request):
        if request.user.is_authenticated:
            return redirect('medidas:index')
        return func(request)
    return wrapper


def model_owned_required(model):
    """
    Las opticas solo pueden acceder a sus modelos
    """
    def decorator(func):
        def wrapper(request, pk):
            model_instance = get_object_or_404(model, pk=pk)
            if request.user.get_opticuser() != model_instance.optic:
                raise PermissionDenied()
            return func(request, pk)
        return wrapper
    return decorator


def roles_required(allowed_roles=[]):
    """
    Solo pueden acceder los usuarios con los permisos requeridos
    """
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


def any_permission_required(perms, login_url=None, raise_exception=False):
    """
    A decorator which checks user has any of the given permissions.
    permission required can not be used in its place as that takes only a
    single permission.
    """
    def check_perms(user):
        # First check if the user has the permission (even anon users)
        for perm in perms:
            perm = (perm,)
            if user.has_perms(perm):
                return True
        # In case the 403 handler should be called raise the exception
        if raise_exception:
            raise PermissionDenied
        # As the last resort, show the login form
        return False
    return user_passes_test(check_perms, login_url=login_url)
