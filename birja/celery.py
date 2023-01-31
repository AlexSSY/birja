import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'birja.settings')

app = Celery('birja')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.beat_schedule = {
    'get_p2p_30s': {
        'task': 'app.tasks.get_joke',
        'schedule': 30.0,
    },
}
app.autodiscover_tasks()