# pull official base image
FROM python:3.8-slim-buster

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update && apt-get install -y netcat git

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

# copy project
COPY . /usr/src/app/

# install Let's encrypt root certificate
RUN cat letsencrypt-root.pem >> /usr/local/lib/python3.8/site-packages/certifi/cacert.pem

# run entrypoint.sh
# ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
