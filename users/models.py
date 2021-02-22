from django.db import models
from django.contrib.auth.models import User, AbstractUser
from .managers import CustomUserManager

# Create your models here.
# class Optica(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     optica = models.CharField(("Optica"), max_length=50)
#     phone = models.CharField("Celular",max_length=30)


#     class Meta:
#         verbose_name = "Optica"
#         verbose_name_plural = "Opticas"

#     def __str__(self):
#         return f'{self.optica}'

class OpticUser(AbstractUser):
    username = None
    email = models.EmailField('Correo electronico', unique=True)
    optic = models.CharField('Optica', max_length=50)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = "Usuario Optica"
        verbose_name_plural = "Usuarios Optica"

    def __str__(self):
        return self.email

