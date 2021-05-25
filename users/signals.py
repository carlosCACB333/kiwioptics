from rest_framework.authtoken.models import Token

from django.urls import reverse_lazy
from django.db.models.signals import post_save
from .models import Account, Configuration
from users.middleware import RequestMiddleware
from .function import create_mail
from django.contrib import messages
from django.dispatch import receiver
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator


@receiver(post_save, sender=Account)
def verify_email(sender, instance, created, **kwargs):
    if created:
        if len(instance.password) == 0:
            instance.verify_email = True
            instance.save()
        else:
            if instance.user_type == 'OPTIC':
                # enviamos el email
                request = RequestMiddleware(get_response=None)
                request = request.thread_local.current_request

                sitio = request.headers['Origin']
                current_site = get_current_site(request)
                site_name = current_site.name
                domain = current_site.domain

                mail = create_mail(
                    instance.username,
                    'Validación de Identidad',
                    'users/email.html',
                    {
                        'domain': domain,
                        'site_name': site_name,
                        'uid': urlsafe_base64_encode(force_bytes(instance.pk)),
                        'user': instance,
                        'token': default_token_generator.make_token(instance),
                        'sitio': sitio,
                    }
                )

                mail.send(fail_silently=False)
                messages.success(
                    request, f'Se envió un Link de verificación a su email. Verifique su correo por favor')
        Configuration.objects.create(account=instance)
