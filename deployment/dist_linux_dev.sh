#!/bin/bash

pwd=$(cd `dirname $0`;pwd)
alias cp='cp -f'
#alias cp='rsync'
#alias rsync='rsync -r'


RELEASE_DIR=$pwd/release

if [ $# == 0 ]; then
  echo 'Warning: params is 0, default: [release]'
else
  RELEASE_DIR=$(echo $1)
fi
PRJ_DIR=$(echo $RELEASE_DIR)/moca
echo $RELEASE_DIR



mkdir -p $RELEASE_DIR/nginx/log
mkdir -p $PRJ_DIR/
mkdir -p $PRJ_DIR/src/
mkdir -p $PRJ_DIR/test/
mkdir -p $PRJ_DIR/bin

mkdir -p $RELEASE_DIR/file
mkdir -p $RELEASE_DIR/package

SRC_HOME=$pwd/..
echo $SRC_HOME


rsync -rvt $SRC_HOME/3rd/Django-1.6.5.tar.gz $RELEASE_DIR/package
rsync -rvt $SRC_HOME/3rd/poster-0.8.1.tar.gz $RELEASE_DIR/package


#cp -r $pwd/../client $PRJ_DIR
rsync -rvt $pwd/../client $PRJ_DIR

rsync -rvt $pwd/../etc $PRJ_DIR

rsync -rvt $pwd/../lemon $PRJ_DIR
rsync -arvt $pwd/../libs $PRJ_DIR
rsync -rvt $pwd/../model $PRJ_DIR
rsync -rvt $pwd/../service $PRJ_DIR
rsync -rvt $pwd/../moca $PRJ_DIR


rsync -rvt $pwd/../src/web $PRJ_DIR/src
rsync -rvt $pwd/../init_script.py $PRJ_DIR



rsync -rvt $pwd/../test/init_data.py $PRJ_DIR/test



rsync clean.sh docker_start.sh service_start.sh init_pgsql.sh service_stop.sh $RELEASE_DIR
rsync -rvt $pwd/../etc/nginx  $RELEASE_DIR/
rsync -rvt $pwd/scripts $RELEASE_DIR/


#rsync -rvt $SRC_HOME/src/pdf_converter/pdf_convert $PRJ_DIR/bin
#rsync -rvt $SRC_HOME/service/file_convert $RELEASE_DIR



sed -e 's/server1/localhost/' -e 's/192.168.10.99/localhost/' $pwd/../etc/settings.yaml > $PRJ_DIR/etc/settings.yaml
sed -e 's/server1/localhost/' -e 's/server2/localhost/' $pwd/../etc/services.xml > $PRJ_DIR/etc/services.xml
bash $RELEASE_DIR/scripts/ssl_enable.sh

