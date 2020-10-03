from redis import Redis
from rq import Queue, Worker

redis_conn = Redis(host="0.0.0.0", port=6379, db=0)
queue = Queue.from_queue_key("rq:queue:default", connection=redis_conn) 

# Start a worker with a custom name
worker = Worker([queue], connection=redis_conn, name='work1')