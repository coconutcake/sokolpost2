FROM python:3.8-slim
LABEL maintainer = "Gobit"

ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y \
		gcc \
		gettext \
		nano \ 
        cups \
        cups-client \
        lpr \
        apt-utils && rm -rf /var/lib/apt/lists/*

RUN python -m pip install --upgrade pip

RUN mkdir /app
WORKDIR /app

RUN useradd -ms /bin/bash user
RUN adduser user lpadmin
USER user
