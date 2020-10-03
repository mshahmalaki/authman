#!/bin/bash
docker run --rm -d --name authmandb \
-e MYSQL_ROOT_PASSWORD=123456 \
-e MYSQL_DATABASE=authman \
-e MYSQL_USER=authman \
-e MYSQL_PASSWORD=123456 \
-p 3316:3306 mysql
export AUTHMAN_DATABASE_URI=mysql+pymysql://authman:123456@192.168.99.102:3316/authman