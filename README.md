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
$ docker build . -t dev
$ docker run -it -p 5000:5000 dev bash
$ cd e_wallet
```

### Main app

```sh
$ python3 api.py
```


### Script for imitating test POST requests

```sh
$ python3 test_request.py
```
