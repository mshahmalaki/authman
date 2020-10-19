python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput
gunicorn "{subfolder}.{module_file}:app" -w 10 -b 0.0.0.0:5000 --daemon
python manage.py runserver 0.0.0.0:80

