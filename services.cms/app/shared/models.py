from django.db import models
from django.utils.translation import gettext_lazy as _

class BaseModel(models.Model):
    createdAt = models.DateTimeField(auto_now_add = True)
    updatedAt = models.DateTimeField(auto_now = True)
    
    class Meta:
        abstract = True
        
class Gender(models.TextChoices):
    MALE = 'MALE'
    FEMALE = 'FEMALE'
    OTHER = 'OTHER'

class Profile(BaseModel):
    firstName = models.CharField(_('first name'), max_length = 64, blank = True, db_index = True)
    lastName = models.CharField(_('last name'), max_length = 64, blank = True, db_index = True)
    dob = models.DateField(_('date of birth'), null = True)
    avatar = models.CharField(_('avatar'), max_length = 255, null = True)
    phoneNumber = models.CharField(_('phone number'), max_length = 20, blank = True)
    address= models.CharField(_('address'), max_length = 255, null = True)
    gender = models.CharField(
        _('gender'), max_length = 10,
        choices = Gender.choices,
        default = Gender.OTHER
    )
    age = models.IntegerField(_('age'), null = True)
    class Meta:
        abstract = True
        
class RateModel(models.Model):
    totalPoints = models.FloatField(_('total rate points'), default = 0)
    turns = models.IntegerField(_('rate turns'), default = 0)
    
    def add_point(self, point):
        self.totalPoints += point
        self.turns += 1
        
    def get_rate(self) -> float:
        if self.turns == 0:
            return 0
        return (self.totalPoints / self.turns)
    
    class Meta:
        abstract = True
        
class SoftDelete(models.Model):
    is_deleted = models.BooleanField(_('is deleted'), default = False)
    class Meta:
        abstract = True
        
class LoginPlatform(models.TextChoices):
    FACEBOOK = 'FACEBOOK'
    GOOGLE = 'GOOGLE'
    
class ContractStatus(models.TextChoices):
    APPROVED = 'APPROVED'
    IN_PROGRESS = 'IN_PROGRESS'
    EXPIRED = 'EXPIRED'
    PENDING = 'PENDING'
    CANCELLED = 'CANCELLED'
    POSTPONE = 'POSTPONE',
    SIGNED = 'SIGNED'
    
class AppointmentStatus(models.TextChoices):
    COMPLETED = 'COMPLETED'
    CANCELLED = 'CANCELLED'
    IN_PROGRESS = 'IN_PROGRESS'
    PENDING = 'PENDING'
    
class AppointmentType(models.TextChoices):
    ONLINE = 'ONLINE'
    OFFLINE = 'OFFLINE'
    
class WeekDay(models.IntegerChoices):
    SUNDAY = 1
    MONDAY = 2
    TUESDAY = 3
    WEDNESDAY = 4
    THURSDAY = 5
    FRIDAY = 6
    SATURDAY = 7

class ScheduleType(models.TextChoices):
    SESSION = 'SESSION'
    APPOINTMENT = 'APPOINTMENT'

class PrescriptionStatus(models.TextChoices):
    ACTIVE = 'ACTIVE'
    CANCELLED = 'CANCELLED'
    EXPIRED = 'EXPIRED'
    
class NotificationType(models.TextChoices):
    INFO = 'INFO'
    WARN = 'WARN'
    
class ServiceCategory(models.TextChoices):
    AT_PATIENT_HOME = 'AT_PATIENT_HOME'
    AT_DOCTOR_HOME = 'AT_DOCTOR_HOME'
    ONLINE = 'ONLINE'
    CONTRACT = 'CONTRACT'
    
class Search(models.Lookup):
    lookup_name = 'search'

    def as_mysql(self, compiler, connection):
        lhs, lhs_params = self.process_lhs(compiler, connection)
        rhs, rhs_params = self.process_rhs(compiler, connection)
        params = lhs_params + rhs_params
        return 'MATCH (%s) AGAINST (%s IN BOOLEAN MODE)' % (lhs, rhs), params
    
models.CharField.register_lookup(Search)
models.TextField.register_lookup(Search)
