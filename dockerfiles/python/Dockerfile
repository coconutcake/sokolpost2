FROM python:3.8-slim
LABEL maintainer = "Gobit"

ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y \
		gcc \
		curl \
		gettext \
        mariadb-client \
		default-mysql-client default-libmysqlclient-dev \
		libpq-dev \
		iputils-ping \
		sqlite3 \
		nano \
	--no-install-recommends apt-utils && rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt /requirements.txt
COPY ./initialize.sh /initialize.sh
COPY ./baza.sql /baza.sql
RUN chmod +x /initialize.sh

COPY wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh
COPY run.sh /run.sh
COPY run.py /run.py
RUN chmod +x /run.sh
RUN chmod +x /run.py

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt


RUN mkdir /app




WORKDIR /app
COPY ./app /app

RUN useradd -ms /bin/bash user
# RUN useradd -D user
RUN chown user -R /app/
# USER user


# EXPOSE 8000
# CMD [ "python", "manage.py migrate", "python", "manage.py runserver 0.0.0.0:8000" ]

# CMD ["/wait-for-it.sh", "db:3306", "--timeout=45", "--strict", "--", "./run.sh"]



