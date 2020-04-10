import requests
from random import seed
from random import choice

pids = ['high', 'default', 'low']
tasks = ['wait_1', 'wait_2', 'wait_3']

seed(1)
sequence = [i for i in range(3)]
for _ in range(50):
    pid = choice(sequence)
    
    seq = [i for i in range(3)]
    for _ in range(1):
        task = choice(seq)
    
    print('PID:{}, Task:{}'.format(pids[pid], tasks[task]))

    r = requests.post('http://127.0.0.1:5000/task', data = {'job_id':'x808', 'submitter_id':'X5', 'command':tasks[task], 'processor_id':pids[pid]})
    print(r.text)
