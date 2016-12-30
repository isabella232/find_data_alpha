source /usr/lib/finding/bin/activate
cd /vagrant/src
export DJANGO_SETTINGS_MODULE="find_data.settings.dev"
./manage.py runserver 0.0.0.0:8000
