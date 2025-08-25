from celery import shared_task
import time

@shared_task
def send_welcome_email(user_id):
    print(f"Sending welcome email to user {user_id}...")
    time.sleep(5)
    print("Email sent ✅")
    return f"Email sent to user {user_id}"
