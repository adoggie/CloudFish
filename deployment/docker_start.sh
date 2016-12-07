#!/usr/bin/env bash


pwd=$(cd `dirname $0`;pwd)
DEAMON=-d
VER=$1
docker run --name moca --mac-address="12:34:de:b0:6b:61" $DEAMON -it -v $pwd:/opt -p 25432:5432 -p 37017:37017 -p 16379:6379 -p 15672:5672 -p 16001:16001 -p 20020:80 -p 14001:14001 -p 14002:14002 lemon:0.1.4 /run/start.sh
