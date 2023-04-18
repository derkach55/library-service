from django.db import models

from borrowing.models import Borrowing


class Payment(models.Model):
    STATUS_CHOICES = [('PAID', 'Payment Paid'), ('PENDING', 'Payment Pending')]
    TYPE_CHOICES = [('PAYMENT', 'Payment type'), ('FINE', 'Fine type')]
    status = models.CharField(choices=STATUS_CHOICES, max_length=7)
    type = models.CharField(choices=TYPE_CHOICES, max_length=7)
    borrowing = models.ForeignKey(Borrowing, on_delete=models.DO_NOTHING)
    session_url = models.CharField(max_length=255)
    session_id = models.CharField(max_length=255)
    money_to_pay = models.DecimalField(max_digits=19, decimal_places=10)
