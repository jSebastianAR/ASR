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

EXPOSE 21

#Inicia el servidor en modo foreground
CMD ["proftpd","-n"]