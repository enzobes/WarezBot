FROM python:3.4-slim-jessie

ADD . /app

ENV LAYER13_API YourApiKey

RUN pip install discord.py requests datetime

WORKDIR /app

CMD ["python3", "WarezBot.py", "-k", "$LAYER13_API"]
