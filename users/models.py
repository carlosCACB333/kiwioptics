from django.db import models
from django.contrib.auth.models import User, AbstractUser
from .managers import CustomUserManager

class Account(AbstractUser):
    class Types(models.TextChoices):
        Optic = 'OPTIC','Optic'
        Employee = 'EMPLOYEE','Employee'

    first_name = None
    last_name = None
    email = None
    full_name = models.CharField("Nombre completo", max_length=100)
    user_type = models.CharField(choices=Types.choices, max_length=10, blank=False, null=False)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = "Cuenta"
        verbose_name_plural = "Cuentas"

    def __str__(self):
        return self.username

class OpticUser(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE, null=False)
    optic_name = models.CharField("Nombre de la optica", max_length=50, null=False)

    class Meta:
        verbose_name = "OpticUser"
        verbose_name_plural = "OpticUsers"

    def __str__(self):
        return str(self.account)


class EmployeeUser(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE)
    optic = models.ForeignKey(OpticUser, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "EmployeeUser"
        verbose_name_plural = "EmployeeUsers"

    def __str__(self):
        return str(self.account)



