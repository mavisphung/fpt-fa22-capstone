from prescription.models import Prescription, PrescriptionDetail
from instruction.models import MedicalInstruction
from health_record.models import HealthRecord
from shared.exceptions import CustomValidationError

def clonePrescription(prescription_id: int, clonedHealthRecord: HealthRecord):
    print('before cloning loop 6')
    src: Prescription = Prescription.objects.filter(pk=prescription_id).first()
    src.healthRecord = clonedHealthRecord
    src.pk = None
    src.save()
    details = PrescriptionDetail.objects.filter(prescription__pk=prescription_id)
    clonedDetails = []
    print('before cloning loop 12')
    for detail in details:
        detail.pk = None
        detail.prescription = src
        clonedDetails.append(detail)
        print('detail', detail)
    print('clonedDetail', clonedDetails)
    PrescriptionDetail.objects.bulk_create(clonedDetails)

def cloneMedicalInstruction(instruction: int, clonedHealthRecord: HealthRecord):
    src: MedicalInstruction = MedicalInstruction.objects.filter(pk = instruction).first()
    if src is None:
        raise CustomValidationError(message='Not Found', detail='Not found medical instruction', code = 400) 
    src.healthRecord = clonedHealthRecord
    src.pk = None
    src.save()
    return src

def cloneInstruction2(instructions:list[dict], clonedHealthRecord: HealthRecord):
    print('before cloning loop 6')
    # src: Prescription = Prescription.objects.filter(pk=prescription_id).first()
    # src.healthRecord = clonedHealthRecord
    # src.pk = None
    # src.save()
    # details = PrescriptionDetail.objects.filter(prescription__pk=prescription_id)
    data = []
    for instruct in instructions:
        category = instruct.pop('category')
        data.append(
                MedicalInstruction(
                **instruct, 
                category_id = category, 
                healthRecord = clonedHealthRecord, 
                patient = clonedHealthRecord.patient)
        )
    MedicalInstruction.objects.bulk_create(data)