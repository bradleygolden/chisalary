from celery.task.schedules import crontab
from celery.decorators import periodic_task
from .manager import EmployeeManager


# execute daily at midnight
@periodic_task(run_every=(crontab(minute=0, hour=0)),
               name="sync_employees",
               ignore_result=True)
def sync_employees():
    EmployeeManager().sync_employees()
