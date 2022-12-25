from django.db import models
from shared.models import BaseModel, Gender
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from user.models import User

# Create your models here.
class Patient(BaseModel):
    firstName = models.CharField(_('first name'), max_length = 64, blank = True)
    lastName  = models.CharField(_('last name'), max_length = 64, blank = True)
    dob       = models.DateField(_('date of birth'), null = True)
    address   = models.CharField(_('address'), max_length = 255, null = True)
    gender    = models.CharField(
        _('gender'), max_length = 10,
        choices = Gender.choices,
        default = Gender.OTHER
    )
    avatar    = models.CharField(_('avatar'), max_length = 255, blank = True)
    
    # Supervisor
    supervisor = models.ForeignKey(User, on_delete = models.DO_NOTHING, related_name = 'patient_profiles', null = True)
    
    old_health_records = models.JSONField(_('old health records'), null = True)
    
    @property
    def age(self):
        now = timezone.now().year
        age = (now - self.dob.year) if self.dob is not None else None
        return age
    
    class Meta:
        db_table = 'patient'
