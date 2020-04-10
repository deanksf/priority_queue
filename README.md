# API/QUEUING SERVER
## Homework Assignment

### Endpoints
* POST /task - Submit a new task to the queue.
* GET  /task - Get the next available task with highest priority.
* GET  /task/$id - Get the status of the task with id = $id
* GET  /average - Return the average processing time 

### Usage
* Tested on Mac, known issues on EC2
* After downloading, run 'start_api.sh'
* 'rq info' from the command line shows the status of the queues and the worker
* submit.py adds 50 random jobs to the queue. Response includes job_ids
* http://127.0.0.1:5000/task/{job_id} shows the status of the job
* http://127.0.0.1:5000/task shows the next task to be processed
* http://127.0.0.1:5000/average shows the average time to process a job

### Other info
* Redis is used as an option for scaling in the future. Current config uses one server for queues and workers, only launches one worker
* 'Notes' and 'TODO' listed in code comments