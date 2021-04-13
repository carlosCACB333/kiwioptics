from django.urls import path
from . import views
from . import  rest


app_name = 'medidas'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('patients/', views.PatientListView.as_view(), name='patients'),
    path('patients/<int:pk>/add-prescription/', views.patient_add_prescription, name='patient-add'),
    # path('patients/<int:pk>/', views.patient_detail, name='patient-detail'),
    path('prescriptions/', views.PrescriptionListView.as_view(), name='prescriptions'),
    path('prescriptions/add/', views.add_prescription, name='prescription-add'),
    path('prescriptions/<int:pk>/', views.prescription_detail, name='prescription-detail'),
    path('prescriptions/<int:pk>/change/', views.prescription_update, name='prescription-update'),
    path('prescriptions/delete/', views.prescription_delete, name='prescription-delete'),
    path('crystals/', views.CrystalListView.as_view(), name='crystals'),
    path('crystals/add', views.CrystalCreateView.as_view(), name='crystal-add'),
    path('crystals/<int:pk>/change', views.CrystalUpdateView.as_view(), name='crystal-update'),
    path('crystals/delete/', views.CrystalDeleteView.as_view(), name='crystal-delete'),
    path('crystals/materials', views.CrystalMaterialListView.as_view(), name='materials'),
    path('crystals/materials/add', views.CrystalMaterialCreateView.as_view(), name='material-add'),
    path('crystals/materials/<int:pk>/change', views.CrystalMaterialUpdateView.as_view(), name='material-update'),
    path('crystals/materials/delete', views.CrystalMaterialDeleteView.as_view(), name='material-delete'),
    path('crystals/treatments', views.CrystalTreatmentsListView.as_view(), name='treatments'),
    path('crystals/treatments/add', views.CrystalTreatmentsCreateView.as_view(), name='treatment-add'),
    path('crystals/treatments/<int:pk>/change', views.CrystalTreatmentsUpdateView.as_view(), name='treatment-update'),
    path('crystals/treatments/delete', views.CrystalTreatmentsDeleteView.as_view(), name='treatment-delete'),
    
    # api rest-framework
    path('api/patientList/', rest.PatientListApiView.as_view(),name='rest-patient-list'),
    path('api/patientCreate/', rest.PatientCreateApiView.as_view(),name='rest-patient-create'),
    path('api/patientDetail/<pk>/', rest.PatientDetailApiView.as_view(),name='rest-patient-detail'),
    path('api/patientDelete/<pk>/', rest.PatientDeleteApiView.as_view(),name='rest-patient-delete'),
    path('api/patientUpdate/<pk>/', rest.PatientUpdateApiWiew.as_view(),name='rest-patient-update'),
   
]