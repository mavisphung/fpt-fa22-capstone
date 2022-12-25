from http.client import PARTIAL_CONTENT
from random import choices
from django.db import models
from django.utils.translation import gettext_lazy as _
from shared.models import BaseModel
from doctor.models import Doctor
from patient.models import Patient
from health_record.models import HealthRecord

class MedicalInstructionCategory(BaseModel):
    name = models.CharField(max_length=100)

class MedicalInstructionStatus(models.TextChoices):
    PENDING= 'PENDING'
    COMPLETED = 'COMPLETED'
    CANCELLED = 'CANCELLED'

class MedicalInstruction(BaseModel):
    healthRecord = models.ForeignKey(HealthRecord, related_name="medical_instructions", on_delete= models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete = models.CASCADE, related_name = 'medical_instructions', null = True)
    patient = models.ForeignKey(Patient, on_delete = models.CASCADE, related_name = 'medical_instructions')
    category = models.ForeignKey(MedicalInstructionCategory, on_delete = models.SET_NULL, related_name = 'medical_instructions',null=True)
    requirments = models.JSONField(_('requirments'))
    submissions = models.JSONField(_('submissions'), null=True)
    status = models.TextField(_('status'),max_length=100, choices = MedicalInstructionStatus.choices, default= MedicalInstructionStatus.PENDING)
    
    def __str__(self):
        return f'{self.requirments}'

class MedicalInstructionFeedback(BaseModel):
    instruction = models.ForeignKey(MedicalInstruction , related_name="feedbacks", on_delete = models.CASCADE)
    message = models.CharField(_('message'),null=True, max_length=300)
    attachment = models.CharField(_('attachment'),null=True, max_length=300)
