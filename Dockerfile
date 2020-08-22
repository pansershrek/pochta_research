FROM python:3
ENV PYTHONUNBUFFERED 1

WORKDIR main


COPY . .
RUN pip install -r ./requirements.txt