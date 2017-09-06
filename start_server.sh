#!/usr/bin/env bash

git pull
kill $(ps aux | grep 'what-i-am-grateful-for' | awk '{print $2}')
nohup gunicorn --certfile cert.pem --keyfile key.pem -k geventwebsocket.gunicorn.workers.GeventWebSocketWorker -w 1  -b 0.0.0.0:80 wsgi:app &
