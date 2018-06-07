#Download base image unbuntu 16.04
FROM ubuntu:16.04
RUN apt-get update && \
      apt-get -y install sudo
ADD WarezBot.py /
USER root
ENV LAYER13_API YourApiKey
RUN apt-get update \
  && apt-get -y install python3-pip python3-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip
RUN apt-get -y install git
RUN git clone https://github.com/enzobes/WarezBot.git
RUN python3 -m pip install -U discord.py
RUN python3 -m pip install requests
RUN python3 -m pip install datetime
CMD python3 WarezBot/WarezBot.py -k $LAYER13_API > bot.log