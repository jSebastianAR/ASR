FROM ubuntu:18.04

RUN apt-get update && apt-get -y install apache2 #Se descarga el servidor http apache2
RUN apt-get install -y net-tools #Se descarga la paqueteria de redes que permite visualizar las interfaces
RUN apt-get install -y nano #Editor de texto de consola

#El puerto 80 queda abierto para que otros contenedores puedan conectarse al servicio
EXPOSE 80 

#Se copian los archivos de las páginas web
COPY Sitio1 /var/www/html/ 
COPY Sitio2 /var/www/html/
COPY Sitio3 /var/www/html/

#Se copian los archivos de configuración deseados para customizar nuestro servidor al modo deseado
COPY apache2.conf /etc/apache2/
COPY 000-default.conf /etc/apache2/sites-available
COPY interfaces /etc/network/

#Se ejecuta apache en primer plano
CMD ["apachectl","-D","FOREGROUND"]

