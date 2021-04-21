from django.contrib import admin
from .models import Prescription, Patient, Crystal, CrystalMaterial, CrystalTreatments
from users.models import Account
# Register your models here.

# @admin.register(Crystal)
# class CrystalAdmin(admin.ModelAdmin):
#     list_display = (
#         'id',
#         'crystal_name',
#         'material',
#         'get_treatments',
#         'default_price',
#         'optic',
#     )

#     def get_treatments(self, obj):
#         return ", ".join([p.name for p in obj.treatments.all()])
    
#     get_treatments.short_description = 'Tratamientos'


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'dni',
        'full_name',
        'phone',
    )
    list_display_links = (
        'id',
        'dni',
        'full_name',
    )
    search_fields = (
        'dni',
        'full_name',
    )

    def full_name(self, obj):
        return f"{obj.full_name}"



# @admin.register(Laboratory)
# class LaboratoryAdmin(admin.ModelAdmin):
#     list_display = (
#         'id',
#         'name',
#     )
#     list_display_links = (
#         'id',
#         'name',
#     )
#     search_fields = (
#         'name',
#     )


@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Prescription._meta.get_fields() if field.name != 'observation']
    fieldsets = (
        (None, {
            "fields": (
                'patient', 'date', 'doctor',
            ),
        }),
        ('Medidas de Lejos', {
            'classes': (
                'collapse',
            ),
            "fields": (
                ('far_spherical_right','far_cylinder_right','far_axis_right'),
                ('far_spherical_left','far_cylinder_left','far_axis_left'),
            ),
        }),
        ('Medidas de Cerca', {
            'classes': (
                'collapse',
            ),
            "fields": (
                ('near_spherical_right','near_cylinder_right','near_axis_right'),
                ('near_spherical_left','near_cylinder_left','near_axis_left'),
            ),
        }),
        ('Otros', {
            'classes': (
                'collapse',
            ),
            "fields": (
                'intermediate_add','near_add','patient_notes','laboratory_notes','optic_notes'
            ),
        }),
        ('Lunas y monturas', {
            "fields": (
                'measure_price', 'crystals','crystals_price','frame','frame_price'
            ),
        }),
    )
    
    list_display_links = (
        'id',
        'patient',
    )
    # def codigo(self, obj):
    #     return f"{obj.first_name[0]}{obj.last_name[0]}{obj.job[0]}{obj.id}"

    search_fields = (
        'patient__dni',
        'patient__full_name',
    )
    # list_filter = ('job','habilidades')
    # filter_vertical = ('habilidades',)
