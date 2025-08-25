from django.core.mail import send_mail
from django.conf import settings

def send_welcome_email(to_email, username):
    subject = "Welcome to Job Portal"
    message = f"Hi {username},\n\nThank you for registering with us!"
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [to_email]

    send_mail(subject, message, from_email, recipient_list, fail_silently=False)
