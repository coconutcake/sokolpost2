# Sokol2 

## :rocket: Uruchamianie
Aby uruchomić alikacje procesor hosta musi wspierac wirtualizacje. Pobierz [Docker](https://www.docker.com/products/docker-desktop)

Po sklonowaniu repozytorium, przejdz do folderu aplikacji i uruchom kontenery poleceniem:

    docker-compose up --build

Nastepnie uruchom populacje domyślną dla bazy danych aplikacji zapisanej w pliku initialize.sh:
    
    docker exec -it app sh -c '../initialize.sh'

Przejdz do aplikacji przez przeglądarkę i zaakceptuj certyfikat a nastepnie zaloguj przy użyciu poświadczeń admina:

    Login: contact@mign.pl
    Hasło: asdasd123

## :file_folder: Struktura katalogów
:file_folder: Aplikacja - **/app/HD_app**<br />
:file_folder: Certyfikaty ssl - **/certs**<br />
:file_folder: Dockerfiles - **/dockerfiles**<br />
:file_folder: Konfiguracja serwera nginx -  **/nginx_config**<br />
:file_folder: Logi serwera nginx - **/nginx_logs**<br />
:file_folder: Pliki importu modeli bazy - **/app/export**<br />

## :memo: Opis

Sokół robiony jest na Django/Python w środowisku wirtualnym Docker na którym odpalane są po kolei 3 nastepujace kontenery:
- kontener bazy danych mysql 5.7
- kontener aplikacyjny app
- kontener serwera upstream nginx

![Schemat](http://mign.pl/temp/docker.png)

Ponieważ Django posiada tylko serwer developerski, Na kontenerze app, zamiast niego, działa serwer produkcyjny Gunicorn na porcie 8000. (https://gunicorn.org/). Jest to typowy serwer aplikacji wsgi. Kontener wystawia ten port poprzez expose w **docker-compose.yml**.
Nginx bedacy w innym kontenerze (https://www.nginx.com/), wyłapuje upstremem usługe aplikacji app i uruchamia 2 serwery: http na porcie 88 oraz ssl na porcie 443. Dopina do niego dodatkowo wygenerowany certyfikat. Skonfugurowano na nim reverse_proxy ktory jest w stanie przekierować zapytania z portu 88 na 443, dzięki temu za każdym razem gdy wejdziemy na http orazu nas przeniesie to https.
UWAGA: Restapi potrzebuje miec wskazacy port uslugi http aby mogl wylistować. Dlatego w **nginx.conf** musi być podany port 88 w sekcji servera ssl:

**nginx.conf**:

    server {
 
        listen 443 ssl http2;
    
        ssl_certificate_key /etc/nginx/conf.d/certs/localhost.key;
        ssl_certificate /etc/nginx/conf.d/certs/localhost.pem;
    
        ssl_protocols TLSv1.2;
    
        access_log /var/log/nginx/access.log;
        error_log  /var/log/nginx/error_log;
    
        location / {
            proxy_pass http://app;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header Host $host:88; <---- TUTAJ
            proxy_redirect off;
            }


Kolejność odpalania kontenerów zapewnia wait-for-it.sh ktory nasluchuje czy dany serwer sie odpalił po czym odpala kolejne. Link -> https://github.com/vishnubob/wait-for-it

Aby rozpocząć przygotowanie obrazów mozna każdy z osobna zbudować (pamiętaj o kropce!):

    docker build -f dockerfiles/python/Dockerfile .

lub od razu za pomocą komposera:

    docker-compose up --build
    
który zbuduje i odpali wszystkie obrazy.

### Przydatne komendy:

tryb interaktywny dla kontenera app:

    docker exec -it app sh -c 'bash'

kolekcja staticów django w trybie interaktywnym:

    docker exec -it app sh -c 'python3 manage.py collectstatic'

sporzadzanie listy migracyjnej django:

    docker exec -it app sh -c 'python3 manage.py makemigrations'

migracja do bazy:

    docker exec -it app sh -c 'python3 manage.py migrate'

pokazuje wszystkie kontenery:

    docker ps -a

zamykanie wszystkich kontenerów:

    docker rm $(docker ps -a -q)

zamyka kontenery komposera:

    docker-compose down

pokazuje live kontenery i obciążenia:

    docker stats

Export modelu do pliku:

    docker exec -it app sh -c 'python3 manage.py dumpdata HD_app.MODEL export/MODEL.json'

## :satellite: API

Wrzucam przykladowe zapytania do resta za pomocą CURLA. W VBS trzeba bedzie zassać jakąś biblioteke do takich requestów niemniej trzeba pamietać o paru rzeczach aby moć poprawnie wysłac zapytania tj:

> -k -> ignoruj samopodpisywane certy SSL. Dopóki nie mamy takiego.

> -H -> Do zapytania trzeba wrzucić nagłowek w którym uwzglednić trzeba dwie rzeczy: 

- 'Authorization' w tym wypadku nie basicAuth lecz Token, 
- Typ zwracanych danych 'Accept': application/json.

> -d -> Czyli dane jakie chcesz wyslać

Czyli już wiadomo że zawsze przy każdym zapytaniu bedziesz mial {JSONA}

### Przykładowe zapytania:

GET:

    curl -X GET -k https://**IP**/api/order/ -H 'Authorization: Token **TUTAJ_WKLEJ_TOKEN**' -H 'Accept: application/json' | jq

POST:

    curl -X POST -k https://**IP**/api/ordertypes/ -H 'Authorization: Token **TUTAJ_WKLEJ_TOKEN**' -H 'Content-Type: application/json' -d '{"name":"testapi","description":"opisapitestu"}' | jq

PUT:

    curl -X PUT -k https://**IP**/api/ordertypes/ -H 'Authorization: Token **TUTAJ_WKLEJ_TOKEN**' -H 'Content-Type: application/json' -H 'Accept: application/json' -d '{"id":"3","name":"jacek","description":"placek"}' | jq

DELETE:

    curl -X DELETE -k https://**IP**/api/ordertypes/ -H 'Authorization: Token **TUTAJ_WKLEJ_TOKEN**' -H 'Content-Type: application/json' -H 'Accept: application/json' -d '{"id":"1"}' | jq

HINT: jq jest opcjonalna biblioteką do wyswietlania {JSON} w postaci human-readable :)

Adresy API dostepne są tu -> https://IP/api/