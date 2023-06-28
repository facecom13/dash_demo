#!/bin/bash
# cd project || exit
rm -r migrations
python delete_alembic.py
flask db init
flask db migrate -m 'init'
flask db upgrade

gunicorn -k geventwebsocket.gunicorn.workers.GeventWebSocketWorker -w 1 --reload -b 0.0.0.0:8000 app:app
