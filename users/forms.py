from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import OpticUser

class OpticaRegisterForm(UserCreationForm):
    email = forms.EmailField(label='Correo electronico', required=True)
    full_name = forms.CharField(label='Nombres y apellidos', max_length=100, required=True)
    optic = forms.CharField(label='Nombre de tu optica', max_length=50, required=True)
    class Meta:
        model = OpticUser
        fields =  ('full_name','email','optic','password1','password2')

    def __init__(self, *args, **kwargs):
        super(OpticaRegisterForm, self).__init__(*args,**kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['placeholder'] = field.label

    
  

    
