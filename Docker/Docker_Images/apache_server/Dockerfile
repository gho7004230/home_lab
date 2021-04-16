FROM ubuntu

ENV TZ=America/Chicago
# Req'd for new versions of Ubuntu. Need to set timezone up front
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update && apt-get -y install \
    apache2

EXPOSE 80

VOLUME ${PWD}/data:/data

CMD ["/usr/sbin/apachectl", "-D", "FOREGROUND"]
