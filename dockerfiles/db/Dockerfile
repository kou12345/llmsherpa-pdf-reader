FROM postgres:15

RUN apt-get update && apt-get install -y \
    wget \
    lsb-release \
    gnupg2 \
    && wget https://apache.jfrog.io/artifactory/arrow/debian/apache-arrow-apt-source-latest-$(lsb_release --codename --short).deb \
    && apt-get install -y -V ./apache-arrow-apt-source-latest-$(lsb_release --codename --short).deb \
    && wget https://packages.groonga.org/debian/groonga-apt-source-latest-$(lsb_release --codename --short).deb \
    && apt-get install -y -V ./groonga-apt-source-latest-$(lsb_release --codename --short).deb \
    && apt-get update \
    && apt-get install -y -V postgresql-15-pgdg-pgroonga \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# PGroonga を初期化するスクリプトをコピー
COPY dockerfiles/db/init-pgroonga.sql /docker-entrypoint-initdb.d/
