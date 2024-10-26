if [[ -z "${SECRET_KEY}" ]]; then
   # export SECRET_KEY=`python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'`
   ./genskey.sh
fi

###
python3 manage.py makemigrations
python3 manage.py migrate

###
if [[ -z "${DJANGO_SUPERUSER_USERNAME}" ]]; then
   export DJANGO_SUPERUSER_USERNAME='admin'
fi
if [[ -z "${DJANGO_SUPERUSER_EMAIL}" ]]; then
   export DJANGO_SUPERUSER_EMAIL='admin@admin.com'
fi
if [[ -z "${DJANGO_SUPERUSER_PASSWORD}" ]]; then
   export DJANGO_SUPERUSER_PASSWORD='admin'
fi

python3 createsuperuser --noinput 

python3 manage.py runserver 0.0.0.0:8000
