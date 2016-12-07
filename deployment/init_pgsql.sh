#!/bin/bash

pwd=$(cd `dirname $0`;pwd)

echo 'waiting for database is ok..'
sleep 4
echo 'create database moca..'
su - postgres -c "createdb moca"
echo 'alter user role..'
su - postgres -c "psql -c \"alter user postgres with password '111111'\" "

echo "create tables.."
cd /opt/moca/model/django
python manage.py syncdb --noinput
cd -
sleep 1
echo "init data scripts.."
cd /opt/moca/test
python init_data.py
cd -
