```
celery -A evolutionlab worker -l INFO
celery -A evolutionlab beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler

```