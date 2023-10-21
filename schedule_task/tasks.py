from celery import shared_task


@shared_task
def add():
    x = 10
    y = 20
    return x + y


@shared_task
def mul(x, y):
    return x * y

