from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, FileResponse
from django.urls import reverse_lazy
import random
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import ListView, UpdateView, TemplateView, CreateView, TemplateView, DetailView, DeleteView
from django.db.models.functions import Concat
from django.core.serializers import serialize
from django.core.exceptions import PermissionDenied
from .forms import PatientForm, PrescriptionForm, CrystalForm, CrystalMaterialForm, CrystalTreatmentsForm, SubsidiaryForm, LaboratoryForm
from .models import Patient, Prescription, DiagnosisChoices, Crystal, CrystalTreatments, CrystalMaterial, Subsidiary, Laboratory
from users.models import EmployeeUser, Configuration
from users.mixins import OpticPermissionRequiredMixin
from termcolor import colored
from django.contrib import messages
from .custom_functions import django_admin_keyword_search
from .decorators import *
from django.contrib.auth.views import PasswordResetView
from django.conf import settings
from django_weasyprint import WeasyTemplateResponseMixin
from django_weasyprint.views import CONTENT_TYPE_PNG, WeasyTemplateResponse
from django_weasyprint.utils import django_url_fetcher
from django.utils import timezone
from django.utils.decorators import method_decorator
import functools
import ssl


class TestView(TemplateView):
    template_name = "medidas/prescription_pdf.html"


@method_decorator(login_required, 'dispatch')
class IndexView(ListView):
    """
    Vista de administracion
    """
    model = EmployeeUser
    template_name = "medidas/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        optic = self.request.user.get_opticuser()
        context["subsidiary_list"] = Subsidiary.objects.filter(optic=optic)
        return context


@login_required
@permission_required('medidas.add_prescription', raise_exception=True)
def add_prescription(request):
    """
    Vista de añadir prescripcion
    """
    context = {}
    if request.method == 'POST':
        patient_form = PatientForm(request.POST, request=request)
        if patient_form.is_valid():
            new_patient = patient_form.save(commit=False)
            account = request.user
            new_patient.optic = account.get_opticuser()
            new_patient.save()
            updated_request = request.POST.copy()
            updated_request.update({'patient': new_patient})
            prescription_form = PrescriptionForm(
                updated_request, request=request)
            print(colored(patient_form.cleaned_data, 'yellow'))
            if prescription_form.is_valid():
                new_prescription = prescription_form.save(commit=False)
                new_prescription.optic = account.get_opticuser()
                print(colored(prescription_form.cleaned_data, 'blue'))
                new_prescription.save()
                messages.success(request, f'Historia añadida exitosamente')
                return redirect('medidas:prescriptions')
            else:
                print(colored(prescription_form.errors, 'red'))
                new_patient.delete()
        else:
            prescription_form = PrescriptionForm(request.POST, request=request)
            prescription_form.is_valid()
            print(colored(patient_form.errors, 'red'))
            print(colored(prescription_form.errors, 'red'))
    else:
        patient_form = PatientForm(request=request)
        prescription_form = PrescriptionForm(request=request)
    context['patient_form'] = patient_form
    context['prescription_form'] = prescription_form
    context['diagnosis_choices'] = DiagnosisChoices.choices
    context['is_dip'] = request.user.configuration.is_dip
    return render(request, 'medidas/prescription.html', context)


@login_required
@model_owned_required(Prescription)
def prescription_detail(request, pk):
    """
    Vista de visualizar prescripcion
    """
    print(colored(f"{request} + {pk}", 'red'))
    context = {}
    if request.method == 'GET':
        prescription = get_object_or_404(Prescription, pk=pk)
        patient = prescription.patient
        patient_form = PatientForm(instance=patient, request=request)
        initial = {}
        if prescription.is_dip:
            if prescription.far_dnp_left:
                far_dip = prescription.far_dnp_left * 2
                initial['far_dip'] = far_dip
            if prescription.intermediate_dnp_left:
                intermediate_dip = prescription.intermediate_dnp_left * 2
                initial['intermediate_dip'] = intermediate_dip
            if prescription.near_dnp_left:
                near_dip = prescription.near_dnp_left * 2
                initial['near_dip'] = near_dip
        prescription_form = PrescriptionForm(
            instance=prescription, request=request, initial=initial)
        return render(request, 'medidas/prescription.html', context={
            'patient_form': patient_form,
            'prescription_form': prescription_form,
            'detail': True,
            'is_dip': prescription.is_dip,
        })


@login_required
@permission_required('medidas.change_prescription', raise_exception=True)
@model_owned_required(Prescription)
def prescription_update(request, pk):
    """
    Vista de actualizar prescripcion
    """
    context = {}
    if request.method == 'GET':
        prescription = get_object_or_404(Prescription, pk=pk)
        patient = prescription.patient
        patient_form = PatientForm(instance=patient, request=request)
        initial = {}
        if prescription.is_dip:
            if prescription.far_dnp_left:
                far_dip = prescription.far_dnp_left * 2
                initial['far_dip'] = far_dip
            if prescription.intermediate_dnp_left:
                intermediate_dip = prescription.intermediate_dnp_left * 2
                initial['intermediate_dip'] = intermediate_dip
            if prescription.near_dnp_left:
                near_dip = prescription.near_dnp_left * 2
                initial['near_dip'] = near_dip
        prescription_form = PrescriptionForm(
            instance=prescription, request=request, initial=initial)
        return render(request, 'medidas/prescription.html', context={
            'patient_form': patient_form,
            'prescription_form': prescription_form,
            'update': True,
            'is_dip': prescription.is_dip,
        })
    if request.method == 'POST':
        prescription = get_object_or_404(Prescription, pk=pk)
        patient = prescription.patient
        updated_request = request.POST.copy()
        updated_request.update({'patient': patient})
        prescription_form = PrescriptionForm(
            updated_request, instance=prescription, request=request)
        if prescription_form.is_valid():
            prescription_form.save()
            messages.success(request, 'Prescripcion actualizada exitosamente!')
            return redirect('medidas:prescription-detail', pk=pk)
        else:
            prescription = get_object_or_404(Prescription, pk=pk)
            patient = prescription.patient
            patient_form = PatientForm(instance=patient, request=request)
            print(colored(prescription_form.errors, 'red'))
            return render(request, 'medidas/prescription.html', context={
                'patient_form': patient_form,
                'prescription_form': prescription_form,
                'update': True,
                'ís_dip': prescription.is_dip,
            })


@login_required
@permission_required('medidas.delete_prescription', raise_exception=True)
def prescription_delete(request):
    """
    Vista de eliminar prescripcion
    """
    if request.method == 'POST':
        pk = request.POST['prescription_id']
        prescription = get_object_or_404(Prescription, pk=pk)
        if request.user.get_opticuser() != prescription.optic:
            raise PermissionDenied()
        prescription.delete()
        return redirect('medidas:prescriptions')


@login_required
@permission_required('medidas.add_prescription', raise_exception=True)
@model_owned_required(Patient)
def patient_add_prescription(request, pk):
    """
    Vista de añadir prescripcion a un cliente
    """
    if request.method == 'GET':
        patient = get_object_or_404(Patient, pk=pk)
        patient_form = PatientForm(instance=patient, request=request)
        prescription_form = PrescriptionForm(request=request)
        return render(request, 'medidas/prescription.html', context={
            'patient_form': patient_form,
            'prescription_form': prescription_form,
            'update': True,
            'is_dip': request.user.configuration.is_dip,
        })
    if request.method == 'POST':
        patient = get_object_or_404(Patient, pk=pk)
        updated_request = request.POST.copy()
        updated_request.update({'patient': patient})
        prescription_form = PrescriptionForm(updated_request, request=request)
        if prescription_form.is_valid():
            new_prescription = prescription_form.save(commit=False)
            new_prescription.optic = request.user.get_opticuser()
            new_prescription.save()
            return redirect('medidas:prescriptions')
        else:
            print(colored(prescription_form.errors, 'red'))


@method_decorator(login_required, 'dispatch')
class PrescriptionListView(ListView):
    """
    Vista de visualizar lista de prescripciones
    """
    model = Prescription
    context_object_name = 'prescriptions'
    template_name = 'medidas/prescription_list.html'
    paginate_by = 20

    def get_queryset(self):
        q = self.request.GET.get('q', '')
        opticUser = self.request.user.get_opticuser().id
        return django_admin_keyword_search(Prescription, q, ['patient__full_name', 'patient__dni']).filter(optic_id=opticUser).order_by('-prescription_optic_id')


@method_decorator(login_required, 'dispatch')
class PatientListView(ListView):
    """
    Vista de listar pacientes con sus prescripciones
    """
    model = Patient
    context_object_name = 'patients'
    paginate_by = 20

    def get_queryset(self):
        q = self.request.GET.get('q', '')
        opticUser = self.request.user.get_opticuser().id
        return django_admin_keyword_search(Patient, q, ['full_name', 'dni']).filter(optic_id=opticUser).order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["patient_form"] = PatientForm(request=self.request)
        return context

# class PrescriptionUpdateView(UpdateView):
#     model = Prescription
#     fields = '__all__'
#     template_name = "medidas/prescription_update.html"


@method_decorator(login_required, 'dispatch')
class CrystalListView(ListView):
    """
    Vista de listar lunas
    """
    model = Crystal
    context_object_name = 'crystals'
    template_name = "medidas/crystals.html"

    def get_queryset(self):
        opticUser = self.request.user.get_opticuser().id
        return Crystal.objects.filter(optic=opticUser)


@method_decorator(login_required, 'dispatch')
@method_decorator(permission_required('medidas.add_crystal', raise_exception=True), 'dispatch')
class CrystalCreateView(CreateView):
    """
    Vista de crear lunas
    """
    model = Crystal
    template_name = "medidas/crystal_add.html"
    form_class = CrystalForm
    success_url = reverse_lazy('medidas:crystals')

    def form_valid(self, form):
        print(colored(form.cleaned_data, 'green'))
        form.instance.optic = self.request.user.get_opticuser()
        return super().form_valid(form)

    def form_invalid(self, form):
        print(colored(form.cleaned_data, 'red'))
        print(colored(form.errors, 'red'))
        return super().form_invalid(form)

    def get_form_kwargs(self):
        kwargs = super(CrystalCreateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


@method_decorator(login_required, 'dispatch')
@method_decorator(permission_required('medidas.change_crystal', raise_exception=True), 'dispatch')
class CrystalUpdateView(UpdateView):
    """
    Vista de actualizar lunas
    """
    model = Crystal
    success_url = reverse_lazy('medidas:crystals')
    form_class = CrystalForm
    template_name = "medidas/crystal_add.html"

    def form_invalid(self, form):
        print(colored(form.cleaned_data, 'red'))
        print(colored(form.errors, 'red'))
        return super().form_invalid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['update'] = True
        return context


@method_decorator(login_required, 'dispatch')
@method_decorator(permission_required('medidas.delete_crystal', raise_exception=True), 'dispatch')
class CrystalDeleteView(View):
    """
    Vista de eliminar lunas
    """

    def post(self, request, *args, **kwargs):
        pk = request.POST['crystal_id']
        crystal = get_object_or_404(Crystal, pk=pk)
        crystal.delete()
        return redirect('medidas:crystals')


@method_decorator(login_required, 'dispatch')
class CrystalMaterialListView(ListView):
    """
    Vista de listar materiales
    """
    model = CrystalMaterial
    context_object_name = 'crystals_materials'
    template_name = "medidas/crystal_materials.html"

    def get_queryset(self):
        opticUser = self.request.user.get_opticuser().id
        return CrystalMaterial.objects.filter(optic=opticUser)


@method_decorator(login_required, 'dispatch')
@method_decorator(permission_required('medidas.add_crystalmaterial', raise_exception=True), 'dispatch')
class CrystalMaterialCreateView(CreateView):
    """
    Vista de crear material
    """
    model = CrystalMaterial
    form_class = CrystalMaterialForm
    template_name = "medidas/crystal_material_add.html"
    success_url = reverse_lazy('medidas:materials')

    def form_valid(self, form):
        form.instance.optic = self.request.user.get_opticuser()
        return super().form_valid(form)

    def form_invalid(self, form):
        print(colored(form.cleaned_data, 'red'))
        print(colored(form.errors, 'red'))
        return super().form_invalid(form)


@method_decorator(login_required, 'dispatch')
@method_decorator(permission_required('medidas.change_crystalmaterial', raise_exception=True), 'dispatch')
class CrystalMaterialUpdateView(UpdateView):
    """
    Vista de actualizar material
    """
    model = CrystalMaterial
    template_name = "medidas/crystal_material_add.html"
    form_class = CrystalMaterialForm
    success_url = reverse_lazy('medidas:materials')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['update'] = True
        return context


@method_decorator(login_required, 'dispatch')
@method_decorator(permission_required('medidas.delete_crystalmaterial', raise_exception=True), 'dispatch')
class CrystalMaterialDeleteView(View):
    """
    Vista de eliminar material
    """

    def post(self, request, *args, **kwargs):
        pk = request.POST['material_id']
        material = get_object_or_404(CrystalMaterial, pk=pk)
        if material.optic != request.user.get_opticuser():
            raise PermissionDenied()
        material.delete()
        return redirect('medidas:materials')


@method_decorator(login_required, 'dispatch')
class CrystalTreatmentsListView(ListView):
    """
    Vista de listar tratamientos
    """
    model = CrystalTreatments
    context_object_name = 'crystals_treatments'
    template_name = "medidas/crystal_treatments.html"

    def get_queryset(self):
        opticUser = self.request.user.get_opticuser().id
        return CrystalTreatments.objects.filter(optic=opticUser)


@method_decorator(login_required, 'dispatch')
@method_decorator(permission_required('medidas.add_crystaltreatments', raise_exception=True), 'dispatch')
class CrystalTreatmentsCreateView(CreateView):
    """
    Vista de crear tratamiento
    """
    model = CrystalTreatments
    form_class = CrystalTreatmentsForm
    template_name = "medidas/crystal_treatment_add.html"
    success_url = reverse_lazy('medidas:treatments')

    def form_valid(self, form):
        form.instance.optic = self.request.user.get_opticuser()
        return super().form_valid(form)

    def form_invalid(self, form):
        print(colored(form.cleaned_data, 'red'))
        print(colored(form.errors, 'red'))
        return super().form_invalid(form)


@method_decorator(login_required, 'dispatch')
@method_decorator(permission_required('medidas.change_crystaltreatments', raise_exception=True), 'dispatch')
class CrystalTreatmentsUpdateView(UpdateView):
    """
    Vista de actualizar tratamiento
    """
    model = CrystalTreatments
    template_name = "medidas/crystal_treatment_add.html"
    form_class = CrystalTreatmentsForm
    success_url = reverse_lazy('medidas:treatments')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["update"] = True
        return context


@method_decorator(login_required, 'dispatch')
@method_decorator(permission_required('medidas.delete_crystaltreatments', raise_exception=True), 'dispatch')
class CrystalTreatmentsDeleteView(View):
    """
    Vista de eliminar tratamiento
    """

    def post(self, request, *args, **kwargs):
        pk = request.POST.get('treatment_id')
        treatment = get_object_or_404(CrystalTreatments, pk=pk)
        if treatment.optic != request.user.get_opticuser():
            raise PermissionDenied()
        treatment.delete()
        return redirect('medidas:treatments')


@method_decorator(login_required, 'dispatch')
class PrescriptionPDFDetailView(DetailView):
    """
    Vista de visualizar prescripcion en pdf
    """
    model = Prescription
    template_name = "medidas/prescription_pdf.html"
    context_object_name = 'prescription'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        random_choices = ['.', '', '-', '+', '+-', '1', '0', '...', '_']
        context["random"] = random.choice(random_choices)
        context["is_dip"] = self.object.is_dip
        if self.object.is_dip:
            if self.object.far_dnp_left:
                context["far_dip"] = str(
                    self.object.far_dnp_left * 2)[:-2]+"mm"
            else:
                context["far_dip"] = None
            if self.object.intermediate_dnp_left:
                context["intermediate_dip"] = str(
                    self.object.intermediate_dnp_left * 2)[:-2]+"mm"
            else:
                context["intermediate_dip"] = None
            if self.object.near_dnp_left:
                context["near_dip"] = str(
                    self.object.near_dnp_left * 2)[:-2]+"mm"
            else:
                context["near_dip"] = None
        return context


class CustomWeasyTemplateResponse(WeasyTemplateResponse):
    """
    Vista que renderiza el pdf
    """
    # customized response class to change the default URL fetcher

    def get_url_fetcher(self):
        # disable host and certificate check
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        return functools.partial(django_url_fetcher, ssl_context=context)


@method_decorator(login_required, 'dispatch')
class PrescriptionPDFPrintView(WeasyTemplateResponseMixin, PrescriptionPDFDetailView):
    """
    Vista que carga los estilos css al pdf
    """
    # output of PrescriptionView rendered as PDF with hardcoded CSS
    pdf_stylesheets = [
        'medidas' + settings.STATIC_URL + 'css/prescription.css',
    ]
    # show pdf in-line (default: True, show download dialog)
    pdf_attachment = False
    # custom response class to configure url-fetcher
    response_class = CustomWeasyTemplateResponse


class PrescriptionPDFDownloadView(WeasyTemplateResponseMixin, PrescriptionPDFDetailView):
    """
    Vista para descargar en pdf
    """
    # suggested filename (is required for attachment/download!)
    pdf_filename = 'foo.pdf'


class PrescriptionPDFImageView(WeasyTemplateResponseMixin, PrescriptionPDFDetailView):
    """
    Vista para la prescripcion en imagen
    """
    # generate a PNG image instead
    content_type = CONTENT_TYPE_PNG

    # dynamically generate filename
    def get_pdf_filename(self):
        return 'foo-{at}.pdf'.format(
            at=timezone.now().strftime('%Y%m%d-%H%M'),
        )


@method_decorator(login_required, 'dispatch')
@method_decorator(permission_required('medidas.add_subsidiary', raise_exception=True), 'dispatch')
class SubsidiaryCreateView(CreateView):
    """
    Vista que crea sucursal
    """
    model = Subsidiary
    template_name = "medidas/subsidiary_add.html"
    form_class = SubsidiaryForm
    success_url = reverse_lazy('medidas:index')

    def form_valid(self, form):
        optic = self.request.user.get_opticuser()
        form.instance.optic = optic
        return super().form_valid(form)


@method_decorator(login_required, 'dispatch')
@method_decorator(any_permission_required(['medidas.change_subsidiary', 'medidas.delete_subsidiary'], raise_exception=True), 'dispatch')
@method_decorator(permission_required('medidas.change_subsidiary', raise_exception=True), 'post')
class SubsidiaryUpdateView(UpdateView):
    """
    Vista actualizar sucursal
    """
    model = Subsidiary
    template_name = "medidas/subsidiary_add.html"
    form_class = SubsidiaryForm
    success_url = reverse_lazy('medidas:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["update"] = True
        return context


@method_decorator(login_required, 'dispatch')
@method_decorator(permission_required('medidas.delete_subsidiary', raise_exception=True), 'dispatch')
class SubsidiaryDeleteView(DeleteView):
    """
    Vista eliminar sucursal
    """
    model = Subsidiary
    success_url = reverse_lazy('medidas:index')


@method_decorator(login_required, 'dispatch')
class LaboratoryListView(ListView):
    """
    Vista de listar laboratorios
    """
    model = Laboratory
    context_object_name = 'laboratories'
    template_name = "medidas/crystal_laboratories.html"

    def get_queryset(self):
        opticUser = self.request.user.get_opticuser().id
        return Laboratory.objects.filter(optic=opticUser)


@method_decorator(login_required, 'dispatch')
@method_decorator(permission_required('medidas.add_laboratory', raise_exception=True), 'dispatch')
class LaboratoryCreateView(CreateView):
    """
    Vista crear laboratorio
    """
    model = Laboratory
    template_name = "medidas/crystal_laboratory_add.html"
    form_class = LaboratoryForm
    success_url = reverse_lazy('medidas:laboratories')

    def form_valid(self, form):
        optic = self.request.user.get_opticuser()
        form.instance.optic = optic
        return super().form_valid(form)


@method_decorator(login_required, 'dispatch')
@method_decorator(permission_required('medidas.change_laboratory', raise_exception=True), 'dispatch')
class LaboratoryUpdateView(UpdateView):
    """
    Vista actualizar laboratorio
    """
    model = Laboratory
    template_name = "medidas/crystal_laboratory_add.html"
    form_class = LaboratoryForm
    success_url = reverse_lazy('medidas:laboratories')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["update"] = True
        return context


@method_decorator(login_required, 'dispatch')
@method_decorator(permission_required('medidas.delete_laboratory', raise_exception=True), 'dispatch')
class LaboratoryDeleteView(View):
    """
    Vista eliminar laboratorio
    """

    def post(self, request, *args, **kwargs):
        pk = request.POST.get('laboratory_id')
        laboratory = get_object_or_404(Laboratory, pk=pk)
        if laboratory.optic != request.user.get_opticuser():
            raise PermissionDenied()
        laboratory.delete()
        return redirect('medidas:laboratories')
