from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import ListView, UpdateView, TemplateView
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
                return redirect('medidas:prescriptions')
            else:
                print(colored(prescription_form.errors,'red'))
                new_patient.delete()
        else:
            prescription_form = PrescriptionForm(request.POST)
            prescription_form.is_valid()
            print(colored(patient_form.errors,'red'))
            print(colored(prescription_form.errors,'red'))
    else:
        patient_form = PatientForm()
        prescription_form = PrescriptionForm()
        context['editable'] = False
    context['patient_form'] = patient_form
    context['prescription_form'] = prescription_form
    return render(request, 'medidas/prescription.html', context)

def prescription_detail(request, pk):
    context = {}
    if request.method=='GET':
        prescription = Prescription.objects.get(pk=pk)
        patient = prescription.patient
        patient_form = PatientForm(instance=patient)
        prescription_form = PrescriptionForm(instance=prescription)
        return render(request, 'medidas/prescription.html', context={
            'patient_form': patient_form,
            'prescription_form': prescription_form,
            'detail': True,
        })

def prescription_update(request, pk):
    context = {}
    if request.method=='GET':
        prescription = Prescription.objects.get(pk=pk)
        patient = prescription.patient
        patient_form = PatientForm(instance=patient)
        prescription_form = PrescriptionForm(instance=prescription)
        return render(request, 'medidas/prescription.html', context={
            'patient_form': patient_form,
            'prescription_form': prescription_form,
            'update': True,
        })
    if request.method=='POST':
        prescription = Prescription.objects.get(pk=pk)
        patient = prescription.patient
        updated_request = request.POST.copy()
        updated_request.update({'patient': patient})
        prescription_form = PrescriptionForm(updated_request,instance=prescription)
        if prescription_form.is_valid():
            prescription_form.save()
            messages.success(request, 'Prescripcion actualizada exitosamente!')
            return redirect('medidas:prescription-detail', pk=pk)
        else:
            print(colored(prescription_form.errors,'red'))

# def prescription_list(request):
#     prescriptions = Prescription.objects.order_by(
#         '-date'
#     )
#     context = {
#         'prescriptions': prescriptions,
#     }
#     return render(request, 'medidas/prescription_list.html', context)

class PrescriptionListView(ListView):
    model = Prescription
    queryset = Prescription.objects.order_by('-date')
    context_object_name = 'prescriptions'
    template_name = 'medidas/prescription_list.html'

class PatientListView(ListView):
    model = Patient
    context_object_name = 'patients'
    template_name = "medidas/patients.html"

# class PrescriptionUpdateView(UpdateView):
#     model = Prescription
#     fields = '__all__'
#     template_name = "medidas/prescription_update.html"


