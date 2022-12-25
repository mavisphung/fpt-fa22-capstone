from datetime import timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.models import DjangoJobExecution, DjangoJob
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler import util
from django.utils import timezone
from django.db import transaction
import logging
from shared.models import AppointmentStatus, ContractStatus

from appointment.models import Appointment
from treatment.models import TreatmentContract

logger = logging.getLogger(__name__)

# logger.info('Querying all misfire job...')
# misfire_jobs =  DjangoJob.objects.filter(next_run_time__lte = timezone.now())
# print('misfire_jobs', misfire_jobs)
global scheduler
scheduler = BackgroundScheduler(daemon = True)
scheduler.add_jobstore(DjangoJobStore(), "default")

# for job in misfire_jobs:
#     temp = scheduler.get_job(job.id)
#     print(temp)
#     print(type(temp))
#     print(dir(temp))
logger.info('Executed old jobs successfully...')

@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    """
    This job deletes APScheduler job execution entries older than `max_age` from the database.
    It helps to prevent the database from filling up with old historical records that are no
    longer useful.
    
    :param max_age: The maximum length of time to retain historical job execution records.
                    Defaults to 7 days.
    """
    DjangoJobExecution.objects.delete_old_job_executions(max_age)

scheduler.add_job(
    delete_old_job_executions,
    trigger = CronTrigger(
        day_of_week = "mon", hour = "00", minute = "00"
    ),  # Midnight on Monday, before start of the next work week.
    id="delete_old_job_executions",
    max_instances = 1,
    replace_existing = True,
)

logger.info("Added weekly job: 'delete_old_job_executions'.")
# Remove expiry appointment
def remove_expiry_appointment():
    with transaction.atomic():
        logger.info('Task: Removing old appointments with status PENDING')
        past_day = timezone.now()
        try:
            updated = Appointment.objects\
                .filter(
                    bookedAt__date__lt = timezone.now(), 
                    status__in = [AppointmentStatus.PENDING, AppointmentStatus.IN_PROGRESS]
                )\
                .update(
                    cancelReason = 'Đã hủy vì quá giờ hẹn',
                    status = AppointmentStatus.CANCELLED,
                    isSystemCancelled = True,
                    endAt = past_day + timedelta(hours = 7)
                )
            logger.info(f'Affected {updated} row(s)')
        except:
            logger.info('Removal Task invoked but no pending appointment expired')
        logger.info('Removal Task succeeded')

scheduler.add_job(
    remove_expiry_appointment,
    trigger = CronTrigger.from_crontab('0 5 * * *'),
    id = 'remove_expiry_appointment',
    max_instances = 1,
    replace_existing = True
)
logger.info("Added daily job: 'remove_expiry_appointment'.")

def remove_expired_nonsign_contract():
    with transaction.atomic():
        logger.info(
            'Task: Removing expired to sign|approve contract with status PENDING or Approved')
        try:
            updated = TreatmentContract.objects.filter(startedAt__date__lt=timezone.now())\
                .filter(status__in=[ContractStatus.APPROVED, ContractStatus.PENDING])\
                .update(
                    cancelReason='Đã hủy vì chưa có được giám hộ hoặc bác sĩ kí kết trước khi thời điểm hẹn bắt đầu',
                    status=ContractStatus.CANCELLED,
                    isSystemCancelled = False
            )
            logger.info(f'Affected {updated} row(s)')
        except:
            logger.info(
                'Removal Task invoked but no pending appointment expired')
        logger.info('Removal Task succeeded')

scheduler.add_job(
    remove_expired_nonsign_contract,
    trigger = CronTrigger.from_crontab('0 2 * * *'),
    id = 'remove_expired_nonsign_contract',
    max_instances = 1,
    replace_existing = True
)


scheduler.print_jobs()
if not scheduler.running:
    scheduler.start()
    logger.info('Scheduler has been started')