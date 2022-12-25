from django.db import models
from django.utils.translation import gettext_lazy as _
from treatment.models import TreatmentContract
from patient.models import Patient
from doctor.models import Doctor
from shared.models import BaseModel
import uuid

# Create your models here.

def _get_default_value():
    return {}

class HealthRecord(BaseModel):
    startedAt = models.DateField(_('started date'), auto_now_add=True)
    endedAt = models.DateField(_('ended date'), null=True)
    name = models.CharField(_('name'), max_length = 64, default = uuid.uuid4)
    patient = models.ForeignKey(
        Patient,
        on_delete = models.DO_NOTHING,
        related_name = 'health_records'
    )
    doctor = models.ForeignKey(
        Doctor,
        on_delete = models.DO_NOTHING,
        related_name = 'health_records',
        null = True
    )
    
    contract = models.ForeignKey(
        TreatmentContract,
        on_delete = models.CASCADE,
        related_name = 'health_records',
        null = True,
    )

    isPatientProvided = models.BooleanField(
        _('is provided by patient'), default=False)
    
    detail = models.JSONField(_('health record detail'), default = _get_default_value)
    
    historical = models.JSONField(_('historical detail'), default = _get_default_value)
    class Meta:
        db_table = 'health_record'
