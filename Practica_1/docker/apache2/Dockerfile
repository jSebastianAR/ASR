FROM ubuntu:18.04

RUN apt-get update && apt-get -y install apache2
EXPOSE 80

COPY Sitio1 /var/www/html/
COPY Sitio2 /var/www/html/
CMD ["apachectl","-D","FOREGROUND"]