from termcolor import colored
from django.http import HttpResponseForbidden
from django.core.exceptions import PermissionDenied, RequestAborted
from django.shortcuts import get_object_or_404

def model_owned_required(model):
    def decorator(func):
        def wrapper(request, pk):
            model_instance = get_object_or_404(model, pk=pk)
            if request.user.get_opticuser() != model_instance.optic:
                raise PermissionDenied()
            return func(request, pk)
        return wrapper
    return decorator