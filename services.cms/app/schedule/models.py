from doctor.models import Doctor
from shared.models import BaseModel
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from shared.models import ScheduleType

# Create your models here.
class Schedule(BaseModel):
    doctor = models.ForeignKey(Doctor, on_delete = models.CASCADE, related_name = 'schedules')
    bookedAt = models.DateTimeField(_('booked at'), null = True)
    estEndAt = models.DateTimeField(_('estimate end at'), null = True)
    
    # Foreign key for session and appointment schedule
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    
    type = models.CharField(_('schedule type'), max_length = 15, choices = ScheduleType.choices, null = True)
    
    def __str__(self):
        return f'{self.id} - {self.bookedAt.strftime("%Y-%m-%d %H:%M")}'
    
    class Meta:
        unique_together   = ('content_type', 'object_id')
        db_table = 'schedule'