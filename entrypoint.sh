#!/bin/bash
flask db upgrade
# gunicorn -w 4 --log-level debug --access-logfile ./acct.log -b 0.0.0.0:5000 "acct:create_app()"
gunicorn -w 4 --log-level debug --access-logfile /dev/fd/1 -b 0.0.0.0:5000 "acct:create_app()"