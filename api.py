from flask import Flask, json, request
from redis import Redis
from datetime import datetime
from rq import Queue
from rq.job import Job
from rq.registry import FinishedJobRegistry
import time, platform

# TODO dynamically import tasks so this file doesn't need to be updated.
import tasks

api = Flask(__name__)

@api.route('/average', methods=['GET'])
def get_average():

  avg_time = {}
  redis = Redis()
  qs = ['high','default','low']
  for q in qs:
    registry = FinishedJobRegistry(name=q, connection=redis)
    averages = []
    for job_id in registry.get_job_ids():
      job = Job.fetch(job_id, connection=redis)
      averages.append((job.ended_at - job.enqueued_at).total_seconds())
    ave = sum(averages) / len(averages)
    avg_time[q] = time.strftime('%H:%M:%S', time.gmtime(ave))
      
  response = api.response_class(
    response=json.dumps(avg_time),
    status=200,
    mimetype='application/json'
    )
  return response

@api.route('/task/<job_id>', methods=['GET'])
def find_task(job_id):

  redis = Redis()

  # TODO: Invalid jobs throw exception, find more elegant way to do this
  try:
    job = Job.fetch(job_id, connection=redis)
    job_status = job.get_status()
  except:
    job_status = 'job not found'

  response = api.response_class(
    response=json.dumps({'job_status':job_status}),
    status=200,
    mimetype='application/json'
    )
  return response

@api.route('/task', methods=['GET'])
def get_task():

  qs = ['high','default','low']
  redis_conn = Redis()

  for cue in qs:

    q = Queue(cue, connection=redis_conn)

    if len(q) > 0:
      queued_job_ids = q.job_ids # Gets a list of job IDs from the queue
      next_job = queued_job_ids[0]
      process = cue
  
      data = {'process':process, 'job_id':next_job, 'status':'job found'}

      response = api.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
        )
      return response

    response = api.response_class(
      response=json.dumps({'status':'no jobs waiting'}),
      status=200,
      mimetype='application/json'
      )
  return response


@api.route('/task', methods=['POST'])
def set_task():

  required = ['job_id', 'submitter_id', 'command']
  optional = ['processor_id']
  missing = []
  data = {}

  for val in required:
    if not val in request.form:
      missing.append(val)

  if len(missing) > 0:
    this_status = 400
    data['status'] = 'fail'
    errors = []
    for miss in missing:
      this_response = {miss:'required parameter missing'}
      errors.append(this_response)
    data['errors'] = errors

  else:
    if not request.form['processor_id']:
      pid = 'default'
    else:
      pid = validate_pid(request.form['processor_id'])

    # TODO: Research performance issues opening multiple
    # Redis connections and refactor/optimize code 
    # for scale.
    redis_conn = Redis()
    q = Queue(pid, connection=redis_conn)

    # TODO: Need validate 'command'
    job = q.enqueue(getattr(tasks, request.form['command']), result_ttl=604800)
    this_status = 200
    data['status'] = 'success'
    data['job_id'] = job.id


  response = api.response_class(
    response=json.dumps(data),
    status=this_status,
    mimetype='application/json'
    )
  return response

"""
NOTES: Validating PIDs assumes that 'default' will be used
if an invalid value is sent.  In reality this should return
an error and ask the user to submit a valid PID.
"""
def validate_pid(pid):
  valid_pids = ['high','default','low']
  if pid in valid_pids:
    return pid
  else:
    return 'default'

if __name__ == '__main__':
    api.run()
