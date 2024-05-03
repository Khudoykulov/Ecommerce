from django.contrib.auth import get_user_model
from config.celery import app
from django.core.mail import send_mail
from django.conf import settings
import os
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_bytes
from django.utils.http import urlsafe_base64_encode

from apps.account.models import User


# @app.task()
# def send_mail_reset_passwd(email):
#     users = get_user_model().objects.all()
#     subject = 'Hi! Celery'
#     user = User.objects.get(email=email)
#     uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
#     token = PasswordResetTokenGenerator().make_token(user)
#     current_site = os.getenv('SITE_NAME')
#     protocol = os.getenv('PROTOCOL')
#     abs_url = f'{protocol}://{current_site}/account/api/check_password/{uidb64}/{token}'
#     message = f'Reset Password link:\n{abs_url}'
#     send_mail(subject=subject,
#               message=message,
#               from_email=settings.EMAIL_HOST_USER,
#               recipient_list=[user.email],
#               fail_silently=True
#               )
#
#     return "Sent"


@app.task(bind=True)
def ecommerce_send_email(self, subject, message, recipient_list, *args, **kwargs):
    from_email = os.getenv('EMAIL_HOST_USER')
    send_mail(subject, message, from_email, recipient_list)
