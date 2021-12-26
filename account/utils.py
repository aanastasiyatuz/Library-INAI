from django.core.mail import send_mail
from decouple import config

DOMAIN = config("DOMAIN")

def send_activation_email(email, activation_code):
    activation_url = f'{DOMAIN}/account/activate/{activation_code}'
    message = f"To activate your account click here {activation_url}"
    send_mail('INAI Library Activation account', message, 'admin@admin.com', [email, ], fail_silently=False)
