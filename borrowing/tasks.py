import datetime
from celery import shared_task

from borrowing.models import Borrowing
from borrowing.telegram_alert import send_to_telegram


@shared_task
def borrowing_alert(email, title, expected_return):
    message = f'{email} just borrowed {title} until {expected_return}'
    send_to_telegram(message)



