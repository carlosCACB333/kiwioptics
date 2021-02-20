from django.urls import path
from . import views

app_name = 'medidas'
urlpatterns = [
    path('', views.index, name='index'),
    path('patients/', views.PatientListView.as_view(), name='patients'),
    path('patients/<int:pk>/add-prescription', views.patient_add_prescription, name='patient-add'),
    path('prescriptions/', views.PrescriptionListView.as_view(), name='prescriptions'),
    path('prescription-add/', views.prescription, name='prescription-add'),
    path('prescription/<int:pk>/', views.prescription_detail, name='prescription-detail'),
    path('prescription/<int:pk>/change/', views.prescription_update, name='prescription-update'),
    path('prescription/delete/', views.prescription_delete, name='prescription-delete'),
    path('test/', views.TestView.as_view()),
]