from doctor.models import Doctor
from shared.models import BaseModel
from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Specialist(BaseModel):
    name = models.CharField(_('specialist name'), max_length = 64, null = True)
    description = models.CharField(_('description'), max_length = 255, null = True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'specialist'
        
class DoctorSpecialist(BaseModel):
    doctor = models.ForeignKey(Doctor, on_delete = models.CASCADE, related_name = 'specialists')
    specialist = models.ForeignKey(Specialist, on_delete = models.CASCADE, related_name = 'doctors')
    
    def __str__(self):
        return f'Doctor id {self.doctor_id} | Specialist id {self.specialist_id}'
    
    class Meta:
        db_table = 'doctor_specialist'