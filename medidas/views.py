from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.shortcuts import redirect
from .forms import PatientForm, PrescriptionForm
from .models import Patient, Prescription
from termcolor import colored
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request, 'medidas/index.html')

def prescription(request):
    if request.method == 'POST':
        if "id" in request.GET:
            id = request.GET['id']
            prescription = Prescription.objects.get(id=id)
            patient = prescription.patient
            patient_form = PatientForm(request.POST, instance=patient)
            if patient_form.is_valid():
                updated_patient = patient_form.save(commit=True)
                updated_request = request.POST.copy()
                updated_request.update({'patient': updated_patient})
                prescription_form = PrescriptionForm(updated_request, instance=prescription)
                print(colored(patient_form.cleaned_data,'yellow'))
                if prescription_form.is_valid():
                    prescription_form.save()
                    print(colored(prescription_form.cleaned_data,'blue'))
                    messages.success(request, f'Historia actualizada exitosamente')
                    return redirect('medidas:prescription-list')
        else:
            patient_form = PatientForm(request.POST)
            if patient_form.is_valid():
                new_patient = patient_form.save(commit=True)
                updated_request = request.POST.copy()
                updated_request.update({'patient': new_patient})
                prescription_form = PrescriptionForm(updated_request)
                print(colored(patient_form.cleaned_data,'yellow'))
                if prescription_form.is_valid():
                    prescription_form.save()
                    print(colored(prescription_form.cleaned_data,'blue'))
                    messages.success(request, f'Historia añadida exitosamente')
                    return redirect('medidas:prescription-list')
                else:
                    new_patient.delete()
    if 'id' in request.GET:
        id = request.GET['id']
        prescription = Prescription.objects.get(id=id)
        patient = prescription.patient
        patient_form = PatientForm(instance=patient)
        prescription_form = PrescriptionForm(instance=prescription)
        context = {
            'patient_form': patient_form,
            'prescription_form': prescription_form,
        }
    else:
        patient_form = PatientForm()
        prescription_form = PrescriptionForm()
        context = {
            'patient_form': patient_form,
            'prescription_form': prescription_form,
        }
    return render(request, 'medidas/prescription.html', context)

def prescription_list(request):
    prescriptions = Prescription.objects.order_by(
        '-id'
    )
    context = {
        'prescriptions': prescriptions,
    }
    return render(request, 'medidas/prescription_list.html', context)