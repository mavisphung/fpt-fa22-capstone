from schedule.models import Schedule
from service.models import Service
from shared.models import BaseModel
from django.db import models
from doctor.models import Doctor
from patient.models import Patient
from user.models import User
from transaction.models import Order
from shared.models import ContractStatus
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericRelation
# Create your models here.
    
class TreatmentContract(BaseModel):
    doctor = models.ForeignKey(Doctor, on_delete=models.PROTECT, related_name = 'contracts')
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT, related_name = 'contracts')
    supervisor = models.ForeignKey(User, on_delete=models.PROTECT, related_name = 'contracts')
    service = models.ForeignKey(Service, on_delete=models.PROTECT, related_name = 'contracts', null = True)
    status = models.CharField(
        _('contract status'), 
        choices = ContractStatus.choices, 
        default = ContractStatus.PENDING,
        max_length = 20
    )
    cancelReason = models.CharField(
        _('cancellation reason'),
        max_length = 255,
        null = True,
        blank = True
    )
    startedAt = models.DateTimeField(_('started date'), null = True)
    endedAt = models.DateTimeField(_('ended date'), null = True)
    price = models.FloatField(_('price'), default = 0)
    order = GenericRelation(Order, object_id_field = 'object_id', content_type_field = 'content_type', related_query_name = 'treatment_contract', null = True)
    isSupervisorCancelled = models.BooleanField(_('Is_Supervisor_Cancel'), default = False)
    isDoctorCancelled = models.BooleanField(_('Is_Doctor_Cancel'), default = False)
    isSystemCancelled = models.BooleanField(_('Is_System_Cancel'), default = False)
    class Meta:
        db_table = 'treatment_contract'


from slot.models import DoctorSlot

class SessionStatus(models.TextChoices):
    COMPLETED  =  'COMPLETED'
    IN_PROGRESS = 'IN_PROGRESS'
    PENDING = 'PENDING'
    CANCELLED = 'CANCELLED'

def _get_default_value():
    return {}
class TreatmentSession(BaseModel): 
    doctor  = models.ForeignKey(Doctor, related_name = 'treatment_sessions', on_delete = models.PROTECT, null = True)
    patient = models.ForeignKey(Patient, related_name = 'treatment_sessions', on_delete = models.PROTECT, null = True)
    supervisor = models.ForeignKey(User, related_name = 'treatment_sessions', on_delete = models.PROTECT, null = True)
    contract = models.ForeignKey(TreatmentContract, related_name = 'treatment_sessions', on_delete = models.PROTECT, null= True)
    checkInCode =models.CharField(_('check in code'), max_length = 255, default = '123456')
    status = models.CharField(_('Status'), max_length = 255, default = SessionStatus.PENDING, choices= SessionStatus.choices)
    assessment = models.JSONField(_('assessment'), default= _get_default_value)
    note = models.JSONField(_('note'), default= _get_default_value)
    isSupervisorCancelled = models.BooleanField(_('Is_Supervisor_Cancel'), default = False)
    isDoctorCancelled = models.BooleanField(_('Is_Doctor_Cancel'), default = False)
    isSystemCancelled = models.BooleanField(_('Is_System_Cancel'), default = False)
    cancelReason = models.CharField(
        _('cancellation reason'),
        max_length = 255,
        null = True,
        blank = True
    )
    startTime = models.DateTimeField(_('start time'), null= True)
    endTime = models.DateTimeField(_('end time'), null= True)
    slot = GenericRelation(Schedule, object_id_field = 'object_id', content_type_field = 'content_type', related_query_name = 'treatment_session')
    class Meta:
        db_table = 'treatment_sessions'
    
