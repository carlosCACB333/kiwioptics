from django.forms import ModelForm, ModelChoiceField, ModelMultipleChoiceField
from .models import Patient, Prescription, Crystal, CrystalTreatments, CrystalMaterial
from termcolor import colored

class PatientForm(ModelForm):
    class Meta:
        model = Patient
        exclude = ('optic','patient_optic_id')
    
    def __init__(self, *args, **kwargs):
        super(PatientForm, self).__init__(*args, **kwargs)

        # self.fields['integerPolje1'].widget.attrs['class'] = 'SOMECLASS'

        # you can iterate all fields here
        for fname, f in self.fields.items():
            f.widget.attrs['class'] = 'form-control form-control-sm'
            f.widget.attrs['form'] = 'prescription_form'

class PrescriptionForm(ModelForm):
    
    class Meta:
        model = Prescription
        exclude = ('optic','prescription_optic_id','doctor','prescription_type')

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(PrescriptionForm, self).__init__(*args, **kwargs)

        # self.fields['integerPolje1'].widget.attrs['class'] = 'SOMECLASS'
        self.fields['crystals'].queryset = Crystal.objects.filter(optic=self.request.user.get_opticuser())
        # you can iterate all fields here
        for fname, f in self.fields.items():    
            f.widget.attrs['class'] = 'form-control form-control-sm'
            f.widget.attrs['form'] = 'prescription_form'

class CrystalForm(ModelForm):
    
    class Meta:
        model = Crystal
        fields = ['name','material','treatments','default_price']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(CrystalForm, self).__init__(*args, **kwargs)
        self.fields['treatments'].queryset = CrystalTreatments.objects.filter(optic=self.request.user.get_opticuser())
        self.fields['material'].queryset = CrystalMaterial.objects.filter(optic=self.request.user.get_opticuser())
        for fname, f in self.fields.items():    
            f.widget.attrs['class'] = 'form-control form-control-sm'

    