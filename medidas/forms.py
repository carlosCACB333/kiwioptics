from django.forms import ModelForm
from .models import Patient, Prescription
from termcolor import colored

class PatientForm(ModelForm):
    class Meta:
        model = Patient
        fields = '__all__'
    
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
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(PrescriptionForm, self).__init__(*args, **kwargs)

        # self.fields['integerPolje1'].widget.attrs['class'] = 'SOMECLASS'

        # you can iterate all fields here
        for fname, f in self.fields.items():
            f.widget.attrs['class'] = 'form-control form-control-sm'
