import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'messproj.settings')
app = Celery('messproj',  include='messproj.celery.main')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
