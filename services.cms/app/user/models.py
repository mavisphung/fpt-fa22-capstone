import json
from shared.models import BaseModel
from django.contrib.auth.models import AbstractUser, UserManager
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _
from django.db import models

from shared.models import Profile, NotificationType
from doctor.models import Doctor
# Create your models here.

class CustomUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        email = self.normalize_email(email)
        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.
        # GlobalUserModel = apps.get_model(
        #     self.model._meta.app_label, self.model._meta.object_name
        # )
        # username = GlobalUserModel.normalize_username(username)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)

class UserType(models.TextChoices):
    ADMIN = 'ADMIN'
    MEMBER = 'MEMBER'
    DOCTOR = 'DOCTOR'
    PATIENT = 'PATIENT'
    MANAGER = 'MANAGER'

class User(Profile, AbstractUser):
    
    first_name = None
    last_name = None
    username = None
    
    email = models.EmailField(
        _('email address'),
        unique = True,
        max_length = 150
    )
    
    type = models.CharField(
        _('user type'), 
        max_length = 10, 
        choices = UserType.choices,
        default = UserType.MEMBER
    )
    
    googleId = models.CharField(
        _('google id'),
        max_length = 255,
        null = True,
        blank = True
    )
    
    # balance
    tempBalance = models.FloatField(_('temp balance'), default = 0.0)
    mainBalance = models.FloatField(_('main balance'), default = 0.0)
    
    # Link to Doctor profile
    doctor = models.OneToOneField(Doctor, on_delete = models.RESTRICT, related_name = 'account', null = True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()
    
class VerificationCode(BaseModel):
    code = models.CharField(_('verify code'), max_length = 10)
    expiredAt = models.DateTimeField(_('expiry date'))
    isUsed = models.BooleanField(_('status'), default = False)
    
    # foreign key
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'verify_codes')
    
    def __str__(self):
        return self.code
    
    class Meta:
        db_table = 'verification_code'
        

def _get_default_dict():
    return {}

class Notification(BaseModel):
    user    = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'notifications')
    type    = models.CharField(max_length = 10, choices = NotificationType.choices, default = NotificationType.INFO)
    isRead  = models.BooleanField(default = False)
    title   = models.CharField(max_length = 256, null = True, blank = True)
    message = models.CharField(max_length = 256, null = True, blank = True)
    payload = models.JSONField(null = True, blank = True, default = _get_default_dict)
    
    def __str__(self):
        return f'Notification: {self.title}'
    
    @property
    def to_json(self) -> str:
        return json.dumps({
            'type': self.type,
            'title': self.title,
            'message': self.message,
            'payload': self.payload,
        })
    
    class Meta:
        db_table = 'notification'