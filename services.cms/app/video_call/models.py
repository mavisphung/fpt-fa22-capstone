from django.db import models
from shared.models import BaseModel
from doctor.models import Doctor
from patient.models import Patient
from user.models import User
# from django.contrib.contenttypes.fields import GenericRelation 

class VideoConference(BaseModel):
    doctor = models.ForeignKey(Doctor,  on_delete  = models.CASCADE, related_name = 'conferences')
    patient = models.ForeignKey(Patient , on_delete = models.CASCADE, related_name = 'conferences')
    supervisor  = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'conferences')
    channel = models.CharField(max_length = 255)
    supervisorToken = models.CharField(max_length = 300)
    doctorToken = models.CharField(max_length = 300)
    beginAt = models.DateTimeField()
    isExpire = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'video_room'
        
