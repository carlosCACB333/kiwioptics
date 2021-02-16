from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import date
import decimal
from termcolor import colored

# Create your models here.
class Patient(models.Model):

    class Gender(models.TextChoices):
        MALE = 'MALE','Masculino'
        FEMALE = 'FEMALE','Femenino'
        OTHER = 'OTHER','Otro'
    
    first_name = models.CharField("Nombres",max_length=100)    
    last_name = models.CharField("Apellidos",max_length=100)    
    dni = models.CharField("Dni",max_length=20, unique=True, blank=True, null=True)    
    gender = models.CharField("Genero", max_length=20, blank=True, choices=Gender.choices)
    phone = models.CharField("Celular",max_length=30, blank=True)
    age = models.IntegerField("Edad", blank=True, null=True)

    class Meta:
        verbose_name = "Paciente"
        verbose_name_plural = "Pacientes"
    
    def __str__(self):
        return f"{self.last_name} {self.first_name}"

# class Laboratory(models.Model):

#     name = models.CharField("Nombre", max_length=50)

#     class Meta:
#         verbose_name = ("Laboratorio")
#         verbose_name_plural = ("Laboratorios")

#     def __str__(self):
#         return self.name


class Prescription(models.Model):
    
    @staticmethod
    def generateChoices(start, end):
        choices = [( decimal.Decimal(f'{i*0.25}0') if i%2==0 else decimal.Decimal(f'{i*0.25}'), (f'{i*0.25}0' if i <= 0 else f'+{i*0.25}0') if i%2==0 else (f'{i*0.25}' if i <= 0 else f'+{i*0.25}')) for i in range(start,end)]
        for i, (value, name) in enumerate(choices):
            if value == decimal.Decimal(0):
                choices.insert(i+1, ('','---------'))
                break
        return choices

    spherical_choices = generateChoices.__func__(-100,101)
    cylinder_choices = generateChoices.__func__(-29, 1)
    axis_choices = [(i,f'{i}°') for i in range(0,181)]
    dip_choices = [(i,f'{i}mm') for i in range(50,81)]
    add_choices = generateChoices.__func__(1, 25)

    # print(colored(spherical_choices,'green'))
    # print(colored(cylinder_choices,'red'))
    # print(colored(axis_choices,'green'))
    # print(colored(dip_choices,'red'))
    # print(colored(add_choices,'green'))

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, verbose_name="Paciente")
    # laboratory = models.ForeignKey(Laboratory, on_delete=models.SET_NULL,verbose_name="Laboratorio", blank=True, null=True)
    date = models.DateField(verbose_name='Fecha', default=date.today)
    far_spherical_right = models.DecimalField("Esf. derecho Lejos", max_digits=4, decimal_places=2, blank=True, null=True,choices=spherical_choices)
    far_cylinder_right = models.DecimalField("Cil. derecho Lejos", max_digits=4, decimal_places=2, blank=True, null=True, choices=cylinder_choices)
    far_axis_right = models.PositiveSmallIntegerField("Eje derecho Lejos", validators=[MaxValueValidator(180,'El eje solo permite valores entre 0° y 180°')], blank=True, null=True, choices=axis_choices)
    far_av_right = models.CharField("Av. derecho lejos",max_length=50, blank=True, null=True)
    far_spherical_left = models.DecimalField("Esf. izquierdo Lejos", max_digits=4, decimal_places=2, blank=True, null=True,choices=spherical_choices)
    far_cylinder_left = models.DecimalField("Cil. izquierdo Lejos", max_digits=4, decimal_places=2, blank=True, null=True, choices=cylinder_choices)
    far_axis_left = models.PositiveSmallIntegerField("Eje izquierdo Lejos",validators=[MaxValueValidator(180,'El eje solo permite valores entre 0° y 180°')], blank=True, null=True, choices=axis_choices)
    far_av_left = models.CharField("Av. izquierdo lejos",max_length=50, blank=True, null=True)
    near_spherical_right = models.DecimalField("Esf. derecho Cerca", max_digits=4, decimal_places=2, blank=True, null=True,choices=spherical_choices)
    near_cylinder_right = models.DecimalField("Cil. derecho Cerca", max_digits=4, decimal_places=2, blank=True, null=True, choices=cylinder_choices)
    near_axis_right = models.PositiveSmallIntegerField("Eje derecho Cerca",validators=[MaxValueValidator(180,'El eje solo permite valores entre 0° y 180°')], blank=True, null=True, choices=axis_choices)
    near_av_right = models.CharField("Av. derecho Cerca",max_length=50, blank=True, null=True)
    near_spherical_left = models.DecimalField("Esf. izquierdo Cerca", max_digits=4, decimal_places=2, blank=True, null=True,choices=spherical_choices)
    near_cylinder_left = models.DecimalField("Cil. izquierdo Cerca", max_digits=4, decimal_places=2, blank=True, null=True, choices=cylinder_choices)
    near_axis_left = models.PositiveSmallIntegerField("Eje izquierdo Cerca", validators=[MaxValueValidator(180,'El eje solo permite valores entre 0 y 180')], blank=True, null=True, choices=axis_choices)
    near_av_left = models.CharField("Av. izquierdo Cerca",max_length=50, blank=True, null=True)
    observation = models.TextField("Observacion", blank=True)
    far_dip = models.PositiveSmallIntegerField("Dip. lejos", blank=True, null=True, choices=dip_choices)
    near_dip = models.PositiveSmallIntegerField("Dip. cerca", blank=True, null=True, choices=dip_choices)
    intermediate_add = models.DecimalField("Add. intermedio", max_digits=4, decimal_places=2, blank=True, null=True, choices=add_choices)
    near_add = models.DecimalField("Add. cerca", max_digits=4, decimal_places=2, blank=True, null=True, choices=add_choices)
    price = models.DecimalField('Precio',max_digits=10, decimal_places=2, default=0,validators=[MinValueValidator(0,'No se permite el valor ingresado')])

    class Meta:
        verbose_name = "Receta"
        verbose_name_plural = "Recetas"

    def __str__(self):
        return f"""{self.patient} S/{self.price}
        ODL:{self.far_spherical_right if self.far_spherical_right is not None else '?'}({self.far_cylinder_right if self.far_cylinder_right is not None else '?'}){self.far_axis_right if self.far_axis_right is not None else '?'}° 
        OIL:{self.far_spherical_left if self.far_spherical_left is not None else '?'}({self.far_cylinder_left if self.far_cylinder_left is not None else '?'}){self.far_axis_left if self.far_axis_left is not None else '?'}° 
        ODC:{self.near_spherical_right if self.near_spherical_right is not None else '?'}({self.near_cylinder_right if self.near_cylinder_right is not None else '?'}){self.near_axis_right if self.near_axis_right is not None else '?'}° 
        OIC:{self.near_spherical_left if self.near_spherical_left is not None else '?'}({self.near_cylinder_left if self.near_cylinder_left is not None else '?'}){self.near_axis_left if self.near_axis_left is not None else '?'}° 
        """



