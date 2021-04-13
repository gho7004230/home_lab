FROM ubuntu:latest

ENV TZ=America/Chicago

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

CMD ["/bin/bash", "-c", "rm -rf /run/httpd/* &&", "/usr/sbin/apachectl", "-D", "FOREGROUND"]
