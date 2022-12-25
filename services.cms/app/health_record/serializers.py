from rest_framework import serializers
from medicine.models import Medicine
from instruction.serializers import ReadOnlyMedicalInstructionSerializer
from instruction.serializers import HealthRecordInstructionSerializer
from instruction.models import MedicalInstruction, MedicalInstructionStatus
from shared.utils import to_json, from_json
from instruction.serializers import ReadOnlyDoctorMedicalInstructionSerializer
from prescription.models import Prescription, PrescriptionDetail
from prescription.serializers import ReadOnlyPrescriptionSerializer2, PrescriptionDetailReadOnlySerializer
from disease.serializers import DiagnoseSerializer
from health_record.models import HealthRecord
from shared.exceptions import CustomValidationError
from shared.response_messages import ResponseMessage
from django.db import transaction
from patient.models import Patient
from user.models import User
from doctor.models import Doctor
from disease.models import Disease
from treatment.models import TreatmentContract
from myapp.settings import DOB_FORMAT
import logging, uuid
logger = logging.getLogger(__name__)

def _get_prescription_details(record: HealthRecord):
    try:
        prescription = record.prescription_set.all()[0]
    except:
        prescription = None
        
    return PrescriptionDetailReadOnlySerializer(prescription.prescriptiondetail_set.all(), many = True).data\
        if prescription\
        else []

class PatientMedicalHistorySerializer(serializers.Serializer):
    socialHistory = serializers.JSONField(required = False)
    historyOfPresentIllness = serializers.JSONField(required = False)
    medicationHistory = serializers.JSONField(required = False)
    allergies = serializers.JSONField(required = False)
    def to_representation(self, instance):
        return {
            "historyOfPresentIllness": instance.historyOfPresentIllness,
            "socialHistory": instance.socialHistory,
            "medicationHistory": instance.medicationHistory,
            "allergies": instance.allergies
        }

class DetailSerializer(serializers.Serializer):
    medicine = serializers.IntegerField(min_value = 1)
    quantity = serializers.IntegerField(min_value = 1)
    unit = serializers.CharField(max_length = 255)
    guide = serializers.CharField(max_length = 500)
    
    class Meta:
        fields = ['medicine', 'quantity', 'unit', 'guide']

class HrDetailSerializer(serializers.Serializer):
    name = serializers.CharField(max_length = 200, required = False)
    pathologies = serializers.ListField(
        allow_empty = True,
        required = False,
        child = serializers.IntegerField(min_value = 1)
    )
    
    class NestedInstructionSerializer(serializers.Serializer):
        category = serializers.IntegerField(min_value = 1)
        requirments = serializers.CharField(max_length = 1000)
        submissions = serializers.CharField(max_length = 1000, allow_blank = True)
        
        class Meta:
            fields = ['category', 'requirments', 'submissions']
    instructions = NestedInstructionSerializer(many = True)
    
    allergies = serializers.ListField(
        allow_empty = True,
        required = False,
        child = serializers.CharField(max_length = 255),
    )
    
    socialHistory = serializers.ListField(
        allow_empty = True,
        required = False,
        child = serializers.CharField(max_length = 255),
    )
    
    diseases = serializers.ListField(
        allow_empty = False,
        required = False,
        child = serializers.IntegerField(min_value = 1),
    )

    # prescriptions
    class NestedPrescriptionsSerializer(serializers.Serializer):
        note = serializers.CharField(max_length = 200)
        fromDate = serializers.DateField()
        toDate = serializers.DateField()
        detail = DetailSerializer(many = True)
        
        def validate_detail(self, detail):
            medicine_ids = list(( item.get('medicine') for item in detail ))
            results = Medicine.objects.filter(pk__in = medicine_ids)
            if results.count() != len(medicine_ids):
                raise CustomValidationError(message = ResponseMessage.INVALID_ID, detail = { 'detail': { 'medicine': 'Invalid id' } })
            
            return detail
        
        class Meta:
            fields = ['note', 'fromDate', 'toDate', 'detail']

    prescriptions = serializers.ListField(
        child = NestedPrescriptionsSerializer()
    )
    
    def validate_pathologies(self, data):
        results = Disease.objects.filter(pk__in = data)
        if results.count() != len(data):
            raise CustomValidationError(message = ResponseMessage.INVALID_ID, detail = {'pathologies': 'Invalid input data'})

        return list(results)
    
    def validate_diseases(self, data):
        results = Disease.objects.filter(pk__in = data)
        if results.count() != len(data):
            raise CustomValidationError(message = ResponseMessage.INVALID_ID, detail = {'diseases': 'Invalid input data'})

        return list(results)
    
    class Meta:
        fields = ['name', 'allergies', 'socialHistory', 'pathologies', 'diseases', 'prescriptions', 'instructions']

class DoctorHealthRecordSerializer(serializers.Serializer):
    patient = serializers.IntegerField(min_value = 1)
    detail = HrDetailSerializer()
    contract = serializers.IntegerField(min_value = 1, required = False)
    _valid_fields = ('name', 'allergies', 'socialHistory', 'pathologies', 'diseases', 'prescriptions', 'instructions')
    
    def validate_patient(self, patient_id: int):
        logger.info('DoctorHealthRecordSerializer.validate_patient invoked')
        try:
            patient = Patient.objects.select_related('supervisor').get(pk = patient_id)
        except:
            raise CustomValidationError(message = ResponseMessage.NOT_FOUND, detail = {'patient': f'Patient with id {patient_id} not found'})
        
        return patient
        
    def validate_contract(self, contract_id):
        try:
            return TreatmentContract.objects.get(pk = contract_id)
        except:
            raise CustomValidationError(message = ResponseMessage.NOT_FOUND, detail = {})
    
    def create(self, validated_data):
        logger.info('Creating health record by doctor...')
        detail: dict = validated_data['detail'] # OrderedDict
        pathologies: list[Disease] = detail.get('pathologies') or []
        diseases: list[Disease] = detail.get('diseases') or []
        allergies = detail.get('allergies') or []
        socialHistory = detail.get('socialHistory') or []
        prescriptions = detail.get('prescriptions') or []
        instructions = detail.get('instructions') or []
        
        dt = dict() # dict
        dt['pathologies'] = list(( patho.to_dict() for patho in pathologies ))
        dt['diseases'] = list(( disease.to_dict() for disease in diseases ))
        dt['allergies'] = allergies
        dt['socialHistory'] = socialHistory
        # dt['prescriptions'] = prescriptions
        
        doctor_account: User = self.context.get('user', None)
        patient: Patient = validated_data['patient']
        health_record = HealthRecord(
            patient = patient, 
            doctor = doctor_account.doctor,
            isPatientProvided = False,
        )
        
        # Xử lí instructions
        logger.info('Processing instructions...')
        inst_to_db = []
        for item in instructions:
            inst_to_db.append(
                MedicalInstruction(
                    category_id = item.get('category'),
                    requirments = item.get('requirments'),
                    status = MedicalInstructionStatus.PENDING,
                    healthRecord = health_record,
                    patient = patient,
                )
            )
        
        # Xử lí prescriptions
        logger.info('----- Process Prescriptions -----')
        try:
            d_prescription = prescriptions[0]
        except:
            pass
        presc = Prescription(
            healthRecord = health_record,
            fromDate = d_prescription.get('fromDate'),
            toDate = d_prescription.get('toDate'),
            note = d_prescription.get('note'),
            
        )
        
        logger.info('----- Process Prescriptions Detail -----')
        pre_details = []
        for item in d_prescription.get('detail'):
            pre_details.append(
                PrescriptionDetail(
                    prescription = presc,
                    medicine_id = item.get('medicine'),
                    quantity = item.get('quantity'),
                    unit = item.get('unit'),
                    guide = item.get('guide')
                )
            )
        
        health_record.detail = dt
        health_record.save()
        MedicalInstruction.objects.bulk_create(inst_to_db)
        presc.save()
        PrescriptionDetail.objects.bulk_create(pre_details)
        logger.info('Creating health record success')
        return health_record
    
    def to_representation(self, instance: HealthRecord):
        patient: Patient = instance.patient
        supervisor: User = patient.supervisor
        prescriptions = PrescriptionDetail.objects\
            .select_related('medicine', 'prescription')\
            .filter(
                prescription__healthRecord_id = instance.pk
            )
        instance.detail['prescriptions'] = PrescriptionDetailReadOnlySerializer(prescriptions, many = True).data
        instance.detail['instructions'] = ReadOnlyMedicalInstructionSerializer(instance.medical_instructions.all(), many = True).data
        return {
            'record': {
                'id': instance.id,
                'createdAt': instance.createdAt.strftime(DOB_FORMAT) if instance.createdAt else None,
                'startedAt': instance.startedAt,
                'isPatientProvided': instance.isPatientProvided,
                'name': instance.name,
            },
            'patient': {
                'id': patient.id,
                'firstName': patient.firstName,
                'lastName': patient.lastName,
                'gender': patient.gender,
                'age': patient.age,
                'avatar': patient.avatar,
                'address': patient.address,
            },
            'doctor': {
                'id': instance.doctor_id,
                'firstName': instance.doctor.firstName,
                'lastName': instance.doctor.lastName,
                'experienceYears': instance.doctor.experienceYears
            },
            'supervisor': {
                'id': supervisor.id,
                'email': supervisor.email,
                'firstName': supervisor.firstName,
                'lastName': supervisor.lastName,
                'phoneNumber': supervisor.phoneNumber,
                'avatar': supervisor.avatar,
            },
            'isPatientProvided': instance.isPatientProvided,
            'detail': instance.detail,
        }

    class Meta:
        fields = ['patient', 'detail', 'contract']
        

class SupervisorHealthRecordSerializer(serializers.Serializer):
    patient = serializers.IntegerField(min_value = 1)
    detail = HrDetailSerializer()
    _valid_fields = ('name', 'allergies', 'socialHistory', 'pathologies', 'diseases', 'prescriptions', 'instructions')
    
    def validate_patient(self, patient_id: int):
        logger.info('DoctorHealthRecordSerializer.validate_patient invoked')
        supervisor: User = self.context.get('user')
        try:
            patient = Patient.objects\
                .select_related('supervisor')\
                .get(pk = patient_id, supervisor_id = supervisor.id)
        except:
            raise CustomValidationError(message = ResponseMessage.NOT_FOUND, detail = {'patient': f'Patient with id {patient_id} not found'})
        
        return patient
    
    @transaction.atomic
    def create(self, validated_data):
        logger.info('SupervisorHealthRecordSerializer creating data...')
        patient: Patient = validated_data['patient']
        detail = validated_data['detail']
        name = detail.get('name')
        pathologies: list[Disease] = detail.get('pathologies')
        instructions: list[dict] = detail.get('instructions')
        
        health_record = HealthRecord(
            name = name,
            isPatientProvided = True,
            patient = patient,
        )
        dt = dict()
        # Xử lí bệnh lý
        dt['pathologies'] = list(( patho.to_dict() for patho in pathologies ))
        dt['allergies'] = list()
        dt['socialHistory'] = list()
        dt['diseases'] = list()
        dt['prescriptions'] = list()
        
        # Xử lí instructions
        inst_to_db = []
        for item in instructions:
            inst_to_db.append(
                MedicalInstruction(
                    category_id = item.get('category'),
                    requirments = item.get('requirments'),
                    submissions = item.get('submissions'),
                    status = MedicalInstructionStatus.COMPLETED,
                    healthRecord = health_record,
                    patient = patient,
                )
            )
        
        health_record.detail = dt
        logger.info('Saving health record data to database...')
        health_record.save()
        MedicalInstruction.objects.bulk_create(inst_to_db)
        
        logger.info('SupervisorHealthRecordSerializer created data succeeded')
        return health_record
    
    def to_representation(self, instance: HealthRecord):
        logger.info('SupervisorHealthRecordSerializer deserialize data to dict')
        patient: Patient = instance.patient
        supervisor: User = patient.supervisor
        doctor: Doctor = instance.doctor

        try:
            prescription = instance.prescription_set.all()[0]
            pre_details = prescription.prescriptiondetail_set.all()
            
        except:
            prescription = None
        
        instance.detail['instructions'] = ReadOnlyMedicalInstructionSerializer(instance.medical_instructions.all(), many = True).data
        if prescription:
            instance.detail['prescriptions'] = PrescriptionDetailReadOnlySerializer(pre_details, many = True).data
        else:
            instance.detail['prescriptions'] = []
        return {
            'record': {
                'id': instance.id,
                'createdAt': instance.createdAt.strftime(DOB_FORMAT),
                'startedAt': instance.startedAt.strftime(DOB_FORMAT),
                'isPatientProvided': instance.isPatientProvided,
                'name': instance.name,
            },
            'patient': {
                'id': patient.id,
                'firstName': patient.firstName,
                'lastName': patient.lastName,
                'gender': patient.gender,
                'age': patient.age,
                'avatar': patient.avatar,
                'address': patient.address,
            },
            'supervisor': {
                'id': supervisor.id,
                'email': supervisor.email,
                'firstName': supervisor.firstName,
                'lastName': supervisor.lastName,
                'phoneNumber': supervisor.phoneNumber,
                'avatar': supervisor.avatar,
            },
            'doctor': {
                'id': doctor.pk,
                'firstName': doctor.firstName,
                'lastName': doctor.lastName,
                'email': doctor.email
            } if doctor else None,
            'detail': instance.detail,
        }
    
    class Meta:
        fields = ['patient', 'detail']
        
class ListRecordSerializer(serializers.BaseSerializer):
    
    def to_representation(self, instance: HealthRecord):
        logger.info('ListRecordSerializer deserialize data to dict')
        patient: Patient = instance.patient
        supervisor: User = patient.supervisor
        doctor: Doctor = instance.doctor
        return {
            'record': {
                'id': instance.id,
                'createdAt': instance.createdAt.strftime(DOB_FORMAT),
                'startedAt': instance.startedAt,
                'isPatientProvided': instance.isPatientProvided,
                'name': instance.name,
            },
            'doctor': {
                'id': doctor.pk,
                'firstName': doctor.firstName,
                'lastName': doctor.lastName,
                'avatar': doctor.avatar,
            } if doctor else None,
            'patient': {
                'id': patient.id,
                'firstName': patient.firstName,
                'lastName': patient.lastName,
                'gender': patient.gender,
                'age': patient.age,
                'avatar': patient.avatar,
                'address': patient.address,
            },
            'supervisor': {
                'id': supervisor.id,
                'email': supervisor.email,
                'firstName': supervisor.firstName,
                'lastName': supervisor.lastName,
                'phoneNumber': supervisor.phoneNumber,
                'avatar': supervisor.avatar,    
            },
            'detail': from_json(instance.detail)
            # 'detail': instance.detail
        }
    
class ReadOnlyHealthRecordSerializer(serializers.BaseSerializer):
    
    def to_representation(self, instance: HealthRecord):
        patient: Patient = instance.patient
        supervisor: User = patient.supervisor
        doctor: Doctor = instance.doctor
        
        prescriptions = _get_prescription_details(instance)
        instructions = ReadOnlyMedicalInstructionSerializer(instance = instance.medical_instructions.all(), many = True).data

        instance.detail['prescriptions'] = prescriptions
        instance.detail['instructions'] = instructions
        logger.info(f'Get health record {instance} succeeded')
        return {
            'record': {
                'id': instance.id,
                'createdAt': instance.createdAt.strftime(DOB_FORMAT),
                'startedAt': instance.startedAt,
                'isPatientProvided': instance.isPatientProvided,
                'name': instance.name,
            },
            'patient': {
                'id': patient.id,
                'firstName': patient.firstName,
                'lastName': patient.lastName,
                'dob': patient.dob.strftime(DOB_FORMAT) if patient.dob else None,
                'avatar': patient.avatar,
                'age': patient.age,
                'gender': patient.gender
            },
            'supervisor': {
                'id': patient.supervisor_id,
                'firstName': supervisor.firstName,
                'lastName': supervisor.lastName,
                'phoneNumber': supervisor.phoneNumber,
                'email': supervisor.email
            },
            'doctor': {
                'id': doctor.id,
                'firstName': doctor.firstName,
                'lastName': doctor.lastName,
                'email': doctor.email,
            } if doctor else None,
            'detail': instance.detail
        }

class ReadOnlyHealthRecordSerializer2(serializers.BaseSerializer):
    
    def to_representation(self, instance: HealthRecord):
        patient: Patient = instance.patient
        supervisor: User = patient.supervisor
        doctor: Doctor = instance.doctor
        prescriptionsSerializer = ReadOnlyPrescriptionSerializer2(instance = instance.prescription_set.all(), many = True)
        instruction = ReadOnlyDoctorMedicalInstructionSerializer(instance = instance.medical_instructions.all(), many = True)

        return {
            'record': {
                'id': instance.pk,
                'createdAt': instance.createdAt.strftime(DOB_FORMAT),
                'updatedAt': instance.createdAt.strftime(DOB_FORMAT),
                'isPatientProvided': instance.isPatientProvided,
            },
            'patient': {
                'id': patient.id,
                'firstName': patient.firstName,
                'lastName': patient.lastName,
                'dob': patient.dob.strftime(DOB_FORMAT) if patient.dob else None,
                'avatar': patient.avatar,
                'age': patient.age,
                'gender': patient.gender,
                'address': patient.address,
            },
            'supervisor': {
                'id': patient.supervisor_id,
                'firstName': supervisor.firstName,
                'lastName': supervisor.lastName,
                'phoneNumber': supervisor.phoneNumber,
                'email': supervisor.email,
                'avatar': supervisor.avatar,
            },
            'doctor': {
                'id': doctor.id,
                'firstName': doctor.firstName,
                'lastName': doctor.lastName,
                'email': doctor.email,
                'avatar': doctor.avatar,
            } if doctor else None,
            'prescriptions': prescriptionsSerializer.data,
            'instructions': instruction.data,
            'detail': from_json(instance.detail)
        }

class DoctorHealthRecordSerializer2(serializers.Serializer):
    diagnosis = DiagnoseSerializer(many=True)

class ReadOnlyHealthRecordSerializer3(serializers.BaseSerializer):
    
    def to_representation(self, instance: HealthRecord):
        if instance.contract_id:
            return

        patient: Patient = instance.patient
        supervisor: User = patient.supervisor
        doctor: Doctor = instance.doctor
            
        instance.detail['prescriptions'] = _get_prescription_details(instance)
        instance.detail['instructions'] = ReadOnlyDoctorMedicalInstructionSerializer(instance = instance.medical_instructions.all(), many = True).data
        return {
            'record': {
                'id': instance.pk,
                'createdAt': instance.createdAt.strftime(DOB_FORMAT),
                'updatedAt': instance.createdAt.strftime(DOB_FORMAT),
                'isPatientProvided': instance.isPatientProvided,
                'name': instance.name,
            },
            'patient': {
                'id': patient.id,
                'firstName': patient.firstName,
                'lastName': patient.lastName,
                'dob': patient.dob.strftime(DOB_FORMAT) if patient.dob else None,
                'avatar': patient.avatar,
                'age': patient.age,
                'gender': patient.gender
            },
            'supervisor': {
                'id': patient.supervisor_id,
                'firstName': supervisor.firstName,
                'lastName': supervisor.lastName,
                'phoneNumber': supervisor.phoneNumber,
                'email': supervisor.email
            },
            'doctor': {
                'id': doctor.id,
                'firstName': doctor.firstName,
                'lastName': doctor.lastName,
                'email': doctor.email,
                'avatar': doctor.avatar,
            } if doctor else None,
            'detail': instance.detail
        }
