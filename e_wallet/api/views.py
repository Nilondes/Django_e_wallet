from decimal import Decimal
from rest_framework import generics
from api.serializers import WalletSerializer, TransactionSerializer
from api.models import Wallet, Transaction
from rest_framework.exceptions import NotFound, ValidationError
from django.db import transaction
from django.core.cache import cache


class WalletView(generics.RetrieveAPIView):
    serializer_class = WalletSerializer
    lookup_field = 'wallet_uuid'

    def get_object(self):
        wallet_uuid = self.kwargs['wallet_uuid']
        cache_key = f'wallet_{wallet_uuid}'
        cached_wallet = cache.get(cache_key)
        if cached_wallet:
            return cached_wallet
        try:
            wallet = Wallet.objects.get(wallet_uuid=wallet_uuid)
        except Wallet.DoesNotExist:
            raise NotFound(detail=f"There is no wallet with uuid {wallet_uuid}")
        cache.set(cache_key, wallet, timeout=60)
        return wallet


class TransactionView(generics.CreateAPIView):
    serializer_class = TransactionSerializer
    queryset = Wallet.objects.select_for_update()
    lookup_field = 'wallet_uuid'

    def perform_create(self, serializer):
        wallet_uuid = self.kwargs['wallet_uuid']
        operation_type = serializer.validated_data["operationType"]
        amount = serializer.validated_data["amount"]
        with transaction.atomic():
            wallet = self.get_object()
            if operation_type == "DEPOSIT":
                wallet.amount += amount
            else:
                if wallet.amount < amount:
                    raise ValidationError(detail="Insufficient funds in the wallet.")
                wallet.amount -= amount
            wallet.save()
            serializer.save(wallet_uuid=wallet)
            cache_key = f'wallet_{wallet_uuid}'
            cache.set(cache_key, wallet, timeout=60)
