import factory
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyInteger, FuzzyChoice, FuzzyDecimal, FuzzyDate
from .models import Prescription, Patient
import random
import datetime

class PatientFactory(DjangoModelFactory):
    class Meta:
        model = Patient

    full_name = factory.Faker('name')
    dni = FuzzyInteger(10000000,99999999) 
    gender = factory.Iterator([Patient.Gender.MALE,Patient.Gender.FEMALE,Patient.Gender.OTHER])
    phone = factory.Faker('phone_number')
    job = factory.Faker('job')

class PrescriptionFactory(DjangoModelFactory):
    class Meta:
        model = Prescription

    patient = factory.SubFactory(PatientFactory)
    date = FuzzyDate(datetime.date(2008, 1, 1))
    time = factory.Faker('time')
    far_spherical_right = FuzzyChoice([choice[0] for choice in Prescription.spherical_choices])
    far_cylinder_right = FuzzyChoice([choice[0] for choice in Prescription.cylinder_choices])
    far_axis_right = FuzzyChoice([choice[0] for choice in Prescription.axis_choices])
    far_av_right = '6/20'
    far_dnp_right = FuzzyChoice([choice[0] for choice in Prescription.dnp_choices])
    far_spherical_left = FuzzyChoice([choice[0] for choice in Prescription.spherical_choices])
    far_cylinder_left = FuzzyChoice([choice[0] for choice in Prescription.cylinder_choices])
    far_axis_left = FuzzyChoice([choice[0] for choice in Prescription.axis_choices])
    far_av_left = '9/20'
    far_dnp_left = FuzzyChoice([choice[0] for choice in Prescription.dnp_choices])
    intermediate_spherical_right = FuzzyChoice([choice[0] for choice in Prescription.spherical_choices])
    intermediate_cylinder_right = FuzzyChoice([choice[0] for choice in Prescription.cylinder_choices])
    intermediate_axis_right = FuzzyChoice([choice[0] for choice in Prescription.axis_choices])
    intermediate_av_right = '12/20'
    intermediate_dnp_right = FuzzyChoice([choice[0] for choice in Prescription.dnp_choices])
    intermediate_spherical_left = FuzzyChoice([choice[0] for choice in Prescription.spherical_choices])
    intermediate_cylinder_left = FuzzyChoice([choice[0] for choice in Prescription.cylinder_choices])
    intermediate_axis_left = FuzzyChoice([choice[0] for choice in Prescription.axis_choices])
    intermediate_av_left = '15/20'
    intermediate_dnp_left = FuzzyChoice([choice[0] for choice in Prescription.dnp_choices])
    near_spherical_right = FuzzyChoice([choice[0] for choice in Prescription.spherical_choices])
    near_cylinder_right = FuzzyChoice([choice[0] for choice in Prescription.cylinder_choices])
    near_axis_right = FuzzyChoice([choice[0] for choice in Prescription.axis_choices])
    near_av_right = '6/20'
    near_dnp_right = FuzzyChoice([choice[0] for choice in Prescription.dnp_choices])
    near_spherical_left = FuzzyChoice([choice[0] for choice in Prescription.spherical_choices])
    near_cylinder_left = FuzzyChoice([choice[0] for choice in Prescription.cylinder_choices])
    near_axis_left = FuzzyChoice([choice[0] for choice in Prescription.axis_choices])
    near_av_left = '6/20'
    near_dnp_left = FuzzyChoice([choice[0] for choice in Prescription.dnp_choices])
    patient_notes = factory.Faker('paragraph', nb_sentences=2)
    laboratory_notes = factory.Faker('paragraph', nb_sentences=2)
    optic_notes = factory.Faker('paragraph', nb_sentences=2)
    intermediate_add = FuzzyChoice([choice[0] for choice in Prescription.add_choices])
    near_add = FuzzyChoice([choice[0] for choice in Prescription.add_choices])
    measure_price = FuzzyDecimal(20.5, 351.5)
    crystals_price = FuzzyDecimal(20.5, 351.5)
    frame_price = FuzzyDecimal(20.5, 351.5)


