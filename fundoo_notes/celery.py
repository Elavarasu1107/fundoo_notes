import os
from celery import Celery
from dotenv import load_dotenv

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fundoo_notes.settings")
app = Celery("fundoo_notes")
load_dotenv()
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
