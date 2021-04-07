from termcolor import colored
from django.http import HttpResponseForbidden
from django.core.exceptions import PermissionDenied, RequestAborted

def model_owned_required(model):
    def decorator(func):
        def wrapper(request, pk):
            prescription = model.objects.get(pk=pk)
            if request.user.get_opticuser() != prescription.optic:
                raise PermissionDenied()
            return func(request, pk)
        return wrapper
    return decorator