FROM python:3.8.6
COPY ./api-sensor .

RUN pip install -r requirements.txt

WORKDIR /api-sensor/api-sensor
COPY ./api-sensor .