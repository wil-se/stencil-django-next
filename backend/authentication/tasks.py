from celery import shared_task, Task
from backend.celery import app
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@app.task
def add(x, y):
    logger.info('Adding {0} + {1}'.format(x, y))
    return x + y


@shared_task
def mul(x, y):
    return x * y

@shared_task
def xsum(numbers):
    return sum(numbers)


class DatabaseTask(Task):
    _db = None

    @property
    def db(self):
        if self._db is None:
            # self._db = Database.connect()
            pass
        return self._db
