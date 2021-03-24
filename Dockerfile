FROM python:3.7-slim-jessie

ADD . /app

ENV TOKEN_BOT YourTokenBot

WORKDIR /app

RUN pip install -r requirements.txt


CMD python3 WarezBot.py -b $TOKEN_BOT
