from rest_framework import serializers
from .models import Patient,Prescription


class PatientSerializer(serializers.ModelSerializer):
    model=Patient
    class Meta:
        model = Patient
        fields = ('__all__')

class PrescriptionSerializer(serializers.Serializer):
    dato=serializers.IntegerField()
    total=serializers.IntegerField()
