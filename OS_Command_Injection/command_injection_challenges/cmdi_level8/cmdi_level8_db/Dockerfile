FROM mysql:8.0

COPY db.sql /docker-entrypoint-initdb.d/db.sql

CMD ["--default-authentication-plugin=mysql_native_password"]