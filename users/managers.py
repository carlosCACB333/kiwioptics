from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.db import models

class CustomUserManager(BaseUserManager):
    """
    Custom user model manager donde el correo es el unico
    autenticador en vez del nombre de usuario
    """
    def create_user(self, username, password):
        """
        Crea y guarda un usuario con el correo y contraseña dados.
        """
        if not username:
            raise ValueError(_('The username must be set'))
        user = self.model(
            username = username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        """
        Crea y guarda un superusuario con el correo y contraseña dados.
        """
        user = self.create_user(
            username=username, password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user


class EmployeeUserManager(models.Manager):

    def get_employee_for_account(self,user):
        return self.filter(account=user)