from shared.models import BaseModel, RateModel, ServiceCategory, SoftDelete
from django.db import models
from django.utils.translation import gettext_lazy as _
from doctor.models import Doctor

# Create your models here.
class Service(BaseModel, SoftDelete):
    name = models.CharField(_('service name'), max_length = 64)
    description = models.CharField(_('service description'), max_length = 500)
    method = models.TextField(_('service method'), null = True, blank = True)
    price = models.FloatField(_('service price'), default = 0.0)
    category = models.CharField(_('category'), max_length = 20, choices = ServiceCategory.choices)
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'service'
        
class DoctorService(BaseModel, RateModel):
    doctor = models.ForeignKey(Doctor, on_delete = models.DO_NOTHING, related_name = 'services', null = True)
    service = models.ForeignKey(Service, on_delete = models.DO_NOTHING, related_name = 'doctors', null = True)
    isActive = models.BooleanField(default = True)
    
    class Meta:
        db_table = 'doctor_service'