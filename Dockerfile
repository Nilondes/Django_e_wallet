FROM python:3.12-slim

WORKDIR e_wallet/

COPY requirements.txt /e_wallet/

RUN pip install -r requirements.txt

COPY . /e_wallet/

RUN ["chmod", "+x", "./docker-entrypoint.sh"]
ENTRYPOINT ["bash", "-c"]
CMD ["./docker-entrypoint.sh"]