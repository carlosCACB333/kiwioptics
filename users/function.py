import random
import string
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from myOptica import settings


def create_mail(user_mail, subject, template_name, context):
    template = get_template(template_name)
    content = template.render(context)

    message = EmailMultiAlternatives(
        subject=subject,
        body='',
        from_email=settings.EMAIL_HOST_USER,
        to=[
            user_mail
        ],
        cc=[]
    )

    message.attach_alternative(content, 'text/html')
    return message


def code_generator(size=8, chars=string.ascii_uppercase+string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
