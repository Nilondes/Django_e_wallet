# Django_e_wallet

This is a simple django rest app which imitates interaction with a web wallet.


The API receives requests in format: 

- POST api/v1/wallets/<WALLET_UUID>/operation

  {
  operationType: DEPOSIT or WITHDRAW,
  amount: 1000
  }

  which changes the wallet amount in database.

- GET api/v1/wallets/{WALLET_UUID}
  which responds with the current wallet amount.


## Getting started
To start Docker from main directory:

```sh
$ docker compose up --build
```
