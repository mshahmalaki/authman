#!/usr/bin/env bash

if [[ -z "$VIRTUAL_ENV" ]]
then
  python3 -m venv venv
  source ./venv/bin/activate
else
  echo "We have a Virtual Environments"
fi

trap ctrl_c INT

function ctrl_c() {
  echo
  echo "** Trapped CTRL-C"
  echo -n "DB Container is stopping"
  for i in `seq 1 5`; do
    sleep 1
    echo -n "."
  done
  echo
  echo -n "DB Container stopped: "
  docker stop authmandb
  echo -n "Deactivating Virtual Environment"
  for i in `seq 1 3`; do
    sleep 1
    echo -n "."
  done
  deactivate
  echo
  echo "Virtual Environment deactivated"
}

pip install --upgrade pip
pip install -r requirements.txt

ROOT_PASSWORD="root"
DATABASE="authman"
USER="authman"
PASSWORD="pass"

unameOut="$(uname -s)"
case "${unameOut}" in
    Linux*)     SYSTEM_IP_ADDRESSES=($(hostname -I))
                export SYSTEM_IP_ADDRESS=${SYSTEM_IP_ADDRESSES[0]}
                ;;
    Darwin*)    export SYSTEM_IP_ADDRESS=($(osascript -e "IPv4 address of (system info)"))
                ;;
    *)          echo "UNKNOWN:${unameOut}"
                exit 1
esac

until docker pull mysql:latest; do sleep 5 ; done

docker run --rm -d --name authmandb \
-e MYSQL_ROOT_PASSWORD=$ROOT_PASSWORD \
-e MYSQL_DATABASE=$DATABASE \
-e MYSQL_USER=$USER \
-e MYSQL_PASSWORD=$PASSWORD \
-p 3316:3306 mysql || true

export AUTHMAN_DATABASE_URI=mysql+pymysql://$USER:$PASSWORD@$SYSTEM_IP_ADDRESSES:3316/$DATABASE

echo -n "Connectiong to DB Container"
for i in {1..30}; do
  flask app testdb > /dev/null
  rc=$?
  if [[ $rc -eq 0 ]]; then
    break
  fi
  sleep 1
  echo -n "."
done

echo

if [[ $rc -ne 0 ]]; then
  echo "Service tests failed."
  exit 1
fi

echo "Migration:"
flask db upgrade

echo "Run server:"
flask run --host=0.0.0.0
