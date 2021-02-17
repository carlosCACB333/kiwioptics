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
    context = {}
    if request.method == 'POST':
        #Actualizar
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
                prescription_form = PrescriptionForm(request.POST)
                prescription_form.is_valid()
                print(colored(patient_form.errors,'red'))
                print(colored(prescription_form.errors,'red'))
        #Añadir
        else:
            patient_form = PatientForm(request.POST)
            if patient_form.is_valid():
                new_patient = patient_form.save(commit=True)
                updated_request = request.POST.copy()
                updated_request.update({'patient': new_patient})
                prescription_form = PrescriptionForm(updated_request)
                # print(colored(patient_form.cleaned_data,'yellow'))
                if prescription_form.is_valid():
                    prescription_form.save()
                    print(colored(prescription_form.cleaned_data,'blue'))
                    messages.success(request, f'Historia añadida exitosamente')
                    return redirect('medidas:prescription-list')
                else:
                    print(colored(prescription_form.errors,'red'))
                    new_patient.delete()
            else:
                prescription_form = PrescriptionForm(request.POST)
                prescription_form.is_valid()
                print(colored(patient_form.errors,'red'))
                print(colored(prescription_form.errors,'red'))
    else:
        #Ver
        if 'id' in request.GET:
            id = request.GET['id']
            prescription = Prescription.objects.get(id=id)
            patient = prescription.patient
            patient_form = PatientForm(instance=patient)
            prescription_form = PrescriptionForm(instance=prescription)
            context['editable'] = True
        else:
            patient_form = PatientForm()
            prescription_form = PrescriptionForm()
            context['editable'] = False
    context['patient_form'] = patient_form
    context['prescription_form'] = prescription_form
    return render(request, 'medidas/prescription.html', context)

def prescription_list(request):
    prescriptions = Prescription.objects.order_by(
        '-date'
    )
    context = {
        'prescriptions': prescriptions,
    }
    return render(request, 'medidas/prescription_list.html', context)