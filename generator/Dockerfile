FROM python:latest

RUN pip3 install --upgrade pip
RUN pip3 install paho-mqtt

WORKDIR /tmp/app
COPY . /tmp/app
RUN chmod 777 /tmp/app/wait-for-it.sh

CMD ["pyton3", "generator.py"]
