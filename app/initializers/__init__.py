# __init__.py is a special Python file that allows a directory to become
# a Python package so it can be accessed using the 'import' statement.

# Intentionally left empty

from celery import Celery, Task
from app.initializers import settings


def make_celery(app):
    """ Initialize and return a new Celery instance """
    celery = Celery(app.import_name, broker=settings.CELERY_BROKER_URL,
                    backend=settings.CELERY_RESULT_BACKEND)
    celery.conf.update(CELERY_ACCEPT_CONTENT=['json'],
                       CELERY_TASK_SERIALIZER='json',
                       CELERY_RESULT_SERIALIZER = 'json')
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery

class DBTask(Task):
    _session = None

    def after_return(self, *args, **kwargs):
        if self._session is not None:
            self._session.remove()

    @property
    def session(self):
        if self._session is None:
        	self._session = db.create_scoped_session()

        return self._session

