#!/bin/bash
if [ ! -d "static" ]; then
    python manage.py collectstatic -c --noinput
fi

python ./manage.py migrate --check
status=$?
if [[ $status != 0 ]]; then
  python ./manage.py migrate
fi

exec "$@"
