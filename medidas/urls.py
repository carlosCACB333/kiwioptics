from django.urls import path
from . import views

app_name = 'medidas'
urlpatterns = [
    path('', views.index, name='index'),
    path('prescription', views.prescription, name='prescription'),
    path('prescription-list', views.prescription_list, name='prescription-list'),
]