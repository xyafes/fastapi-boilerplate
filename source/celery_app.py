from celery import Celery
from source import broker_url

celery_app = Celery("source", broker=broker_url)
celery_app.config_from_object("source.settings:celery")
celery_app.autodiscover_tasks(["source.tasks"])
