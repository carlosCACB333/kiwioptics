from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _

class CustomUserManager(BaseUserManager):
    """
    Custom user model manager donde el correo es el unico
    autenticador en vez del nombre de usuario
    """
    def create_user(self, email, password, **extra_fields):
        """
        Crea y guarda un usuario con el correo y contraseña dados.
        """
        if not email:
            raise ValueError