import random

from django.db import transaction
from django.core.management.base import BaseCommand
from django.core.exceptions import ValidationError
from django.db.utils import DataError

from medidas.models import Patient, Prescription
from users.models import Account
from medidas.factories import (
    PatientFactory,
    PrescriptionFactory,
)

USERNAME = 'solanito2000@hotmail.com'
NUM_PATIENTS = 500
NUM_PRESCRIPTIONS = 5000

class Command(BaseCommand):
    help = "Generates test data"

    def handle(self, *args, **kwargs):
        self.stdout.write("Deleting old data...")
        models = [Prescription, Patient,]
        account = Account.objects.get(username=USERNAME)
        optic = account.get_opticuser()
        for model in models:
            model.objects.filter(optic=optic).delete()
        self.stdout.write("Creating new data...")
        # Create all the patients
        patients = []
        for _ in range(NUM_PATIENTS):
            try:
                patient = PatientFactory(optic=optic)
                patients.append(patient)
            except DataError:
                print('DataError')

        # Create all the prescriptions
        for _ in range(NUM_PRESCRIPTIONS):
            patient = random.choice(patients)
            try:
                prescription = PrescriptionFactory(optic=optic,patient=patient, is_dip=True)
                print(f'{_/NUM_PRESCRIPTIONS*100}%')
            except ValidationError:
                print('ValidationError')
            except ValueError:
                print('ValueError')