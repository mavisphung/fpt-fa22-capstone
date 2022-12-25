from django.db import models
from django.utils import timezone
from service.models import Service
from transaction.models import Order
from shared.models import BaseModel, AppointmentStatus, AppointmentType
from django.utils.translation import gettext_lazy as _
from doctor.models import Doctor, Package, WorkingShift
from patient.models import Patient
from user.models import User
from schedule.models import Schedule
from django.contrib.contenttypes.fields import GenericRelation

def _get_default_value() -> dict:
    return {}

class Appointment(BaseModel):
    bookedAt = models.DateTimeField(default = timezone.now)
    beginAt = models.DateTimeField(null = True)
    endAt = models.DateTimeField(null = True)
    status = models.CharField(
        _('status'), 
        max_length = 15,
        choices = AppointmentStatus.choices,
        default = AppointmentStatus.PENDING
    )
    checkInCode = models.CharField(max_length = 255, unique=True)
    cancelReason = models.TextField(
        _('cancellation reason'), 
        null = True
    )
    diseaseDescription = models.TextField(
        _('patient\'s diseases description'),
        null = True
    )
    isDoctorCancelled = models.BooleanField(_('doctor cancelled'), default = False)
    isSupervisorCancelled = models.BooleanField(_('supervisor cancelled'), default = False)
    isSystemCancelled = models.BooleanField(_('system cancelled'), default = False)
    
    doctor = models.ForeignKey(Doctor, on_delete=models.PROTECT, related_name='appointments')
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT, related_name='appointments')
    booker = models.ForeignKey(User, on_delete=models.PROTECT, related_name='appointments', null = True)
    service = models.ForeignKey(Service, on_delete = models.DO_NOTHING, related_name = 'appointments', null = True)
    
    historical = models.JSONField(_('historical detail'), default = _get_default_value)
    
    schedule = GenericRelation(Schedule, object_id_field = 'object_id', content_type_field = 'content_type', related_query_name = 'appointment')
    order = GenericRelation(Order, object_id_field = 'object_id', content_type_field = 'content_type', related_query_name = 'appointment', null = True)
    
    def __str__(self):
        return f'Id - {self.pk} | Code - {self.checkInCode}'
    
    class Meta:
        db_table = 'appointment'
        