redis-server > /dev/null 2>&1 &
python3 api.py > /dev/null 2>&1 &
rq worker high default low > /dev/null 2>&1 &
