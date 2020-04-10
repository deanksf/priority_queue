#!/bin/sh
sudo apt-get install software-properties-common
sudo apt-add-repository universe
sudo apt-get update
sudo apt install python3-pip
sudo apt install emacs25
pip3 install flask
pip3 install rq
sudo apt install redis-server

# Linux
sudo apt install curl
sudo pip3 install redis

# MAC
pip3 install pycurl
brew install redis
redis-server > /dev/null 2>&1 &
python3 api.py > /dev/null 2>&1 &
rq worker high default low > /dev/null 2>&1 &
