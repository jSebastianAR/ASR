################################################################################
# Build a dockerfile for Prosody XMPP server
# Based on ubuntu
################################################################################

FROM debian:10

MAINTAINER Prosody Developers <developers@prosody.im>

# Install dependencies
RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        lsb-base \
        procps \
        adduser \
        libidn11 \
        libicu63 \
        libssl1.1 \
        lua-bitop \
        lua-dbi-mysql \
        lua-dbi-postgresql \
        lua-dbi-sqlite3 \
        lua-event \
        lua-expat \
        lua-filesystem \
        lua-sec \
        lua-socket \
        lua-zlib \
        lua5.1 \
        lua5.2 \
        openssl \
        ca-certificates \
        ssl-cert \
        nano \
        net-tools \
    && rm -rf /var/lib/apt/lists/*

# Install and configure prosody
COPY ./prosody.deb /tmp/prosody.deb
RUN dpkg -i /tmp/prosody.deb
    
COPY prosody.cfg.lua /etc/prosody/ 
COPY docker.com.key /var/lib/prosody/
COPY docker.com.crt /var/lib/prosody/

RUN chown prosody: /etc/prosody/prosody.cfg.lua && chown prosody: /var/lib/prosody/docker.com.key && chown prosody: /var/lib/prosody/docker.com.crt

RUN mkdir -p /var/run/prosody && chown prosody:prosody /var/run/prosody

EXPOSE 5222
ENV __FLUSH_LOG yes

CMD ["prosodyctl", "start"]
