from .models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail

from cmdbox.profiles.models import Profile

@receiver(post_save, sender=User)
def send_user_email(sender, instance, created, **kwargs):
    url        = User.get_absolute_url()
    first_name = User.first_name
    last_name  = User.last_name
    email      = User.email

    subject = "Venchmark Account Creation Notificatoin"
    message = ""
    message += "Hello, " + first_name + ", "
    message += "      An account has been created for you in the Venchmark system. You can log into Venchmark at the link below. Please remember to reset your password once you log in. {% url 'login' %}"
    from_email = "no_reply@venchmark.com"
    to_email = email
    send_mail(
        subject,
        message,
        from_email,
        recipient_list = [ to_email ]
    )
