#!/usr/bin/env bash

git pull
kill $(ps aux | grep 'gunicorn' | awk '{print $2}')
nohup gunicorn -k geventwebsocket.gunicorn.workers.GeventWebSocketWorker -w 1  -b 0.0.0.0:8000 wsgi:app &
