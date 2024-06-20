FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    libjpeg-dev \
    zlib1g-dev \
    libfreetype6-dev \
    libblas-dev \
    liblapack-dev \
    gfortran \
    libgl1-mesa-glx \
    libglib2.0-0 \
    curl \
    && apt-get clean

WORKDIR /app

RUN pip install --upgrade pip
RUN pip install gunicorn
ADD ../../requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

COPY . .

RUN chmod +x /app/docker/backend/server-entrypoint.sh
RUN chmod +x /app/docker/backend/worker-entrypoint.sh