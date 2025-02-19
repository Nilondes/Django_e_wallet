from decimal import Decimal
from rest_framework import generics
from api.serializers import WalletSerializer, TransactionSerializer
from api.models import Wallet, Transaction
from rest_framework.exceptions import NotFound, ValidationError
from django.db import transaction
from django.core.cache import cache


class WalletView(generics.ListAPIView):
    serializer_class = WalletSerializer
    queryset = Wallet.objects.all()

    def filter_queryset(self, queryset):
        wallet_uuid = self.request.parser_context['kwargs']['wallet_uuid']
        try:
            wallet = Wallet.objects.get(wallet_uuid=wallet_uuid)
        except Wallet.DoesNotExist:
            raise NotFound(detail=f"There is no wallet with uuid {wallet_uuid}")
        return queryset.filter(wallet_uuid=wallet_uuid)


class TransactionView(generics.ListCreateAPIView):
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()

    def filter_queryset(self, queryset):
        wallet_uuid = self.request.parser_context['kwargs']['wallet_uuid']
        try:
            wallet = Wallet.objects.get(wallet_uuid=wallet_uuid)
        except Wallet.DoesNotExist:
            raise NotFound(detail=f"There is no wallet with uuid {wallet_uuid}")
        return queryset.filter(wallet_uuid=wallet_uuid)

    def perform_create(self, serializer):
        wallet_uuid = self.request.parser_context['kwargs']['wallet_uuid']
        operationType = self.request.data.get('operationType')
        amount = Decimal(self.request.data.get('amount'))
        # cache_key = f'wallet_{wallet_uuid}'
        # cached_wallet = cache.get(cache_key)
        # if cached_wallet:
        #     wallet = cached_wallet

        try:
            wallet = Wallet.objects.get(wallet_uuid=wallet_uuid)
        except Wallet.DoesNotExist:
            raise NotFound(detail=f"There is no wallet with uuid {wallet_uuid}")
        # cache.set(cache_key, wallet, timeout=60)

        if operationType == "DEPOSIT":
            wallet.amount += amount
        else:
            if wallet.amount < amount:
                raise ValidationError(detail="Insufficient funds in the wallet.")
            wallet.amount -= amount
        wallet.save()
        # cache.set(cache_key, wallet, timeout=60)
        return serializer.save(wallet_uuid=wallet)
