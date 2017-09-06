#!/usr/bin/env bash

git pull
kill $(ps aux | grep 'gunicorn' | awk '{print $2}')
nohup gunicorn -k geventwebsocket.gunicorn.workers.GeventWebSocketWorker -w 1  -b 127.0.0.1:8000 wsgi:app &
