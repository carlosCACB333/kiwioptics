from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _

class CustomUserManager(BaseUserManager):
    """
    Custom user model manager donde el correo es el unico
    autenticador en vez del nombre de usuario
    """
    def create_user(self, email, password):
        """
        Crea y guarda un usuario con el correo y contraseña dados.
        """
        if not email:
            raise ValueError(_('The email must be set'))
        user = self.model(
            email = self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Crea y guarda un superusuario con el correo y contraseña dados.
        """
        user = self.create_user(
            email, password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user