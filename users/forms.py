import unicodedata

from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, UserChangeForm, UserChangeForm, AuthenticationForm, PasswordResetForm
from django.contrib.auth.models import User, Group, Permission
from .models import OpticUser, Account, EmployeeUser

from validate_email import validate_email

from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib import messages


class OpticaRegisterForm(UserCreationForm):
    username = forms.EmailField(label='Correo electronico', required=True)
    full_name = forms.CharField(
        label='Nombres y apellidos', max_length=100, required=True)
    optic_name = forms.CharField(
        label='Nombre de tu optica', max_length=50, required=True)
    phone = forms.CharField(label="Celular", max_length=30, required=True)

    class Meta:
        model = Account
        fields = ('full_name', 'username', 'optic_name', 'phone',
                  'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(OpticaRegisterForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['placeholder'] = field.label
            field.widget.attrs['class'] = "form-control"


class EmployeeUserForm(forms.ModelForm):
    class Meta:
        model = EmployeeUser
        exclude = ('account', 'optic')

    def __init__(self, *args, **kwargs):
        super(EmployeeUserForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['placeholder'] = field.label
            field.widget.attrs['class'] = "form-control border-md"


class EmployeeUserForm2(forms.ModelForm):

    class Meta:
        model = EmployeeUser
        exclude = ('account', 'optic')

        widgets = {
            'password': forms.PasswordInput(),
        }

    def __init__(self, *args, **kwargs):
        super(EmployeeUserForm2, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['placeholder'] = field.label
            field.widget.attrs['class'] = "form-control border-md"


class OpticUserForm(forms.ModelForm):
    class Meta:
        model = OpticUser
        exclude = ("account", "prescription_name")

    def __init__(self, *args, **kwargs):
        super(OpticUserForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['placeholder'] = field.label
            field.widget.attrs['class'] = "form-control border-md"


class OpticUserUpdateForm(forms.ModelForm):
    class Meta:
        model = OpticUser
        exclude = ("account",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['placeholder'] = field.label
            field.widget.attrs['class'] = "form-control border-md"


class AccountChangeForm(UserChangeForm):
    class Meta:
        model = Account
        fields = ('full_name',)

    def __init__(self, *args, **kwargs):
        super(AccountChangeForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['placeholder'] = field.label
            field.widget.attrs['class'] = "form-control"


class UserOfOpticForm(forms.ModelForm):
    """formulario para registrar la cuenta de los usuarios de las opticas"""

    class Meta:
        model = Account
        # fields='__all__'
        exclude = ('last_login', 'date_joined',
                   'user_type', 'is_superuser', 'is_staff')
        widgets = {
            'password': forms.PasswordInput(
                attrs={
                    'value': ''
                },
            ),

            'user_permissions': forms.CheckboxSelectMultiple(),
            'groups': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super(UserOfOpticForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['placeholder'] = field.label
            field.widget.attrs['class'] = "form-control"

    def clean_username(self):
        email_v = validate_email(self.cleaned_data['username'])
        if email_v == True:
            raise forms.ValidationError('Este campo no puede ser un email')
        return self.cleaned_data['username']


class AccountCreatePasswordForm(UserCreationForm):
    class Meta:
        model = Account
        fields = ('password1', 'password2')


class AccountAutenticateForm(AuthenticationForm):
    """ autentication user"""

    def clean(self):
        cuenta = Account.objects.filter(
            username=self.cleaned_data.get('username'))
        if cuenta:
            if cuenta.first().verify_email == False and cuenta.first().user_type == Account.Types.Optic:
                raise forms.ValidationError(
                    'Su email no ha sido verificado. Entre a su correo y valide su cuenta')
        return super(AccountAutenticateForm, self).clean()


class PasswordResetForm2(PasswordResetForm):

    def get_users(self, email):
        username_field_name = Account.USERNAME_FIELD
        active_users = Account._default_manager.filter(**{
            '%s__iexact' % username_field_name: email,
            'is_active': True,
        })
        return (
            u for u in active_users
            if u.has_usable_password() and _unicode_ci_compare(email, getattr(u, username_field_name))
        )

    def save(self, domain_override=None, subject_template_name='registration/password_reset_subject.txt', email_template_name='registration/password_reset_email.html', use_https=False, token_generator=default_token_generator, from_email=None, request=None, html_email_template_name=None, extra_email_context=None):
        email = self.cleaned_data["email"]
        if not domain_override:
            current_site = get_current_site(request)
            site_name = current_site.name
            domain = current_site.domain
        else:
            site_name = domain = domain_override
        for user in self.get_users(email):
            user_email = user
            context = {
                'email': user_email,
                'domain': domain,
                'site_name': site_name,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'user': user,
                'token': token_generator.make_token(user),
                'protocol': 'https' if use_https else 'http',
                **(extra_email_context or {}),
            }
            self.send_mail(
                subject_template_name, email_template_name, context, from_email,
                user_email, html_email_template_name=html_email_template_name,
            )
            messages.success(request, f'Hemos enviado un link de recuperacion a tu email. revisa tu bandeja de entrada')
            break
        else:
            messages.error(request, f'No se encontró ningun usuario con el correo ingresado. por favor intente con otro correo')


# functions

def _unicode_ci_compare(s1, s2):
    """
    Perform case-insensitive comparison of two identifiers, using the
    recommended algorithm from Unicode Technical Report 36, section
    2.11.2(B)(2).
    """
    return unicodedata.normalize('NFKC', s1).casefold() == unicodedata.normalize('NFKC', s2).casefold()
