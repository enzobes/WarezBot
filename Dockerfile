FROM python:3.4-slim-jessie

ADD . /app

ENV LAYER13_API YourApiKey
ENV TOKEN_BOT YourTokenBot

RUN pip install -r requirements.txt

WORKDIR /app

CMD python3 WarezBot.py -k $LAYER13_API -b $TOKEN_BOT