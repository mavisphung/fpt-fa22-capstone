from doctor.models import Doctor
from shared.models import BaseModel, SoftDelete

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericRelation


class DoctorSlotState(models.TextChoices):
    EXPIRED = 'EXPIRED'
    AVAILABLE = 'AVAILABLE'
    BOOKED = 'BOOKED'


class DoctorSlot(BaseModel, SoftDelete):
    date = models.DateField(_('day of week'))
    start = models.TimeField(_('start'))
    end = models.TimeField(_('end'))
    doctor = models.ForeignKey(Doctor, related_name='slots', null=True, on_delete=models.DO_NOTHING)
    status = models.CharField(_('status'), choices= DoctorSlotState.choices, default=DoctorSlotState.AVAILABLE, max_length= 20)
    class Meta:
        db_table = 'doctor_slots'