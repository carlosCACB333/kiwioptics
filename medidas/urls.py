from django.urls import path
from . import views

app_name = 'medidas'
urlpatterns = [
    path('', views.index, name='index'),
    path('prescriptions/', views.PrescriptionListView.as_view(), name='prescriptions'),
    path('patients/', views.PatientListView.as_view(), name='patients'),
    path('prescription-add/', views.prescription, name='prescription-add'),
    path('prescription/<int:pk>/', views.prescription_detail, name='prescription-detail'),
    path('prescription/<int:pk>/change/', views.prescription_update, name='prescription-update'),
]