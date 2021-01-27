#!/usr/bin/env bash
printf "\nUruchamam traviscript\n"
docker-compose run app sh -c "python manage.py migrate" \
&& printf "\nUruchamiam testy jednostkowe\n" \
&& printf "\nWylaczam uslugi\n" \
&& docker-compose down \
&& printf "\nWylaczone!\n"