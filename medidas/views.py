from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, UpdateView, TemplateView
from django.db.models.functions import Concat
from django.core.serializers import serialize
from .forms import PatientForm, PrescriptionForm
from .models import Patient, Prescription
from termcolor import colored
from django.contrib import messages
from .custom_functions import django_admin_keyword_search

# Create your views here.

@login_required
def index(request):
    return render(request, 'medidas/index.html')

# def patient_detail(request, pk):
#     if request.method == 'GET':
#         patient = get_object_or_404(Patient, pk=pk)
#         data = {
#             'first_name':patient.first_name,
#             'last_name':patient.last_name,
#             'dni':patient.dni,
#             'gender':patient.gender,
#             'phone':patient.phone,
#             'job':patient.job,
#         }
#         return JsonResponse(data, safe=False)

@login_required
def add_prescription(request):
    context = {}
    if request.method == 'POST':
        patient_form = PatientForm(request.POST)
        if patient_form.is_valid():
            new_patient = patient_form.save(commit=False)
            new_patient.optic = request.user
            new_patient.save()
            updated_request = request.POST.copy()
            updated_request.update({'patient': new_patient})
            prescription_form = PrescriptionForm(updated_request)
            # print(colored(patient_form.cleaned_data,'yellow'))
            if prescription_form.is_valid():
                new_prescription = prescription_form.save(commit=False)
                new_prescription.optic = request.user
                new_prescription.save()
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
    context['patient_form'] = patient_form
    context['prescription_form'] = prescription_form
    return render(request, 'medidas/prescription.html', context)

@login_required
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

@login_required
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

@login_required
def prescription_delete(request):
    if request.method == 'POST':
        pk = request.POST['prescription_id']
        prescription = Prescription.objects.get(id=pk)
        prescription.delete()
        return redirect('medidas:prescriptions')

@login_required
def patient_add_prescription(request, pk):
    if request.method=='GET':
        patient = Patient.objects.get(pk=pk)
        patient_form = PatientForm(instance=patient)
        prescription_form = PrescriptionForm()
        return render(request, 'medidas/prescription.html', context={
            'patient_form': patient_form,
            'prescription_form': prescription_form,
            'update': True,
        })
    if request.method=='POST':
        patient = Patient.objects.get(pk=pk)
        updated_request = request.POST.copy()
        updated_request.update({'patient':patient})
        prescription_form = PrescriptionForm(updated_request)
        if prescription_form.is_valid():
            prescription_form.save()
            return redirect('medidas:prescriptions')
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

class PrescriptionListView(LoginRequiredMixin,ListView):
    model = Prescription
    context_object_name = 'prescriptions'
    template_name = 'medidas/prescription_list.html'
    paginate_by = 20
    def get_queryset(self):
        q = self.request.GET.get('q','')
        opticUser = self.request.user.id
        return django_admin_keyword_search(Prescription, q, ['patient__full_name','patient__dni']).filter(optic_id=opticUser).order_by('-date')
    
class PatientListView(LoginRequiredMixin,ListView):
    model = Patient
    context_object_name = 'patients'
    paginate_by = 20
    def get_queryset(self):
        q = self.request.GET.get('q','')
        opticUser = self.request.user.id
        return django_admin_keyword_search(Patient, q, ['full_name','dni']).filter(optic_id=opticUser).order_by('-id')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["patient_form"] = PatientForm()
        return context
    

# class PrescriptionUpdateView(UpdateView):
#     model = Prescription
#     fields = '__all__'
#     template_name = "medidas/prescription_update.html"

class TestView(TemplateView):
    template_name = "medidas/test.html"
    



