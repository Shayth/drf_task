from django.db import models
from django.utils import timezone


class Wallet(models.Model):
    unique_key = models.CharField(max_length=100, unique=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    objects = models.Manager()


class Transaction(models.Model):
    objects = models.Manager()
    TRANSACTION_TYPES = (
        ('deposit', 'Депозит'),
        ('transfer', 'Перевод'),
    )

    sender = models.CharField(max_length=100, blank=True, null=True)
    recipient = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.transaction_type} from {self.sender} to {self.recipient}"
