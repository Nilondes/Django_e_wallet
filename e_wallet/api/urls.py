from django.urls import path
from api.views import WalletView, TransactionView

urlpatterns = [
    path('v1/wallets/<int:wallet_uuid>/', WalletView.as_view()),
    path('v1/wallets/<int:wallet_uuid>/operation/', TransactionView.as_view()),
]