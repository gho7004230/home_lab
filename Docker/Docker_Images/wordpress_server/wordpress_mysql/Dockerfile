FROM mysql_server:v1

ENV TZ=America/Chicago
# Req'd for new versions of Ubuntu. Need to set timezone up front
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

ENV MYSQL_PASSWORD=password
ENV MYSQL_USER=wpuser
ENV MYSQL_DATABASE=wordpress

EXPOSE 3306
