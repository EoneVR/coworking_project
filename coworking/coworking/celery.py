import os
from celery import Celery

# Указываем Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coworking.settings')

app = Celery('coworking')

# Загружаем настройки из Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматически ищем tasks.py во всех приложениях
app.autodiscover_tasks()
