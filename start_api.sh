#!/bin/sh
# TODO: Use package manager so we don't keep trying to load

sudo apt-get install software-properties-common
sudo apt-add-repository universe
sudo apt-get update
sudo apt install python3-pip
sudo apt install emacs25
pip3 install flask
pip3 install rq
sudo apt install redis-server

echo $(uname)
if [ "$(uname)" == "Darwin" ]
then
    pip3 install pycurl
    brew install redis
elif [ "$(uname)" == "Linux" ]
then
    sudo apt install curl
    sudo pip3 install redis
fi


redis-server > /dev/null 2>&1 &
# To kill: sudo /etc/init.d/redis-server stop
python3 api.py > /dev/null 2>&1 &
rq worker high default low > /dev/null 2>&1 &

