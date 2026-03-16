FROM php:7.2-apache

RUN echo "deb http://archive.debian.org/debian stretch main contrib non-free" > /etc/apt/sources.list
RUN apt-get update && apt-get install zip -y

WORKDIR /var/www/html
COPY ./src .
COPY flag.txt /aefd123cdf_secret.txt
# config permission
RUN chown -R root:www-data /var/www/html
RUN chmod 750 /var/www/html
RUN find . -type f -exec chmod 640 {} \;
RUN find . -type d -exec chmod 750 {} \;

RUN chmod +t -R /var/www/html/