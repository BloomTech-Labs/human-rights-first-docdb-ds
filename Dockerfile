FROM ubuntu

# Linux Updates
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update
RUN apt-get upgrade -y

# Sysytem Depencencies
ENV PYTHONUNBUFFERED=1
RUN apt-get -yqq install python3-pip python3-dev
RUN python3 -m pip install --upgrade pip

# Application Dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app app

# Network Settings
EXPOSE 8000
CMD uvicorn app.api:API --host 0.0.0.0 --port 8000

# Local Dependencies
#COPY .env .env
