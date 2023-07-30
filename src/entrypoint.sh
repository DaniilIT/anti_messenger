#!/bin/bash
python ./manage.py collectstatic -c --no-input
python ./manage.py migrate --check
status=$?
if [[ $status != 0 ]]; then
  python ./manage.py migrate
fi
exec "$@"
