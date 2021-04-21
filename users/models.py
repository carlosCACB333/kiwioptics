from django.db import models
from django.contrib.auth.models import User, AbstractUser, PermissionsMixin, AbstractBaseUser
from .managers import CustomUserManager, EmployeeUserManager


class Account(AbstractUser, PermissionsMixin):
    class Types(models.TextChoices):
        Optic = 'OPTIC', 'Optic'
        Employee = 'EMPLOYEE', 'Employee'

    first_name = None
    last_name = None
    email = None
    is_superuser = models.BooleanField(
        ('super usuario'),
        default=False,
        help_text=(
            'Tiene todo los permisos sin asignárselo '
        ),
    )
    full_name = models.CharField("Nombre completo", max_length=100)
    picture = models.ImageField(
        "perfil", upload_to="account", blank=True, null=True, max_length=255)
    user_type = models.CharField(
        choices=Types.choices, max_length=10, blank=False, null=False)
    verification_code = models.CharField('codigo de verificacion', max_length=8,blank=True,null=True)
    verify_email = models.BooleanField('email verificado',default=False)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = "Cuenta"
        verbose_name_plural = "Cuentas"

    def __str__(self):
        return self.username

    def get_optictype(self):
        opticuser = None
        if self.user_type == str(Account.Types.Optic):
            opticuser = self.opticuser
        elif self.user_type == str(Account.Types.Employee):
            opticuser = self.employeeuser
        return opticuser

    def get_opticuser(self):
        opticuser = None
        if self.user_type == str(Account.Types.Optic):
            opticuser = self.opticuser
        elif self.user_type == str(Account.Types.Employee):
            opticuser = self.employeeuser.optic
        return opticuser


class OpticUser(models.Model):
    account = models.OneToOneField(
        Account, on_delete=models.CASCADE, null=False)
    prescription_name = models.CharField(
        "Nombre en la prescripcion", max_length=100)
    optic_name = models.CharField(
        "Nombre de la optica", max_length=30, null=False)
    phone = models.CharField("Numero de contacto", max_length=30, blank=True)
    # logo = models.ImageField("Logo", upload_to=None, height_field=None, width_field=None, max_length=None)

    class Meta:
        verbose_name = "OpticUser"
        verbose_name_plural = "OpticUsers"

    def __str__(self):
        return str(self.optic_name)


class EmployeeUser(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE)
    optic = models.ForeignKey(OpticUser, on_delete=models.CASCADE)
    email = models.EmailField("Correo electronico", blank=True)
    prescription_name = models.CharField(
        "Nombre en la prescripcion", max_length=100)
    phone = models.CharField("Celular", max_length=30, blank=True)
    other_phone = models.CharField("Celular", max_length=30, blank=True)
    # photo = models.ImageField("Foto", upload_to=None, height_field=None, width_field=None, max_length=None)

    objects = EmployeeUserManager()

    class Meta:
        verbose_name = "EmployeeUser"
        verbose_name_plural = "EmployeeUsers"

    def __str__(self):
        return str(self.account)

class Configuration(models.Model):

    account = models.OneToOneField(Account, on_delete=models.CASCADE)
    is_dip = models.BooleanField('Dip o Dnp', default=True)

    class Meta:
        verbose_name = "Configuración"
        verbose_name_plural = "Configuraciones"

    def __str__(self):
        return str(self.is_dip)
