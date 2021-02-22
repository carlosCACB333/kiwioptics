from django.urls import path
from . import views

app_name = 'medidas'
urlpatterns = [
    path('', views.index, name='index'),
    path('patients/', views.PatientListView.as_view(), name='patients'),
    path('patients/<int:pk>/add-prescription', views.patient_add_prescription, name='patient-add'),
    # path('patients/<int:pk>/', views.patient_detail, name='patient-detail'),
    path('prescriptions/', views.PrescriptionListView.as_view(), name='prescriptions'),
    path('prescriptions/add', views.add_prescription, name='prescription-add'),
    path('prescriptions/<int:pk>/', views.prescription_detail, name='prescription-detail'),
    path('prescriptions/<int:pk>/change/', views.prescription_update, name='prescription-update'),
    path('prescriptions/delete/', views.prescription_delete, name='prescription-delete'),
    path('test/', views.TestView.as_view()),
]