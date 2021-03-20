from rest_framework.authtoken.models import Token
from firebase_admin import auth

from django.shortcuts import render
from django.shortcuts import redirect
from termcolor import colored
from django.contrib.auth.views import PasswordChangeView
from django.views.generic import (
    UpdateView, CreateView
)
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth import login

from .forms import OpticaRegisterForm, EmployeeUserForm, OpticUserForm, AccountChangeForm
from .models import Account, OpticUser, EmployeeUser
from .mixins import OpticPermitMixin
from .serializer import LoginSocialSerializer

# Create your views here.


def signup(request):
    if request.method == 'POST':
        optica_form = OpticaRegisterForm(request.POST)
        print(colored(request.POST, 'red'))
        if optica_form.is_valid():
            print(colored(optica_form.cleaned_data, 'green'))
            new_account = optica_form.save(commit=False)
            new_account.user_type = Account.Types.Optic
            new_account.save()
            OpticUser.objects.create(
                account=new_account, optic_name=request.POST.get('optic_name'))
            return redirect('users:login')
        else:
            print(optica_form.errors)
            return render(request, 'users/signup.html', {
                'form': optica_form,
            })
    else:
        return render(request, 'users/signup.html', {
            'form': OpticaRegisterForm(),
        })


class RegisterGoogleUserCreateView(CreateView):
    model = Account
    model_secondary = OpticUser
    template_name = "users/signup_google.html"
    form_class = AccountChangeForm
    form_class_secondary = OpticUserForm

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        if 'form_optic' not in contexto:
            contexto['form_optic'] = self.form_class_secondary
        return contexto

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        serializer = LoginSocialSerializer(data=request.POST)
        # si no es correcto mandamos un error
        serializer.is_valid(raise_exception=True)

        # recupermos el token
        id_token = serializer.data.get('token_id')

        # descincriptamos
        decode_token = auth.verify_id_token(id_token)
        # request.POST['username'] = decode_token['email']
        # request.POST['full_name'] = decode_token['name']
        
        form1 = self.form_class(request.POST)
        form2 = self.form_class_secondary(request.POST)
        if(form1.is_valid() and form2.is_valid()):
            cuenta=form1.save(commit=False)
            cuenta.user_type=Account.Types.Optic
            cuenta.picture=decode_token['picture']
            cuenta.save()
            optica=form2.save(commit=False)
            optica.account=cuenta
            optica.save()

            login(self.request,cuenta)
            Token.objects.create(user=cuenta)

            messages.success(
                request, f'Tu optica a sido creado con exito')
            return HttpResponseRedirect(reverse_lazy("medidas:index"))


        else:
            return self.render_to_response(self.get_context_data(form=form1, form_optic=form2))


class ProfileView(PasswordChangeView):
    "vista que renderiza el perfil de usuario y actualiza su password"

    template_name = "users/profile.html"
    success_url = '.'

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto['form_change_password'] = contexto["form"]
        del contexto["form"]
        return contexto

    def form_valid(self, form):
        form.save()
        messages.success(
            self.request, f'se actualizó exitosamente la contraseña')
        return super().form_valid(form)


class EmployeeUserUpdateView(OpticPermitMixin, UpdateView):
    """ vista que actualiza los datos de los empleados """
    model = EmployeeUser
    template_name = "employee/employee_update.html"
    form_class = EmployeeUserForm
    success_url = reverse_lazy('users:profile')
    permit_type = Account.Types.Employee

    def form_valid(self, form):
        messages.success(
            self.request, f'Tus datos han sido actuliazados correctamente')
        self.object = form.save()
        return super().form_valid(form)


class OpticUserUpdateView(OpticPermitMixin, UpdateView):
    """ vista para actualizar la optica y su cuenta """
    model = OpticUser
    model_secondary = Account
    template_name = "optic/optic_user_update.html"
    form_class = OpticUserForm
    form_class_secondary = AccountChangeForm
    success_url = reverse_lazy('users:profile')
    permit_type = Account.Types.Optic

    def form_valid(self, form):
        messages.success(
            self.request, f'Tus datos han sido actuliazados correctamente')
        self.object = form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        pk = self.kwargs.get("pk", 0)
        contexto = super(OpticUserUpdateView, self).get_context_data(**kwargs)
        cuenta = self.request.user
        if 'form' not in contexto:
            contexto['form'] = self.form_class
        if 'form_change_account' not in contexto:
            contexto['form_change_account'] = self.form_class_secondary(
                instance=cuenta)

        contexto["id"] = pk
        return contexto

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        id_optic = kwargs["pk"]

        optica = self.model.objects.get(id=id_optic)
        cuenta = request.user

        form1 = self.form_class(request.POST, instance=optica)
        form2 = self.form_class_secondary(request.POST, instance=cuenta)

        if(form1.is_valid() and form2.is_valid()):
            form1.save()
            form2.save()
            messages.success(
                request, f'Tus datos han sido actuliazados correctamente')
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form1, form_change_account=form2))
