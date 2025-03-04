from celery import Celery
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

load_dotenv()

# Create a Celery instance
celery = Celery('fastapi_job_tracker', broker='redis://localhost:6379/0')

celery.conf.update(
    task_pool='solo',
)

@celery.task
def send_verification_email(email: str, token: str):
    verification_link = f"http://localhost:8000/verify-email?token={token}"
    msg = MIMEText(f"Click the following link to verify your email: {verification_link}")
    msg['Subject'] = 'Email Verification'
    msg['From'] = os.getenv('EMAIL_USER')
    msg['To'] = email

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(os.getenv('EMAIL_USER'), os.getenv('EMAIL_PASSWORD'))
            server.sendmail(msg['From'], [msg['To']], msg.as_string())
        print(f"Verification email sent to {email}")
    except Exception as e:
        print(f"Failed to send email: {e}")
