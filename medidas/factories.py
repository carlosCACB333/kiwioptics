import factory
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyInteger, FuzzyChoice, FuzzyDecimal
from .models import Prescription, Patient
import random

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
    far_spherical_right = FuzzyChoice([choice[0] for choice in Prescription.spherical_choices])
    far_cylinder_right = FuzzyChoice([choice[0] for choice in Prescription.cylinder_choices])
    far_axis_right = FuzzyChoice([choice[0] for choice in Prescription.axis_choices])
    far_av_right = '6/20'
    far_spherical_left = FuzzyChoice([choice[0] for choice in Prescription.spherical_choices])
    far_cylinder_left = FuzzyChoice([choice[0] for choice in Prescription.cylinder_choices])
    far_axis_left = FuzzyChoice([choice[0] for choice in Prescription.axis_choices])
    far_av_left = '6/20'
    intermediate_spherical_right = FuzzyChoice([choice[0] for choice in Prescription.spherical_choices])
    intermediate_cylinder_right = FuzzyChoice([choice[0] for choice in Prescription.cylinder_choices])
    intermediate_axis_right = FuzzyChoice([choice[0] for choice in Prescription.axis_choices])
    intermediate_av_right = '6/20'
    intermediate_spherical_left = FuzzyChoice([choice[0] for choice in Prescription.spherical_choices])
    intermediate_cylinder_left = FuzzyChoice([choice[0] for choice in Prescription.cylinder_choices])
    intermediate_axis_left = FuzzyChoice([choice[0] for choice in Prescription.axis_choices])
    intermediate_av_left = '6/20'
    near_spherical_right = FuzzyChoice([choice[0] for choice in Prescription.spherical_choices])
    near_cylinder_right = FuzzyChoice([choice[0] for choice in Prescription.cylinder_choices])
    near_axis_right = FuzzyChoice([choice[0] for choice in Prescription.axis_choices])
    near_av_right = '6/20'
    near_spherical_left = FuzzyChoice([choice[0] for choice in Prescription.spherical_choices])
    near_cylinder_left = FuzzyChoice([choice[0] for choice in Prescription.cylinder_choices])
    near_axis_left = FuzzyChoice([choice[0] for choice in Prescription.axis_choices])
    near_av_left = '6/20'
    observation = factory.Faker('paragraph', nb_sentences=2)
    far_dip = FuzzyChoice([choice[0] for choice in Prescription.dip_choices])
    near_dip = FuzzyChoice([choice[0] for choice in Prescription.dip_choices])
    intermediate_add = FuzzyChoice([choice[0] for choice in Prescription.add_choices])
    near_add = FuzzyChoice([choice[0] for choice in Prescription.add_choices])
    price = FuzzyDecimal(20.5, 351.5)

