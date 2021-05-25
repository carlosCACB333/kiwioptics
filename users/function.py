from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template import loader

def create_mail(user_mail, subject, template_name, context):
    
    message = EmailMultiAlternatives(
        subject=subject,
        body='',
        from_email=settings.EMAIL_HOST_USER,
        to=[
            user_mail
        ],
        cc=[]
    )

    html_email = loader.render_to_string(template_name, context)
    message.attach_alternative(html_email, 'text/html')
    return message



