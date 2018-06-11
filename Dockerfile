FROM python:3.4-slim-jessie

ADD . /app

ENV LAYER13_API YourApiKey
ENV TOKEN_BOT YourTokenBot

WORKDIR /app

RUN pip install -r requirements.txt


CMD python3 WarezBot.py -k $LAYER13_API -b $TOKEN_BOT
