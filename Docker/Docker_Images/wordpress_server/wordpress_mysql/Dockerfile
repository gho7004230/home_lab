FROM ubuntu:latest

ENV TZ=America/Chicago
# Req'd for new versions of Ubuntu. Need to set timezone up front
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN echo 'mysql-server mysql-server/root_password password root' | \
debconf-set-selections && \
echo 'mysql-server mysql-server/root_password_again password root' | \
debconf-set-selections

RUN apt-get update && apt-get -qqy install \
    mysql-server

EXPOSE 3306

CMD ["/usr/bin/mysqld_safe"]
