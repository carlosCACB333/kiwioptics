from rest_framework import serializers
from .models import Patient, Prescription, Subsidiary


class PatientSerializer(serializers.ModelSerializer):
    model = Patient

    class Meta:
        model = Patient
        fields = ('__all__')


class PrescriptionSerializer(serializers.Serializer):
    dato = serializers.IntegerField()
    total = serializers.IntegerField()


class SubsidiarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subsidiary
        fields = ('subsidiary_name',)


class SubsidiaryPrescriptionSerializer(serializers.Serializer):
    subsidiary = serializers.SerializerMethodField()
    # subsidiary = serializers.IntegerField()
    dato = serializers.IntegerField()
    total = serializers.IntegerField()

    def get_subsidiary(self, obj):
        id = obj.get('subsidiary','')
        if id:
            query=Subsidiary.objects.get(id=id)
        else:
            query=Subsidiary(subsidiary_name='Desconocido')
        return SubsidiarySerializer(query).data 