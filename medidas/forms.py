
from django.forms import ModelForm, ModelChoiceField, ModelMultipleChoiceField
from django.contrib.auth.forms import PasswordResetForm
from django.core.exceptions import ValidationError
from .models import Patient, Prescription, Crystal, CrystalTreatments, CrystalMaterial
from termcolor import colored

from users.models import Account


class PatientForm(ModelForm):

    class Meta:
        model = Patient
        exclude = ('optic', 'patient_optic_id')

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(PatientForm, self).__init__(*args, **kwargs)
        for fname, f in self.fields.items():
            f.widget.attrs['class'] = 'form-control form-control-sm'
            f.widget.attrs['form'] = 'prescription_form'

    def clean(self):
        cleaned_data = self.cleaned_data
        if Patient.objects.filter(dni=cleaned_data['dni'], optic=self.request.user.get_opticuser()).exists():
            msg = 'Ya existe un paciente con este dni.'
            self.add_error('dni', ValidationError(msg))
        return cleaned_data


class PrescriptionForm(ModelForm):

    class Meta:
        model = Prescription
        exclude = ('optic', 'prescription_optic_id',
                   'doctor', 'prescription_type')

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(PrescriptionForm, self).__init__(*args, **kwargs)

        # self.fields['integerPolje1'].widget.attrs['class'] = 'SOMECLASS'
        self.fields['crystals'].queryset = Crystal.objects.filter(
            optic=self.request.user.get_opticuser())
        # you can iterate all fields here
        for fname, f in self.fields.items():
            f.widget.attrs['class'] = 'form-control form-control-sm'
            f.widget.attrs['form'] = 'prescription_form'


class CrystalForm(ModelForm):

    class Meta:
        model = Crystal
        fields = ['crystal_name', 'material', 'treatments', 'default_price']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(CrystalForm, self).__init__(*args, **kwargs)
        self.fields['treatments'].queryset = CrystalTreatments.objects.filter(
            optic=self.request.user.get_opticuser())
        self.fields['material'].queryset = CrystalMaterial.objects.filter(
            optic=self.request.user.get_opticuser())
        for fname, f in self.fields.items():
            f.widget.attrs['class'] = 'form-control form-control-sm'


class CrystalMaterialForm(ModelForm):

    class Meta:
        model = CrystalMaterial
        exclude = ('optic',)

    def __init__(self, *args, **kwargs):
        super(CrystalMaterialForm, self).__init__(*args, **kwargs)
        self.fields['description'].widget.attrs['rows'] = '3'
        for fname, f in self.fields.items():
            f.widget.attrs['class'] = 'form-control form-control-sm'


class CrystalTreatmentsForm(ModelForm):

    class Meta:
        model = CrystalTreatments
        exclude = ('optic',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['description'].widget.attrs['rows'] = '3'
        for fname, f in self.fields.items():
            f.widget.attrs['class'] = 'form-control form-control-sm'
