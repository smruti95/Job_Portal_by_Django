
from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_job_email(user_email, job_title):
    send_mail(
        f"Application for {job_title}",
        f"Thank you for applying to {job_title}!",
        "nmpatra35@gmail.com",
        [user_email],
    )
    return f"Email sent to {user_email}"
