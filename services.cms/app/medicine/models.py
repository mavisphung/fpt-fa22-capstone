from shared.models import BaseModel
from django.db import models
from doctor.models import Doctor
from patient.models import Patient
from user.models import User
from shared.models import AppointmentStatus, ContractStatus

from django.utils.translation import gettext_lazy as _

# Create your models here.
class Medicine(BaseModel):
    name = models.CharField(_('name'), max_length = 64)
    
    class Meta:
        db_table = 'medicine'