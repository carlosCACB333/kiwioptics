from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect


class OpticPermitMixin(LoginRequiredMixin):
    login_url = reverse_lazy('users:login')
    permit_type = None

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
            
        if not (request.user.user_type == self.permit_type):
            return HttpResponseRedirect(self.login_url)

        return super(OpticPermitMixin, self).dispatch(request, *args, **kwargs)
