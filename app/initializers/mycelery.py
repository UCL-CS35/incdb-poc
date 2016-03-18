from celery import Celery

celery = Celery(
    'tasks',
    broker='redis://localhost:6379',
    backend='redis://localhost:6379',
    include=['app.core.decode']
)

if __name__ == '__main__':
    celery.start()