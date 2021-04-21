from rest_framework.authtoken.models import Token

from django.urls import reverse_lazy
from django.db.models.signals import post_save
from .models import Account, Configuration
from users.middleware import RequestMiddleware
from .function import create_mail,code_generator
from django.contrib import messages
from django.dispatch import receiver

@receiver(post_save, sender=Account)
def verify_email(sender, instance, created, **kwargs):
    if created:
        if len(instance.password)==0:
            instance.verify_email = True
            instance.save()
        else:
            if instance.user_type == 'OPTIC':
                codigo = code_generator()
                instance.verification_code = codigo
                instance.save()
                # enviamos el email

                request = RequestMiddleware(get_response=None)
                request = request.thread_local.current_request

                ruta = request.headers['Origin']+str(reverse_lazy(
                    'users:validateEmail', kwargs={'id': instance.id, 'codigo': codigo}))

                mail = create_mail(
                    instance.username,
                    'Validación de Identidad',
                    'users/email.html',
                    {
                        'username': instance.full_name,
                        'ruta': ruta
                    }
                )

                mail.send(fail_silently=False)
                messages.success(request, f'Se envió un código de verificación a su email. verifique su correo por favor')
        Configuration.objects.create(account=instance)