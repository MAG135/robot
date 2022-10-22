FROM library/postgres
COPY init_tiktok_db.sql /docker-entrypoint-initdb.d/
COPY ./set-config.sh /docker-entrypoint-initdb.d/
