from celery import Celery

BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
app = Celery('tasks', broker=BROKER_URL, backend=CELERY_RESULT_BACKEND)

@app.task
def add(x, y):
  return x + y





  # $ celery -A tasks worker --loglevel=info --autoscale=10,3
  # --autoscale=10,3 => worker 개수 최대10개 최소3개