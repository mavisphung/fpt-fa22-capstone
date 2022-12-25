from django.db import models
from shared.models import BaseModel
from health_record.models import HealthRecord
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Disease(BaseModel):
    code = models.CharField(_('code'), max_length = 255, null = True)
    otherCode = models.CharField(_('other code'), max_length = 255, null = True)
    generalName = models.CharField(_('general name'), max_length = 255, null = True)
    vGeneralName = models.CharField(_('vietnamese general name'), max_length = 255, null = True)
    diseaseName = models.CharField(_('disease name'), max_length = 255, null = True)
    vDiseaseName = models.CharField(_('vietnamese disease name'), max_length = 255, null = True)
    
    def __str__(self):
        return f'{self.vGeneralName}-{self.vDiseaseName}'
    
    def to_dict(self) -> dict:
        return {
            'id': self.pk,
            'code': self.code,
            'otherCode': self.otherCode,
            'vGeneralName': self.vGeneralName,
            'vDiseaseName': self.vDiseaseName
        }
    
    class Meta:
        db_table = 'disease'
        
class Diagnose(BaseModel):
    disease = models.ForeignKey(Disease, on_delete = models.CASCADE, related_name = 'diagnoses')
    healthRecord = models.ForeignKey(HealthRecord, on_delete=models.CASCADE, related_name = 'diagnoses')
    description = models.CharField(_('diagnose description'), max_length = 500)
    
    class Meta:
        db_table = 'disease_diagnose'