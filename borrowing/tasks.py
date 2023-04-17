import datetime
from celery import shared_task

from borrowing.models import Borrowing
from borrowing.telegram_alert import send_to_telegram


@shared_task
def borrowing_alert(email, title, expected_return):
    message = f'{email} just borrowed {title} until {expected_return}'
    send_to_telegram(message)


@shared_task
def check_overdue():
    borrowings = [
        {
            'user': borrowing.user.email,
            'book': borrowing.book.title,
            'overdue': (datetime.date.today() - borrowing.expected_return).days
        }
        for borrowing in Borrowing.objects.filter(
            actual_return__isnull=True,
            expected_return__lt=datetime.date.today()
        )
    ]
    for borrowing in borrowings:
        send_to_telegram(f"{borrowing['user']} overdue {borrowing['book']} for {borrowing['overdue']} days")
