from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.timezone import now
from users.models import OpticUser, Account
import decimal
from termcolor import colored

# Create your models here.
class Patient(models.Model):

    class Gender(models.TextChoices):
        MALE = 'MALE','Masculino'
        FEMALE = 'FEMALE','Femenino'
        OTHER = 'OTHER','Otro'
    
    patient_optic_id = models.PositiveIntegerField(blank=True)
    optic = models.ForeignKey(OpticUser, verbose_name="Optica", on_delete=models.CASCADE, null=False)
    full_name = models.CharField("Nombre completo", max_length=100)  
    dni = models.CharField("Dni",max_length=20, unique=True, blank=True, null=True)    
    gender = models.CharField("Genero", max_length=20, blank=True, choices=Gender.choices)
    phone = models.CharField("Celular",max_length=30, blank=True)
    job = models.CharField('Ocupacion', max_length=70, blank=True)

    class Meta:
        verbose_name = "Paciente"
        verbose_name_plural = "Pacientes"
        unique_together = (('optic','dni'),('optic','patient_optic_id'))
    
    def __str__(self):
        return f"{self.full_name}"

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self._state.adding is True:
            optic = OpticUser.objects.get(pk=self.optic.id)
            last_patient = optic.patient_set.last()
            if last_patient:
                patient_optic_id = last_patient.patient_optic_id + 1
            else:
                patient_optic_id = 1
            self.patient_optic_id = patient_optic_id
        return super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)

# class Diagnosis(models.Model):
#     class DiagnosisChoices(models.TextChoices):
#         GLAUCOMA = 'GLAUCOMA','Glaucoma'
#         CATARACT = 'CATARACT','Catarata'
#         MYOPIA = 'MYOPIA','Miopía'
#         FARSIGHTEDNESS = 'FARSIGHTEDNESS','Hipermetropía'
#         ASTIGMATISM = 'ASTIGMATISM','Astigmatismo'
#         PRESBYOPIA = 'PRESBYOPIA','Presbicia'
#         AMBLYOPIA = 'AMBLYOPIA', 'Ambliopía'
#         SQUINT = 'SQUINT', 'Estrabismo'
#         SQUINT = 'SQUINT', 'Daltonismo'
    
#     name = models.CharField("Diagnostico", max_length=50, blank=False, null=False, choices=DiagnosisChoices.choices)

#     class Meta:
#         verbose_name = "Diagnostico"
#         verbose_name_plural = "Diagnostico"

#     def __str__(self):
#         return self.name


class Subsidiary(models.Model):
    name = models.CharField("Nombre",max_length=50, blank=True)
    direction = models.CharField("Dirección",max_length=80, blank=True)
    optic = models.ForeignKey(OpticUser, verbose_name="Optica", on_delete=models.CASCADE, null=False)

    class Meta:
        verbose_name = "Sucursal"
        verbose_name_plural = "Sucursales"

    def __str__(self):
        return self.name

class CrystalTreatments(models.Model):

    name = models.CharField("Tratamiento", max_length=80)
    description = models.TextField("Descripcion", blank=True)
    optic = models.ForeignKey(OpticUser, verbose_name="Optica", on_delete=models.CASCADE, null=False)

    class Meta:
        verbose_name = "Tratamiento"
        verbose_name_plural = "Tratamientos"

    def __str__(self):
        return self.name

class CrystalMaterial(models.Model):

    name = models.CharField("Material", max_length=80)
    retracting_index = models.DecimalField("Indice retractivo", max_digits=4, decimal_places=3, blank=True, null=True)
    abbe = models.DecimalField("Valor abbe", max_digits=3, decimal_places=1, blank=True, null=True)
    description = models.TextField("Descripcion", blank=True)
    optic = models.ForeignKey(OpticUser, verbose_name="Optica", on_delete=models.CASCADE, null=False)

    class Meta:
        verbose_name = "Material de la luna"
        verbose_name_plural = "Materiales de las lunas"

    def __str__(self):
        return self.name

class Crystal(models.Model):

    name = models.CharField("Material", max_length=120)
    material = models.ForeignKey(CrystalMaterial, verbose_name="Material", on_delete=models.CASCADE)
    treatments = models.ManyToManyField(CrystalTreatments, verbose_name="Tratamientos", blank=True)
    default_price = models.DecimalField('Precio de los lentes',max_digits=10, decimal_places=2, default=0,validators=[MinValueValidator(0,'No se permite el valor ingresado')])
    optic = models.ForeignKey(OpticUser, verbose_name="Optica", on_delete=models.CASCADE, null=False)

    class Meta:
        verbose_name = "Crystal"
        verbose_name_plural = "Crystals"

    def __str__(self):
        return self.name


class Prescription(models.Model):
    class PrescriptionType(models.TextChoices):
        MONOFOCAL = 'MONOFOCAL','Monofocal'
        BIFOCAL = 'BIFOCAL','Bifocal'
        PROGRESSIVE = 'PROGRESSIVE','Progressivo'

    @staticmethod
    def generateChoices(start, end):
        choices = [( decimal.Decimal(f'{i*0.25}0') if i%2==0 else decimal.Decimal(f'{i*0.25}'), (f'{i*0.25}0' if i <= 0 else f'+{i*0.25}0') if i%2==0 else (f'{i*0.25}' if i <= 0 else f'+{i*0.25}')) for i in range(end-1,start-1,-1)]
        for i, (value, name) in enumerate(choices):
            if value == decimal.Decimal(0):
                choices.insert(i, ('','---------'))
                break
        return choices
    
    spherical_choices = generateChoices.__func__(-100,101)
    cylinder_choices = generateChoices.__func__(-29, 1)
    axis_choices = [(i,f'{i}°') for i in range(180,-1,-1)]
    axis_choices.append(('','---------'))
    dip_choices = [(i,f'{i}mm') for i in range(81,40,-1)]
    dip_choices.append(('','---------'))
    dnp_choices = [(decimal.Decimal(i/2),f'{i/2}mm') for i in range(81,40,-1)]
    dnp_choices.append(('','---------'))
    add_choices = generateChoices.__func__(1, 25)
    add_choices.append(('','---------'))
    # print(colored(spherical_choices,'green'))
    # print(colored(cylinder_choices,'red'))
    # print(colored(axis_choices,'green'))
    # print(colored(dip_choices,'red'))
    # print(colored(add_choices,'green'))

    optic = models.ForeignKey(OpticUser, verbose_name="Optica", on_delete=models.CASCADE, null=False)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, verbose_name="Paciente")
    subsidiary = models.ForeignKey(Subsidiary, on_delete=models.CASCADE, verbose_name="Sucursal", blank=True, null=True)
    doctor = models.ForeignKey(Account, verbose_name="Doctor", on_delete=models.CASCADE, null=False)
    prescription_optic_id = models.PositiveIntegerField(blank=True)
    prescription_type = models.CharField("Tipo", max_length=50, choices=PrescriptionType.choices, null=False, blank=False)
    # laboratory = models.ForeignKey(Laboratory, on_delete=models.SET_NULL,verbose_name="Laboratorio", blank=True, null=True)
    date = models.DateTimeField(verbose_name='Fecha', default=now)
    far_spherical_right = models.DecimalField("Esf. derecho Lejos", max_digits=4, decimal_places=2, blank=True, null=True,choices=spherical_choices)
    far_cylinder_right = models.DecimalField("Cil. derecho Lejos", max_digits=4, decimal_places=2, blank=True, null=True, choices=cylinder_choices)
    far_axis_right = models.PositiveSmallIntegerField("Eje derecho Lejos", validators=[MaxValueValidator(180,'El eje solo permite valores entre 0° y 180°')], blank=True, null=True, choices=axis_choices)
    far_av_right = models.CharField("Av. derecho lejos",max_length=50, blank=True, null=True)
    far_dnp_right = models.DecimalField("Dnp. derecho lejos", max_digits=3, decimal_places=1, blank=True, null=True, choices=dnp_choices)
    far_spherical_left = models.DecimalField("Esf. izquierdo Lejos", max_digits=4, decimal_places=2, blank=True, null=True,choices=spherical_choices)
    far_cylinder_left = models.DecimalField("Cil. izquierdo Lejos", max_digits=4, decimal_places=2, blank=True, null=True, choices=cylinder_choices)
    far_axis_left = models.PositiveSmallIntegerField("Eje izquierdo Lejos",validators=[MaxValueValidator(180,'El eje solo permite valores entre 0° y 180°')], blank=True, null=True, choices=axis_choices)
    far_av_left = models.CharField("Av. izquierdo lejos",max_length=50, blank=True, null=True)
    far_dnp_left = models.DecimalField("Dnp. izquierdo lejos", max_digits=3, decimal_places=1, blank=True, null=True,choices=dnp_choices)
    intermediate_spherical_right = models.DecimalField("Esf. derecho intermedio", max_digits=4, decimal_places=2, blank=True, null=True,choices=spherical_choices)
    intermediate_cylinder_right = models.DecimalField("Cil. derecho intermedio", max_digits=4, decimal_places=2, blank=True, null=True, choices=cylinder_choices)
    intermediate_axis_right = models.PositiveSmallIntegerField("Eje derecho Lintermedio", validators=[MaxValueValidator(180,'El eje solo permite valores entre 0° y 180°')], blank=True, null=True, choices=axis_choices)
    intermediate_av_right = models.CharField("Av. derecho intermedio",max_length=50, blank=True, null=True)
    intermediate_dnp_right = models.DecimalField("Dnp. derecho intermedio", max_digits=3, decimal_places=1, blank=True, null=True,choices=dnp_choices)
    intermediate_spherical_left = models.DecimalField("Esf. izquierdo intermedio", max_digits=4, decimal_places=2, blank=True, null=True,choices=spherical_choices)
    intermediate_cylinder_left = models.DecimalField("Cil. izquierdo intermedio", max_digits=4, decimal_places=2, blank=True, null=True, choices=cylinder_choices)
    intermediate_axis_left = models.PositiveSmallIntegerField("Eje izquierdo intermedio",validators=[MaxValueValidator(180,'El eje solo permite valores entre 0° y 180°')], blank=True, null=True, choices=axis_choices)
    intermediate_av_left = models.CharField("Av. izquierdo intermedio",max_length=50, blank=True, null=True)
    intermediate_dnp_left = models.DecimalField("Dnp. izquierdo intermedio", max_digits=3, decimal_places=1, blank=True, null=True,choices=dnp_choices)
    near_spherical_right = models.DecimalField("Esf. derecho Cerca", max_digits=4, decimal_places=2, blank=True, null=True,choices=spherical_choices)
    near_cylinder_right = models.DecimalField("Cil. derecho Cerca", max_digits=4, decimal_places=2, blank=True, null=True, choices=cylinder_choices)
    near_axis_right = models.PositiveSmallIntegerField("Eje derecho Cerca",validators=[MaxValueValidator(180,'El eje solo permite valores entre 0° y 180°')], blank=True, null=True, choices=axis_choices)
    near_av_right = models.CharField("Av. derecho Cerca",max_length=50, blank=True, null=True)
    near_dnp_right = models.DecimalField("Dnp. derecho Cerca", max_digits=3, decimal_places=1, blank=True, null=True,choices=dnp_choices)
    near_spherical_left = models.DecimalField("Esf. izquierdo Cerca", max_digits=4, decimal_places=2, blank=True, null=True,choices=spherical_choices)
    near_cylinder_left = models.DecimalField("Cil. izquierdo Cerca", max_digits=4, decimal_places=2, blank=True, null=True, choices=cylinder_choices)
    near_axis_left = models.PositiveSmallIntegerField("Eje izquierdo Cerca", validators=[MaxValueValidator(180,'El eje solo permite valores entre 0 y 180')], blank=True, null=True, choices=axis_choices)
    near_av_left = models.CharField("Av. izquierdo Cerca",max_length=50, blank=True, null=True)
    near_dnp_left = models.DecimalField("Dnp. izquierdo Cerca", max_digits=3, decimal_places=1, blank=True, null=True,choices=dnp_choices)
    observation = models.TextField("Observacion", blank=True)
    intermediate_add = models.DecimalField("Add. intermedio", max_digits=4, decimal_places=2, blank=True, null=True, choices=add_choices)
    near_add = models.DecimalField("Add. cerca", max_digits=4, decimal_places=2, blank=True, null=True, choices=add_choices)
    diagnosis = models.CharField("Diagnostico", max_length=100)
    measure_price = models.DecimalField('Precio de la medida',max_digits=10, decimal_places=2, default=0,validators=[MinValueValidator(0,'No se permite el valor ingresado')])
    crystals_price = models.DecimalField('Precio de las lunas',max_digits=10, decimal_places=2, default=0,validators=[MinValueValidator(0,'No se permite el valor ingresado')])
    frame = models.CharField("Descripcion de la montura", max_length=120)
    frame_price = models.DecimalField('Precio de la montura',max_digits=10, decimal_places=2, default=0,validators=[MinValueValidator(0,'No se permite el valor ingresado')])

    class Meta:
        verbose_name = "Receta"
        verbose_name_plural = "Recetas"
        unique_together = ('optic','prescription_optic_id')

    def __str__(self):
        return f"""{self.patient} S/{self.price}
        """
        # ODL:{self.far_spherical_right if self.far_spherical_right is not None else '?'}({self.far_cylinder_right if self.far_cylinder_right is not None else '?'}){self.far_axis_right if self.far_axis_right is not None else '?'}° 
        # OIL:{self.far_spherical_left if self.far_spherical_left is not None else '?'}({self.far_cylinder_left if self.far_cylinder_left is not None else '?'}){self.far_axis_left if self.far_axis_left is not None else '?'}° 
        # ODC:{self.near_spherical_right if self.near_spherical_right is not None else '?'}({self.near_cylinder_right if self.near_cylinder_right is not None else '?'}){self.near_axis_right if self.near_axis_right is not None else '?'}° 
        # OIC:{self.near_spherical_left if self.near_spherical_left is not None else '?'}({self.near_cylinder_left if self.near_cylinder_left is not None else '?'}){self.near_axis_left if self.near_axis_left is not None else '?'}° 

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self._state.adding is True:
            optic = OpticUser.objects.get(pk=self.optic.id)
            last_prescription = optic.prescription_set.last()
            if last_prescription:
                prescription_optic_id = last_prescription.prescription_optic_id + 1
            else:
                prescription_optic_id = 1
            self.prescription_optic_id = prescription_optic_id
        return super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)
