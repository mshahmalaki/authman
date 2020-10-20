#!/bin/bash

for i in {1..7}; do
  flask app testdb > /dev/null
  rc=$?
  if [[ $rc -eq 0 ]]; then
    break
  fi
  sleep 5
done

if [[ $rc -ne 0 ]]; then
  echo "Service tests failed."
  exit 1
fi

echo "Migration ..."
flask db upgrade

echo "Run server ..."
flask run --host=0.0.0.0
