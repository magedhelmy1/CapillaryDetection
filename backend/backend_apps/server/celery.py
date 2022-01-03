import os

from celery import Celery
from kombu import Exchange, Queue

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')

app = Celery('server')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.task_queues = (
    Queue('celery', routing_key='celery'),
    Queue('transient', Exchange('transient', delivery_mode=1),
          routing_key='transient', durable=False),
)

worker_prefetch_multiplier = 128


# @app.task(bind=True)
# def debug_task(self):
#     print(f'Request: {self.request!r}')
