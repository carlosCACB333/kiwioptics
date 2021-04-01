from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, UserChangeForm, UserChangeForm
from django.contrib.auth.models import User, Group, Permission
from .models import OpticUser, Account, EmployeeUser
from django.contrib.auth.models import User

from validate_email import validate_email


class OpticaRegisterForm(UserCreationForm):
    username = forms.EmailField(label='Correo electronico', required=True)
    full_name = forms.CharField(
        label='Nombres y apellidos', max_length=100, required=True)
    optic_name = forms.CharField(
        label='Nombre de tu optica', max_length=50, required=True)

    class Meta:
        model = Account
        fields = ('full_name', 'username', 'optic_name',
                  'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(OpticaRegisterForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['placeholder'] = field.label
            field.widget.attrs['class'] = "form-control"


class EmployeeUserForm(forms.ModelForm):
    class Meta:
        model = EmployeeUser
        fields = '__all__'

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
        exclude = ("account",)

    def __init__(self, *args, **kwargs):
        super(OpticUserForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['placeholder'] = field.label
            field.widget.attrs['class'] = "form-control border-md"


class AccountChangeForm(UserChangeForm):
    class Meta:
        model = Account
        fields = ('username', 'full_name')

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
        exclude = ('last_login', 'date_joined', 'user_type', 'is_superuser')
        widgets = {
            'password':forms.PasswordInput(
                attrs={
                    'value':''
                },
            ),

            'user_permissions':forms.CheckboxSelectMultiple(),
            'groups':forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super(UserOfOpticForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['placeholder'] = field.label
            field.widget.attrs['class'] = "form-control"

    def clean_username(self):
        email_v = validate_email(self.cleaned_data['username'])
        if email_v==True:
            raise forms.ValidationError('Este campo no puede ser un email')
        return self.cleaned_data['username']
