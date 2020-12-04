FROM python:3.8.6
COPY ./api-generator .

RUN pip install -r requirements.txt