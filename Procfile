web: sh -c 'cd ./src && ./manage.py migrate && gunicorn find_data.wsgi:application -b 0.0.0.0:$PORT --log-file -'
