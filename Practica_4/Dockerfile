FROM ubuntu:latest

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -q -y --no-install-recommends isc-dhcp-server

COPY dhcpd.conf /etc/dhcp
COPY isc-dhcp-server /etc/default/
RUN service isc-dhcp-server start

CMD [ "dhcpd", "-d" ]