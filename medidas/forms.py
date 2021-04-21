from django.forms import ModelForm, ModelChoiceField, ModelMultipleChoiceField, DecimalField, ChoiceField
from django.contrib.auth.forms import PasswordResetForm
from django.core.exceptions import ValidationError
from .models import Patient, Prescription, Crystal, CrystalTreatments, CrystalMaterial, Subsidiary
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
        if cleaned_data['dni'] and Patient.objects.filter(dni=cleaned_data['dni'], optic=self.request.user.get_opticuser()).exists():
            msg = 'Ya existe un paciente con este dni.'
            self.add_error('dni', ValidationError(msg))
        return cleaned_data


class PrescriptionForm(ModelForm):

    dip_choices = Prescription.dnp_choices[:]
    for i in range(len(dip_choices)):
        dip_choices[i] = list(dip_choices[i])
        dip_choices[i][0] *= 2
        if dip_choices[i][1].endswith('mm'):
             dip_choices[i][1]=str(int(float(dip_choices[i][1][:-2])*2))+'mm'
        dip_choices[i] = tuple(dip_choices[i])
        
    far_dip = ChoiceField(choices=dip_choices, required=False)
    intermediate_dip = ChoiceField(choices=dip_choices, required=False)
    near_dip = ChoiceField(choices=dip_choices, required=False)

    class Meta:
        model = Prescription
        exclude = ('optic', 'prescription_optic_id',
                   'doctor', 'prescription_type','time')

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(PrescriptionForm, self).__init__(*args, **kwargs)
        self.fields['crystals'].queryset = Crystal.objects.filter(
            optic=self.request.user.get_opticuser())
        for fname, f in self.fields.items():
            f.widget.attrs['class'] = 'form-control form-control-sm'
            f.widget.attrs['form'] = 'prescription_form'

    def save(self, commit=True):
        p = super(PrescriptionForm, self).save(commit=False)
        print(colored(type(self.cleaned_data['far_dip']),'green'))
        if p.is_dip:
            if self.cleaned_data['far_dip']:
                far_dip = float(self.cleaned_data['far_dip'])
                p.far_dnp_right = far_dip / 2
                p.far_dnp_left = far_dip / 2
            if self.cleaned_data['intermediate_dip']:
                intermediate_dip = float(self.cleaned_data['intermediate_dip'])
                p.intermediate_dnp_right = intermediate_dip / 2
                p.intermediate_dnp_left = intermediate_dip / 2
            if self.cleaned_data['near_dip']:
                near_dip = float(self.cleaned_data['near_dip'])
                p.near_dnp_right = near_dip / 2
                p.near_dnp_left = near_dip / 2
        if commit:
            p.save()
        return p

    def clean_is_dip(self):
        data = self.request.user.configuration.is_dip
        return data
    
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

class SubsidiaryForm(ModelForm):
    
    class Meta:
        model = Subsidiary
        exclude = ('optic',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fname, f in self.fields.items():
            f.widget.attrs['class'] = 'form-control form-control-sm'

