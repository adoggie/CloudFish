#!/bin/bash

export LC_ALL=en_US.UTF-8
pwd=$(cd `dirname $0`;pwd)
export LD_LIBRARY_PATH=/opt/moca/libs/fa64
export FASoap=/opt/moca/libs/fa64/soap.ini
python $pwd/../moca/service/server.py


