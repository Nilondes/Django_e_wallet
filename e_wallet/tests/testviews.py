from django.test import TestCase
from api.models import Wallet


class WalletViewTestCase(TestCase):
    def setUp(self):
        self.wallet = Wallet.objects.create(wallet_uuid=12345, amount=100.00)
        self.wallet.save()

    def test_get_wallet_amount(self):
        resp = self.client.get('http://127.0.0.1:8000/api/v1/wallets/12345')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data[0]['wallet_uuid'], 12345)
        self.assertEqual(resp.data[0]['amount'], '100.00')

    def test_unknown_wallet(self):
        resp = self.client.get('http://127.0.0.1:8000/api/v1/wallets/1234')
        self.assertEqual(resp.status_code, 404)
        self.assertEqual(resp.data['detail'], 'There is no wallet with uuid 1234')


class TransactionViewTestCase(TestCase):
    def setUp(self):
        self.wallet = Wallet.objects.create(wallet_uuid=12345, amount=100.00)

    def test_unknown_wallet(self):
        resp = self.client.post('http://127.0.0.1:8000/api/v1/wallets/1234/operation', {'operationType': 'DEPOSIT',
                                                                                        'amount': 50}
                                )
        self.assertEqual(resp.status_code, 404)
        self.assertEqual(resp.data['detail'], 'There is no wallet with uuid 1234')

    def test_post_valid_transaction(self):
        transaction_resp = self.client.post('http://127.0.0.1:8000/api/v1/wallets/12345/operation', {'operationType': 'DEPOSIT',
                                                                                        'amount': 50}
                                )
        wallet_resp = self.client.get('http://127.0.0.1:8000/api/v1/wallets/12345')
        self.assertEqual(transaction_resp.status_code, 201)
        self.assertEqual(wallet_resp.status_code, 200)
        self.assertEqual(wallet_resp.data[0]['wallet_uuid'], 12345)
        self.assertEqual(wallet_resp.data[0]['amount'], '150.00')

    def test_post_invalid_transaction(self):
        transaction_resp = self.client.post('http://127.0.0.1:8000/api/v1/wallets/12345/operation', {'operationType': 'WITHDRAW',
                                                                                        'amount': 200}
                                )
        wallet_resp = self.client.get('http://127.0.0.1:8000/api/v1/wallets/12345')
        self.assertEqual(transaction_resp.status_code, 400)
        self.assertEqual(transaction_resp.data[0], 'Insufficient funds in the wallet.')
        self.assertEqual(wallet_resp.status_code, 200)
        self.assertEqual(wallet_resp.data[0]['wallet_uuid'], 12345)
        self.assertEqual(wallet_resp.data[0]['amount'], '100.00')
