from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib import messages
from django.core.exceptions import PermissionDenied

class OpticPermitMixin(LoginRequiredMixin):
    login_url = reverse_lazy('users:login')
    permit_type = None

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
            
        if not (request.user.user_type == self.permit_type):
            return HttpResponseRedirect(self.login_url)

        return super(OpticPermitMixin, self).dispatch(request, *args, **kwargs)

class OpticPermissionRequiredMixin(object):
    permission_required=None
    url_redirect=None

    def get_perms(self):
        if(isinstance(self.permission_required,str)):
            return (self.permission_required)
        else:
            return self.permission_required

    def get_url_redirec(self):
        if self.url_redirect is None:
            return reverse_lazy('users:login')
        else:
            return self.url_redirect

    
    def dispatch(self, request, *args, **kwargs):
        if request.user.has_perms(self.get_perms()):
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

