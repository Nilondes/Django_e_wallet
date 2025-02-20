from django.db import models
from django.core.validators import MinValueValidator
import uuid


class Wallet(models.Model):
    wallet_uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    amount = models.DecimalField(max_digits=7, decimal_places=2, validators=[MinValueValidator(0.00)], default=0.00)


class Transaction(models.Model):
    choices = (
        ("DEPOSIT", "DEPOSIT"),
        ("WITHDRAW", "WITHDRAW")
    )
    wallet_uuid = models.ForeignKey(Wallet, to_field="wallet_uuid", on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=7, decimal_places=2, validators=[MinValueValidator(0.01)])
    operationType = models.CharField(choices=choices)
