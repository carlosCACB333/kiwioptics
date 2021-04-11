from rest_framework.authtoken.models import Token
from firebase_admin import auth

from django.shortcuts import render
from django.shortcuts import redirect
from termcolor import colored
from django.contrib.auth.views import PasswordChangeView
from django.views.generic import (
    UpdateView, CreateView, ListView, View
)
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth import login
from django.contrib.auth.models import Permission, Group
from django.core.paginator import Paginator
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.http import Http404
from termcolor import colored

from .forms import *
from .models import Account, OpticUser, EmployeeUser
from .mixins import OpticPermitMixin, OpticPermissionRequiredMixin
from .serializer import LoginSocialSerializer

# Create your views here.


def signup(request):
    if request.method == 'POST':
        optica_form = OpticaRegisterForm(request.POST)
        print(colored(request.POST,'yellow'))
        if optica_form.is_valid():
            new_account = optica_form.save(commit=False)
            new_account.user_type = Account.Types.Optic
            new_account.save()
            OpticUser.objects.create(
                account=new_account, optic_name=request.POST.get('optic_name'), phone=request.POST.get('phone'))
            return redirect('users:login')
        else:
            return render(request, 'users/signup.html', {
                'form': optica_form,
            })
    else:
        return render(request, 'users/signup.html', {
            'form': OpticaRegisterForm(),
        })


class ValidateEmail(View):
    def get(self, request, *args, **kwargs):
        id_cuenta = kwargs['id']
        codigo = kwargs['codigo']

        try:
            cuenta = Account.objects.get(
                id=id_cuenta, verification_code=codigo)
            cuenta.verify_email = True
            cuenta.save()
            messages.success(
                request, f'Tu email a sido verificado con éxito')
        except Account.DoesNotExist:
            messages.error(request, f'Error al verificar el email')
        return HttpResponseRedirect(reverse_lazy("users:login"))


class RegisterGoogleUserCreateView(CreateView):
    """ vista para registrar un usuario mediante autenticacion por google"""
    model = OpticUser
    template_name = "users/signup_google.html"
    form_class = OpticUserForm

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        token = request.POST['token_id']
        serializer = LoginSocialSerializer(data=request.POST)
        # si no es correcto mandamos un error
        serializer.is_valid(raise_exception=True)

        # recupermos el token
        id_token = serializer.data.get('token_id')

        # descincriptamos
        decode_token = auth.verify_id_token(id_token)

        form1 = self.form_class(request.POST)
        if(form1.is_valid()):
            cuenta = Account(
                username=decode_token['email'],
                full_name=decode_token['name'],
                # is_superuser=True,
                user_type=Account.Types.Optic
            )
            if len(decode_token['picture']) <= Account._meta.get_field('picture').max_length and 'picture' in decode_token:
                cuenta.picture = decode_token['picture']
            cuenta.save()
            optica = form1.save(commit=False)
            optica.account = cuenta
            optica.save()

            login(self.request, cuenta)
            Token.objects.create(user=cuenta)

            messages.success(
                request, f'Tu optica ha sido creado con exito!')
            return HttpResponseRedirect(reverse_lazy("medidas:index"))

        else:
            return self.render_to_response(self.get_context_data(form=form1, token_id=token))


class ProfileView(PasswordChangeView):
    "vista que renderiza el perfil de usuario y actualiza su password"

    template_name = "users/profile.html"
    success_url = '.'

    def get_context_data(self, **kwargs):
        password = self.request.user.password
        contexto = super().get_context_data(**kwargs)
        if len(password) == 0:
            if 'form_create_password' not in contexto:
                contexto['form_create_password'] = AccountCreatePasswordForm
        else:
            contexto['form_change_password'] = contexto["form"]
        del contexto["form"]
        return contexto

    def post(self, request, *args, **kwargs):

        if 'old_password' in request.POST:
            form1 = self.get_form()
            if form1.is_valid():
                form1.save()
                messages.success(
                    self.request, f'se actualizó exitosamente la contraseña')
                return self.form_valid(form1)

            else:
                return self.render_to_response(self.get_context_data(form_change_password=form1))
        else:
            form2 = AccountCreatePasswordForm(
                request.POST, instance=self.request.user)
            form2.user = self.request.user
            if form2.is_valid():
                form2.save()
                messages.success(
                    self.request, f'se creó exitosamente la contraseña')
                return self.form_valid(form2)
            else:
                return self.render_to_response(self.get_context_data(form_create_password=form2))


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
    form_class = OpticUserUpdateForm
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


class UserOfOpticCreateView(OpticPermissionRequiredMixin, CreateView):
    """ vista para crear y actualizar los datos de los empleados """

    permission_required = ('users.view_employeeuser',)
    # url_redirect = None
    model = Account
    template_name = "optic/user_of_optic.html"
    form_class = UserOfOpticForm
    form_class_secondary = EmployeeUserForm2

    def get(self, request, *args, **kwargs):
        self.object = None
        context = self.get_context_data()
        if 'id' in request.GET:
            context['form'] = self.form_class(
                instance=Account.objects.get(employeeuser__id=request.GET['id']))
            context['form_employee'] = self.form_class_secondary(
                instance=EmployeeUser.objects.get(id=request.GET['id']))
            context['id'] = request.GET['id']
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'form_employee' not in context:
            context['form_employee'] = self.form_class_secondary
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        if 'id' in request.POST:
            id = request.POST['id']
        else:
            id = None

        if id:
            # actualizamos
            instancia_cuenta = Account.objects.get(employeeuser__id=id)
            instancia_empleado = EmployeeUser.objects.get(id=id)
            form_user = self.form_class(
                request.POST, instance=instancia_cuenta,)
            form_employees = self.form_class_secondary(
                request.POST, instance=instancia_empleado,)
            if form_user.is_valid() and form_employees.is_valid():
                cuenta = form_user.save(commit=False)
                cuenta.set_password(request.POST['password'])
                if 'picture' in request.FILES:
                    cuenta.picture = request.FILES['picture']
                cuenta.save()
                # asignamos permisos
                cuenta.user_permissions.set(
                    form_user.cleaned_data['user_permissions'])
                cuenta.groups.set(form_user.cleaned_data['groups'])

                empleado = form_employees.save(commit=False)
                empleado.optic = request.user.get_opticuser()
                empleado.save()
                messages.success(
                    request, f'Los datos han sido actualizados correctamente')
                return HttpResponseRedirect(reverse_lazy("medidas:index"))
            else:
                return self.render_to_response(self.get_context_data(form=form_user, form_employee=form_employees, id=id))

        else:
            # creamos
            form_user = self.form_class(request.POST)
            form_employees = self.form_class_secondary(request.POST)
            if form_user.is_valid() and form_employees.is_valid():
                cuenta = form_user.save(commit=False)
                cuenta.set_password(request.POST['password'])
                cuenta.user_type = Account.Types.Employee

                if 'picture' in request.FILES:
                    cuenta.picture = request.FILES['picture']
                cuenta.save()

                # asignamos los permisos respectivos
                cuenta.user_permissions.set(
                    form_user.cleaned_data['user_permissions'])
                cuenta.groups.set(form_user.cleaned_data['groups'])

                empleado = form_employees.save(commit=False)
                empleado.account = cuenta
                empleado.optic = request.user.get_opticuser()
                empleado.save()
                messages.success(
                    request, f'Tu empleado a sido registrado con éxito')
                return HttpResponseRedirect(reverse_lazy("medidas:index"))
            else:
                return self.render_to_response(self.get_context_data(form=form_user, form_employee=form_employees))


class UserOfOpticDeleteView(OpticPermissionRequiredMixin, View):
    """ vista para eliminar un empleado """
    permission_required = ('users.delete_account', 'users.delete_employeeuser')

    def get(self, request, *args, **kwargs):
        EmployeeUser.objects.filter(id=self.kwargs['id']).delete()
        messages.success(request, f'Tu empleado a sido borrado con éxito')
        return HttpResponseRedirect(reverse_lazy('users:userOfOptic'))
