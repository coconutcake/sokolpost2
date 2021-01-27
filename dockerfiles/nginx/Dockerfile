FROM nginx

ADD /nginx_config/nginx.conf /etc/nginx/nginx.conf
COPY /certs /etc/nginx/conf.d/certs
COPY wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh


CMD ["/wait-for-it.sh", "app:8000", "--timeout=30", "--", "nginx", "-g", "daemon off;"]

