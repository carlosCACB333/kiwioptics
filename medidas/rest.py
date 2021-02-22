from rest_framework.generics import  ListAPIView
from .serializers import PatientSerializer
from .models import Patient

class PatientListApiView(ListAPIView):
     serializer_class=PatientSerializer
     def get_queryset(self):
          id = self.kwargs['id']
          return Patient.objects.filter(id=id);