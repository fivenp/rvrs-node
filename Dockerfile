FROM python:3

ENV API_URL https://rvrs-api.fivenp.workers.dev
ENV MQTT_URL rvrs-dev.cloud.shiftr.io
ENV MQTT_USER rvrs-dev
ENV MQTT_PWD Ldbfq2kDqR1CiAk4
ENV VERSION=0.0.1

WORKDIR /usr/src/app

RUN apt-get update
RUN apt-get -y install mtr cron
RUN pip install requests paho-mqtt

COPY crontab /etc/cron.d/crontab
RUN chmod 0644 /etc/cron.d/crontab
RUN crontab /etc/cron.d/crontab
RUN touch /var/log/cron.log

COPY . .

CMD [ "python", "./main.py" ]
