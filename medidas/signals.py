from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import OpticUser
from medidas.models import Crystal, CrystalTreatments, CrystalMaterial

TREATMENTS = (
    {
    "name":"Antirayas",
    "description":"El tratamiento anti-rayas garantiza la durabilidad y adherencia de las capas de anti-reflejo así como la resistencia a ralladuras",
    },
    {
    "name":"Antireflex",
    "description":"reduce considerablemente el brillo que afecta tus ojos y reduce la fatiga ocular.",
    },
    {
    "name":"Blue Defense",
    "description":"""Protege de la luz emitida por los dispositivos digitales, protege contra los rayos UV hasta 400 nm, el nuevo estándar en salud visual.
     Incluye una protección completa contra los rayos UV mas nocivos de 380 nm hasta 400 nm.""",
    },
    {
    "name":"Protección UV",
    "description":"""Las gafas de sol con protección UV son un bloqueador solar para sus ojos.
    La exposición acumulativa a la dañina radiación ultravioleta (UV) a lo largo de la vida de una persona ha sido asociada con problemas relacionados con la edad, como las cataratas y la degeneración macular.""",
    },
    {
    "name":"FotoCromatico",
    "description":"""Las lunas fotocromáticas tienen la capacidad de cambiar de color al entrar
en contacto con los rayos UV. Absorben el 100% de los rayos UVA y UVB
en todo tipo de condiciones y son ideales para situaciones tanto en interior
como exterior.""",
    },
    {
    "name":"Polarizados",
    "description":"""Permite minimizar los efectos de los rayos de luz,
     son ideales para uso sobre pavimento, arena, agua y nieve.
     Elimina el deslumbramiento.""",
    },
    {
    "name":"Hidrofóbicos",
    "description":"""Tratamiento Antireflex Superior resistente al polvo, agua y grasa haciendo que la luna
    no se ensucie ni raye con facilidad y que también sea más facil de limpiar.""",
    },
    {
    "name":"Superclean",
    "description":"""Es un tratamiento antireflejo superior, además de disminuir el brillo y
    brindar mayor comodidad. Repele el polvo, agua y grasa; haciendo que la
    luna sea muy fácil de limpiar.""",
    },
    {
    "name":"Transitions",
    "description":"""Lunas que están también en la familia de los fotocromáticas, pero que
    tienen una tecnología superior en cuanto a la velocidad de opacidad de
    las lunas al estar en contacto con los rayos UV.""",
    },
)

MATERIALS = (
    {
        "name":"Vidrio crown",
        "retracting_index":"1.523",
        "abbe":"59",
        "description":"""Excelente óptica.
        Bajo costo.
        Desventajas: pesado, quebradizo.""",
    },
    {
        "name":"Resina CR-39",
        "retracting_index":"1.498",
        "abbe":"58",
        "description":"""Excelente óptica.
        Bajo costo.
        Desventaja: grosor.""",
    },
    {
        "name":"Trivex",
        "retracting_index":"1.54",
        "abbe":"45",
        "description":"""Resistencia superior a impactos.
        El material más liviano que se ofrece.""",
    },
    {
        "name":"NK-55",
        "retracting_index":"1.56",
        "abbe":"38",
        "description":"""Son resistentes a los impactos, más delgados y altamente reflectantes..""",
    },
    {
        "name":"Policarbonato",
        "retracting_index":"1.586",
        "abbe":"30",
        "description":"""Resistencia superior a impactos.
        Más liviano que los cristales de plástico de alto índice.""",
    },
    {
        "name":"Tríbido",
        "retracting_index":"1.60",
        "abbe":"41",
        "description":"""Delgado y liviano.
        Considerablemente más resistente a impactos que los cristales de plástico CR-39 y de alto índice (excepto el policarbonato y Trivex).
        Desventaja: Todavía no está disponible en una amplia variedad de diseños de cristales.""",
    },
    {
        "name":"Alto indice 1.60",
        "retracting_index":"1.60",
        "abbe":"36",
        "description":"""Delgado y liviano.
        Menos costoso que los lentes de 1.70-1.74 de índice alto.""",
    },
    {
        "name":"Alto indice 1.67",
        "retracting_index":"1.67",
        "abbe":"32",
        "description":"""Delgado y liviano.
        Menos costoso que los lentes de 1.70-1.74 de índice alto.""",
    },
    {
        "name":"Alto indice 1.70",
        "retracting_index":"1.70",
        "abbe":"36",
        "description":"""Los cristales más delgados que se ofrecen.""",
    },
    {
        "name":"Alto indice 1.74",
        "retracting_index":"1.74",
        "abbe":"33",
        "description":"""Los cristales más delgados que se ofrecen.""",
    },
)

CRYSTALS = (
    {
        "name":"Cristal",
        "material":"Vidrio crown",
        "treatments": (),
    },
    {
        "name":"Básicas: Resinas CR-39",
        "material":"Resina CR-39",
        "treatments": (),
    },
    {
        "name":"Plus: Resinas Antireflex",
        "material":"Resina CR-39",
        "treatments": ("Antireflex",),
    },
    {
        "name":"Plus UV: NK-55 Antireflex",
        "material":"NK-55",
        "treatments": ("Antireflex","Antirayas","Protección UV"),
    },
    {
        "name":"Premium: Policarbonato UV",
        "material":"Policarbonato",
        "treatments": ("Antirayas","Protección UV"),
    },
    {
        "name":"Pro: Policarbonato Antireflex UV",
        "material":"Policarbonato",
        "treatments": ("Antireflex","Antirayas","Protección UV"),
    },
    {
        "name":"Blue Defense: NK-55 Antireflex UV",
        "material":"NK-55",
        "treatments": ("Antireflex","Antirayas","Protección UV","Blue Defense"),
    },
    {
        "name":"Chrom: Resina Fotocromática Antireflex UV",
        "material":"Resina CR-39",
        "treatments": ("Antireflex","Antirayas","Protección UV","FotoCromatico"),
    },
    {
        "name":"Chrom Blue Defense: NK-55 Fotocromática Antireflex UV",
        "material":"NK-55",
        "treatments": ("Antireflex","Antirayas","Protección UV","Blue Defense","FotoCromatico"),
    },
    {
        "name":"Delgado: Alto indice 1.60",
        "material":"Alto indice 1.60",
        "treatments": ("Antirayas","Protección UV"),
    },
    {
        "name":"Delgado: Alto indice 1.67",
        "material":"Alto indice 1.67",
        "treatments": ("Antirayas","Protección UV"),
    },
    {
        "name":"Delgado: Alto indice 1.70",
        "material":"Alto indice 1.70",
        "treatments": ("Antirayas","Protección UV"),
    },
    {
        "name":"Delgado: Alto indice 1.74",
        "material":"Alto indice 1.74",
        "treatments": ("Antirayas","Protección UV"),
    },
)

@receiver(post_save, sender=OpticUser)
def add_crystals(sender, instance, created,**kwargs):
    if created:
        for treatment in TREATMENTS:
            instance.crystaltreatments_set.create(treatment_name=treatment["name"], description=treatment["description"])
        for material in MATERIALS:
            instance.crystalmaterial_set.create(
                material_name=material["name"], 
                retracting_index=material["retracting_index"],
                abbe=material["abbe"],
                description=material["description"],
            )
        for crystal in CRYSTALS:
            crystal_material = instance.crystalmaterial_set.get(material_name=crystal["material"])
            new_crystal = instance.crystal_set.create(crystal_name=crystal["name"],material=crystal_material)
            for treatment in crystal["treatments"]:
                crystal_treatment = instance.crystaltreatments_set.get(treatment_name=treatment)
                new_crystal.treatments.add(crystal_treatment)
        # print(instance.crystaltreatments_set.filter(name="Antirayas"))
        # print(instance.crystaltreatments_set.filter(name="Antireflex"))
        # print(instance.crystaltreatments_set.filter(name="Hidrofóbicos"))
        # print(instance.crystaltreatments_set.filter(name="Blue Defense"))
        # print(instance.crystaltreatments_set.filter(name="Superclean"))
        # print(instance.crystaltreatments_set.filter(name="FotoCromatico"))
        # print(instance.crystaltreatments_set.filter(name="Transitions"))
        # print(instance.crystaltreatments_set.filter(name="Polarizados"))
        # print(instance.crystaltreatments_set.filter(name="Protección UV"))
            
