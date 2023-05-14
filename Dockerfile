FROM python:3.10.5-slim-bullseye

#set EnvironmentVarialble
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

#set work directory
WORKDIR /code

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .
