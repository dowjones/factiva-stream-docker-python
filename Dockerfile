FROM python:3.10.2-slim-bullseye

# This env variable is useful when using Google services within the
# message handler function (like writing to BigQuery)
# ENV GOOGLE_APPLICATION_CREDENTIALS /app/service_account.json

ADD app /app/
# Creates the log folder instance that can be mapped with a mountpoint
# when running docker run or docker-compose
RUN mkdir /log
# Creates the folder to store files by the JSONL Handler. It that can
# be mapped with a mountpoint when running docker run or docker-compose
RUN mkdir /articles

RUN ["pip", "install", "factiva-news"]

WORKDIR /app
# Creates the credentials file instance that can be mapped with a mountpoint
# when running docker run or docker-compose
RUN ["touch", "service_account.json"]
CMD ["python", "main.py"]
