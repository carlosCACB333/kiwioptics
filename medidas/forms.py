from django.forms import ModelForm
from django import forms
from .models import Patient, Prescription, Crystal, CrystalTreatments
from termcolor import colored


class PatientForm(ModelForm):
    class Meta:
        model = Patient
        exclude = ('optic', 'patient_optic_id')

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
        exclude = ('optic', 'prescription_optic_id')

    def __init__(self, *args, **kwargs):
        super(PrescriptionForm, self).__init__(*args, **kwargs)

        # self.fields['integerPolje1'].widget.attrs['class'] = 'SOMECLASS'

        # you can iterate all fields here
        for fname, f in self.fields.items():
            f.widget.attrs['class'] = 'form-control form-control-sm'
            f.widget.attrs['form'] = 'prescription_form'


class CrystalPruebaForm(ModelForm):
    """Form definition for CrystalPrueba."""
    id_user = None

    def __init__(self, id, *args, **kwargs):
        self.id_user = id
        print(self.id_user)
        super(CrystalPruebaForm, self).__init__(*args, **kwargs)

    class Meta:
        """Meta definition for CrystalPruebaform."""

        model = Crystal
        fields = "__all__"

    treatments = forms.ModelMultipleChoiceField(
        queryset=CrystalTreatments.objects.filter(id=1)
    )
