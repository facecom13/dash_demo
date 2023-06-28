FROM python:3.8
# RUN apt-get update && apt-get -y
WORKDIR /appcron
COPY crontab /etc/cron.d/crontab
COPY credit_update.py /appcron/credit_update.py
COPY requirements.txt /
RUN pip3 install -r /requirements.txt
RUN chmod 0644 /etc/cron.d/crontab
RUN /etc/cron.d/crontab
# run crond as main process of container
CMD ["cron", "-f"]