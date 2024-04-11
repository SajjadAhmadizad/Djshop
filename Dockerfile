FROM python:3.11.9-alpine

COPY . /app
WORKDIR /app

RUN pip install --upgrade pip
RUN pip install -r req.txt