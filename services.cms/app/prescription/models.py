from disease.models import Diagnose
from shared.models import PrescriptionStatus
from medicine.models import Medicine
from shared.models import BaseModel
from django.db import models
from health_record.models import HealthRecord
from doctor.models import Doctor
from patient.models import Patient
from user.models import User
from shared.models import AppointmentStatus, ContractStatus

from django.utils.translation import gettext_lazy as _

# Create your models here.

def _getDefaultValue():
    return {}

class Prescription(BaseModel):
    healthRecord = models.ForeignKey(
        HealthRecord, on_delete=models.CASCADE, null=True)
    doctor = models.ForeignKey(Doctor, on_delete = models.CASCADE, related_name = 'prescriptions', null=True)
    patient = models.ForeignKey(Patient, on_delete = models.PROTECT, related_name = 'prescriptions', null=True)
    diagnose = models.JSONField(_("diagnose"), null=True)
    fromDate = models.DateField(_("from_date"), null=True)
    toDate = models.DateField(_("to_date"), null=True)
    cancelReason = models.CharField(_("cancelReason"),max_length = 255, null=True)
    note = models.JSONField(_("note"), default = _getDefaultValue)

    class Meta:
        db_table = 'prescription'
        app_label = 'prescription'


class PrescriptionDetail(BaseModel):
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine, on_delete=models.DO_NOTHING)
    guide = models.TextField(_('guideline'))
    quantity = models.IntegerField(_('quantity'), default = 1)
    unit = models.CharField(_('unit'), null = True, max_length = 30)
    class Meta:
        db_table = 'prescription_detail'
        app_label = 'prescription'
