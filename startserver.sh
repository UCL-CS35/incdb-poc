#!/bin/bash

/home/deploy/incdb-poc/venv/bin/celery worker -A app.initializers.mycelery -l info -f /home/deploy/log/celeryd.log &
/home/deploy/incdb-poc/venv/bin/gunicorn manage:app --timeout 120  --log-file /home/deploy/log/gunicorn.log &
