import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'track2.settings')

app = Celery('track2')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
app.broker_connection_retry_on_startup = True