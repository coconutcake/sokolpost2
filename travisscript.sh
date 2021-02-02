#!/usr/bin/env bash
printf "\n[..] Uruchamam traviscript...\n"
docker-compose run app sh -c "python3 manage.py migrate" \
&& printf "\n[..] Uruchamiam testy jednostkowe...\n" \
docker-compose run app sh -c "python3 manage.py test" \
&& printf "\n[OK] Testy wykonane\n" \
&& printf "\n[OK] Kontenery uruchomione\n" \
&& printf "\n[..] Wylaczam kontenery...\n" \
&& docker-compose down \
&& printf "\n[OK] Wylaczone! Brak błędów\n"