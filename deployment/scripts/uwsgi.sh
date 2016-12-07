#!/bin/bash

pwd=$(cd `dirname $0`;pwd)

echo  '[uwsgi]' > $pwd/../moca/etc/uwsgi_lemon.ini
echo  'socket = 127.0.0.1:8089' >> $pwd/../moca/etc/uwsgi_lemon.ini
echo  "chdir = /opt/moca/model/django/project" >> $pwd/../moca/etc/uwsgi_lemon.ini
echo  "wsgi-file = /opt/moca/model/django/project/wsgi.py" >> $pwd/../moca/etc/uwsgi_lemon.ini
echo  "processes = 4" >> $pwd/../moca/etc/uwsgi_lemon.ini
echo  "threads = 2" >> $pwd/../moca/etc/uwsgi_lemon.ini
echo  "stats = 127.0.0.1:9191" >> $pwd/../moca/etc/uwsgi_lemon.ini
echo  "buffer-size = 131072" >> $pwd/../moca/etc/uwsgi_lemon.ini


/home/bin/uwsgi $pwd/../moca/etc/uwsgi_lemon.ini

