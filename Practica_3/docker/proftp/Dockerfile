FROM debian:10

#Instala todas las dependencias del servidor proftpd en modo no interactivo(automatico)

RUN apt-get update && \
	DEBIAN_FRONTEND=noninteractive apt-get install -q -y --no-install-recommends \
	adduser \
	debianutils \
	libacl1 \
	libattr1 \
	libc6 \
	libcap2 \
	libhiredis0.14 \
	libmemcached11 \
	libmemcachedutil2 \
	libncursesw6 \
	libpam-runtime \
	libpam0g \
	libpcre3 \
	libssl1.1 \
	libtinfo6 \
	libwrap0 \
	lsb-base \
	netbase \
	sed \
	ucf \
	zlib1g \
	openssl \
    ca-certificates \
    ssl-cert \
    nano \
	net-tools

#Copia el .deb para instalar el servidor
COPY ./proftpd.deb /tmp/proftpd.deb
RUN dpkg -i /tmp/proftpd.deb

#Creando carpetas de subida y descarga de archivos, además agregando una shell falsa que impide que los usuarios accedan a terminal

RUN mkdir /home/ftp/

#Copia 
COPY ftpdirectory /home/ftp/

#chown root: /home/ftp/upload && chown root: /home/ftp/download	 \

RUN chmod 777 /home/ftp/upload && chmod 755 /home/ftp/download && \
 echo "/bin/false" >> /etc/shells && \
 adduser laptop --home /home/ftp/ -shell /bin/false 

# echo "AllowForeignAddress             on" >> /etc/proftpd/proftpd.conf	#Permite las conexiones de ip's foraneas

EXPOSE 21

#Inicia el servidor en modo foreground
CMD ["proftpd","-n"]