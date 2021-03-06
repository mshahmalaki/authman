#!/bin/bash

ROOT_PASSWORD="123456"
DATABASE="authman"
USER="authman"
PASSWORD="123456"

docker run --rm -d --name authmandb \
-e MYSQL_ROOT_PASSWORD=$ROOT_PASSWORD \
-e MYSQL_DATABASE=$DATABASE \
-e MYSQL_USER=$USER \
-e MYSQL_PASSWORD=$PASSWORD \
-p 3316:3306 mysql

export AUTHMAN_DATABASE_URI=mysql+pymysql://$USER:$PASSWORD@192.168.99.102:3316/$DATABASE
