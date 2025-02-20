from locust import HttpUser, task, between


class WalletUser(HttpUser):
    wait_time = between(1, 2)


    @task
    def get_wallet_amount(self):
        self.client.get('http://127.0.0.1:8000/api/v1/wallets/00000000-0000-0000-0000-000000003039')

    @task
    def deposit_to_wallet(self):
        payload = {
            "operationType": "DEPOSIT",
            "amount": 1.0
        }
        self.client.post('http://127.0.0.1:8000/api/v1/wallets/00000000-0000-0000-0000-000000003039/operation', json=payload)

    @task
    def withdraw_from_wallet(self):
        payload = {
            "operationType": "WITHDRAW",
            "amount": 1.0
        }
        self.client.post('http://127.0.0.1:8000/api/v1/wallets/00000000-0000-0000-0000-000000003039/operation', json=payload)
