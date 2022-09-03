from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect

def send_user_email(subject, message, from_email, to_email, request):
    message += request.get_full_path()
    send_mail(
        subject,
        message,
        from_email,
        recipient_list = [ to_email ]
        )
