#!/bin/bash
cd e_wallet
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py test
python3 manage.py loaddata wallet_fixture.json
python3 manage.py runserver 0.0.0.0:8000