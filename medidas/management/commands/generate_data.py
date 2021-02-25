import random

from django.db import transaction
from django.core.management.base import BaseCommand
from django.core.exceptions import ValidationError
from django.db.utils import DataError

from medidas.models import Patient, Prescription
from medidas.factories import (
    PatientFactory,
    PrescriptionFactory,
)

NUM_PATIENTS = 300
NUM_PRESCRIPTIONS = 1000

class Command(BaseCommand):
    help = "Generates test data"

    def handle(self, *args, **kwargs):
        self.stdout.write("Deleting old data...")
        models = [Prescription, Patient,]
        for model in models:
            model.objects.all().delete()

        self.stdout.write("Creating new data...")
        # Create all the patients
        patients = []
        for _ in range(NUM_PATIENTS):
            try:
                patient = PatientFactory()
                patients.append(patient)
            except DataError:
                print('DataError')

        # Create all the prescriptions
        for _ in range(NUM_PRESCRIPTIONS):
            patient = random.choice(patients)
            try:
                prescription = PrescriptionFactory(patient=patient)
            except ValidationError:
                print('ValidationError')
            except ValueError:
                print('ValueError')