from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveAPIView,
    DestroyAPIView,
    UpdateAPIView,  # no trae los datos del paciente
    RetrieveUpdateAPIView,
)
from .serializers import PatientSerializer
from .models import Patient


class PatientListApiView(ListAPIView):
    """ api para enviar un paciente con el id dado"""
    serializer_class = PatientSerializer

    def get_queryset(self):
        return Patient.objects.all();


class PatientCreateApiView(CreateAPIView):
    """ api para crear un paciente """
    serializer_class = PatientSerializer


class PatientDetailApiView(RetrieveAPIView):
    """ api para mostrar el detalle de un pacientev"""
    serializer_class = PatientSerializer
    queryset = Patient.objects.all()


class PatientDeleteApiView(DestroyAPIView):
    """ api para eliminar un paciente"""
    serializer_class = PatientSerializer
    queryset = Patient.objects.all();


class PatientUpdateApiWiew(RetrieveUpdateAPIView):
    """ api para modificar un paciente"""
    serializer_class = PatientSerializer
    queryset = Patient.objects.all();
