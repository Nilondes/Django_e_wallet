from django.db import models

class Wallet(models.Model):
    wallet_uuid = models.IntegerField(unique=True)
    amount = models.DecimalField(max_digits=7, decimal_places=2)
