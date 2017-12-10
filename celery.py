from __future__ import absolute_import
from kombu import Queue, Exchange

import os
try:
    os.environ['DJANGO_SETTINGS_MODULE'] = 'myproject.settings'
except:
    pass

from celery import Celery
from datetime import timedelta

app = Celery(broker='redis://', backend='redis://')

period = 600
app.conf.update(
    CELERY_DEFAULT_QUEUE = 'backend',
    CELERY_QUEUES = (
        Queue('backend', Exchange('backend'), routing_key='backend'),
    ),
    #CELERY_IGNORE_RESULT = True,
    CELERY_TASK_RESULT_EXPIRES = 600,
    CELERY_MAX_CACHED_RESULTS = -1,
    CELERY_MAX_TASKS_PER_CHILD = 1,
    CELERYD_TASK_TIME_LIMIT = 600,
    CELERY_ACCEPT_CONTENT = ['json', 'pickle'],
    CELERY_TASK_SERIALIZER = 'pickle',
    CELERY_RESULT_SERIALIZER = 'pickle',
    CELERYBEAT_SCHEDULE = {
        '1h': {
            'task': 'myapp.docker_container.container_killer',
            'schedule': timedelta(seconds=period),
            #'args': [period]
            'kwargs': {"ttl":period, "image":"myghost:latest"} 
        },
    },
)

if __name__ == '__main__':
    app.start()

