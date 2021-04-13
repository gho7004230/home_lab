FROM ubuntu:latest

ENV TZ=America/Chicago
# Req'd for new versions of Ubuntu. Need to set timezone up front
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update && apt-get -y install \
    apache2 \
    php \
    php-mysql \
    wget

RUN wget https://wordpress.org/latest.tar.gz && \
    tar xzvf latest.tar.gz && \
    cp -R ./wordpress/* /var/www/html && \
    rm /var/www/html/index.html

COPY wp-config.php /var/www/html/wp-config.php

EXPOSE 80

RUN rm -rf /run/httpd/*

CMD ["/usr/sbin/apachectl", "-D", "FOREGROUND"]

