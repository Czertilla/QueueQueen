FROM python:3.13-slim

# TODO replace all "QueueQueen" by dir name

RUN mkdir /QueueQueen

WORKDIR /QueueQueen

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod a+x docker/*.sh
