from email.policy import default
from random import choices
from django.db import models
from shared.models import BaseModel, Profile, RateModel, WeekDay
from django.utils.translation import gettext_lazy as _
import datetime

# Create your models here.
class Doctor(Profile, RateModel):
    email = models.CharField(_('email'), max_length = 255, unique = True, blank = True, null = True)
    experienceYears = models.FloatField(_('experience years'), default = 0)
    isApproved = models.BooleanField(_('is approved'), default = True)
    
    
    def __str__(self):
        return f'{self.firstName} {self.lastName}'
    
    class Meta:
        db_table = 'doctor' # name of collection in database
        
class SpecType(models.TextChoices):
    IMG = 'IMG'
    FILE = 'FILE'
    PDF = 'PDF'

class Specification(BaseModel):
    doctor = models.ForeignKey(Doctor, on_delete = models.CASCADE, related_name = 'specs')
    url = models.CharField(_('url'), max_length = 255)
    type = models.CharField(_('spec type'), max_length = 10, choices = SpecType.choices)
    
    class Meta:
        db_table = 'specification'

class WorkingShift(BaseModel):
    startTime = models.TimeField(_('start time in weekday'), default = datetime.time(9))
    endTime = models.TimeField(_('end time in weekday'), default = datetime.time(17, 30))
    weekday = models.IntegerField(_('weekday'), choices = WeekDay.choices)
    isActive = models.BooleanField(_('active shift'), default = False)
    doctor = models.ForeignKey(Doctor, on_delete = models.CASCADE, related_name = 'shifts')
    
    def __str__(self):
        return f'Weekday {self.weekday} - {self.startTime.strftime("%H:%M:%S")} - {self.endTime.strftime("%H:%M:%S")}'
    
    class Meta:
        db_table = 'working_shift'



class PackageCategory(models.TextChoices):
    AT_DOCTOR_HOME = 'AT_DOCTOR_HOME'
    AT_PATIENT_HOME = 'AT_PATIENT_HOME'
    ONLINE = 'ONLINE'

class Package(BaseModel):
    name = models.CharField(_('package name'), max_length = 64)
    description = models.CharField('package description', max_length = 255)
    price = models.FloatField(_('package price'), default = 0.0)
    commissionPercent = models.FloatField(_('commission'), default = 0.2)
    isOnline = models.BooleanField(_('is online'), default = False)
    category = models.CharField(_('category'), max_length = 20, choices = PackageCategory.choices)
    
    # FK
    doctor = models.ForeignKey(Doctor, on_delete = models.CASCADE, related_name = 'packages')
    
    isApproved = models.BooleanField(_('is approved'), default = True)

    def __str__(self):
        return self.name
    class Meta:
        db_table = 'package'