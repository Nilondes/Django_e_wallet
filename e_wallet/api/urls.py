from django.urls import path
from api.views import WalletView, TransactionView

urlpatterns = [
    path('v1/wallets/<uuid:wallet_uuid>', WalletView.as_view(), name='wallet-detail'),
    path('v1/wallets/<uuid:wallet_uuid>/operation', TransactionView.as_view(), name='wallet-operation'),
]