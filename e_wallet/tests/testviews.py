from django.test import TestCase
from api.models import Wallet
from django.core.cache import cache
import uuid


class WalletViewTestCase(TestCase):
    def setUp(self):
        cache.clear()
        self.wallet = Wallet.objects.create(amount=100.00)
        self.wallet.save()
        self.uuid = self.wallet.wallet_uuid

    def test_get_wallet_amount(self):
        resp = self.client.get(f'http://127.0.0.1:8000/api/v1/wallets/{self.uuid}')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data['wallet_uuid'], str(self.uuid))
        self.assertEqual(resp.data['amount'], '100.00')

    def test_unknown_wallet(self):
        unknown_uuid = uuid.uuid4()
        resp = self.client.get(f'http://127.0.0.1:8000/api/v1/wallets/{unknown_uuid}')
        self.assertEqual(resp.status_code, 404)
        self.assertEqual(resp.data['detail'], f'There is no wallet with uuid {unknown_uuid}')


class TransactionViewTestCase(TestCase):
    def setUp(self):
        cache.clear()
        self.wallet = Wallet.objects.create(amount=100.00)
        self.wallet.save()
        self.uuid = self.wallet.wallet_uuid

    def test_unknown_wallet(self):
        unknown_uuid = uuid.uuid4()
        resp = self.client.post(f'http://127.0.0.1:8000/api/v1/wallets/{unknown_uuid}/operation', {'operationType': 'DEPOSIT',
                                                                                        'amount': 50}
                                )
        self.assertEqual(resp.status_code, 404)
        self.assertEqual(resp.data['detail'], 'No Wallet matches the given query.')

    def test_post_valid_transaction(self):
        transaction_resp = self.client.post(f'http://127.0.0.1:8000/api/v1/wallets/{self.uuid}/operation', {'operationType': 'DEPOSIT',
                                                                                        'amount': 50}
                                )
        wallet_resp = self.client.get(f'http://127.0.0.1:8000/api/v1/wallets/{self.uuid}')
        self.assertEqual(transaction_resp.status_code, 201)
        self.assertEqual(wallet_resp.status_code, 200)
        self.assertEqual(wallet_resp.data['wallet_uuid'], str(self.uuid))
        self.assertEqual(wallet_resp.data['amount'], '150.00')

    def test_post_invalid_transaction(self):
        transaction_resp = self.client.post(f'http://127.0.0.1:8000/api/v1/wallets/{self.uuid}/operation', {'operationType': 'WITHDRAW',
                                                                                        'amount': 200}
                                )
        wallet_resp = self.client.get(f'http://127.0.0.1:8000/api/v1/wallets/{self.uuid}')
        self.assertEqual(transaction_resp.status_code, 400)
        self.assertEqual(transaction_resp.data[0], 'Insufficient funds in the wallet.')
        self.assertEqual(wallet_resp.status_code, 200)
        self.assertEqual(wallet_resp.data['wallet_uuid'], str(self.uuid))
        self.assertEqual(wallet_resp.data['amount'], '100.00')
