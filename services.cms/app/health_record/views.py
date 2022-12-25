from rest_framework import generics, permissions
from rest_framework.request import Request
from rest_framework.response import Response
from instruction.models import MedicalInstruction
from medicine.models import Medicine
from prescription.models import Prescription, PrescriptionDetail
from patient.models import Patient
from shared.app_permissions import IsDoctor, IsSupervisor
from shared.formatter import format_response
from shared.paginations import get_paginated_response
from shared.utils import get_page_limit_from_request, database_debug
from shared.exceptions import CustomValidationError
from shared.response_messages import ResponseMessage
from health_record.serializers import (
    DoctorHealthRecordSerializer,
    ListRecordSerializer,
    ReadOnlyHealthRecordSerializer,
    ReadOnlyHealthRecordSerializer2,
    ReadOnlyHealthRecordSerializer3,
    SupervisorHealthRecordSerializer
)
from health_record.models import HealthRecord
from django.db.models import Prefetch, F
from user.models import User
from django.db import transaction
import logging
logger = logging.getLogger(__name__)

# Create your views here.


class DoctorCreateHealthRecordView(generics.CreateAPIView):
    """
    Doctor create health record for patient
    """
    permission_classes = [IsDoctor]
    serializer_class = DoctorHealthRecordSerializer

    @transaction.atomic
    def create(self, request: Request, *args, **kwargs):
        """
        Request body contains:
        - doctorId who has logged in before
        - patientId who the doctor picked. Maybe from contract. Define later
        """
        serializer: DoctorHealthRecordSerializer = self.get_serializer(data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        response = format_response(
            success=True,
            status=201,
            message=ResponseMessage.RECORD_CREATED_SUCCEEDED,
            data=serializer.data
        )

        return Response(response, response['status'])

class SupervisorListCreateHealthRecordView(generics.ListCreateAPIView):
    permission_classes = [IsSupervisor]
    serializer_class = SupervisorHealthRecordSerializer

    def list2(self, request: Request, *args, **kwargs):
        supervisor: User = request.user
        page, limit = get_page_limit_from_request(request)
        data = HealthRecord.objects\
            .select_related('patient', 'doctor')\
            .filter(
                patient__supervisor_id = supervisor.id,
                isPatientProvided = True
            )
        response: Response = get_paginated_response(data, page, limit, self.get_serializer_class())
        return response
    
    # @database_debug
    def list(self, request: Request, *args, **kwargs):
        supervisor: User = request.user
        patient_id = request.query_params.get('patientId') or -1
        page, limit = get_page_limit_from_request(request)
        
        # found: Patient = Patient.objects\
        #     .prefetch_related(
        #         Prefetch(
        #             'health_records',
        #             HealthRecord.objects\
        #                 .prefetch_related(
        #                     Prefetch(
        #                         lookup='prescription_set',
        #                         queryset = Prescription.objects\
        #                             .prefetch_related(
        #                                 Prefetch(
        #                                     lookup = 'prescriptiondetail_set',
        #                                     queryset = PrescriptionDetail.objects.select_related('medicine').filter(prescription__healthRecord_id=F('pk'))
        #                                 )
        #                             )\
        #                             .filter(healthRecord_id = F('pk'))
        #                     ),
        #                     Prefetch(
        #                         lookup='patient',
        #                         queryset=Patient.objects.select_related('supervisor')
        #                     ),
        #                     Prefetch(
        #                         lookup='medical_instructions',
        #                         queryset=MedicalInstruction.objects.filter(healthRecord__pk = F('pk'))
        #                     )
        #                 )\
        #                 .select_related('patient', 'doctor')
        #         )
        #     )\
        #     .get(
        #         pk = patient_id,
        #         supervisor_id = supervisor.pk
        #     )
        
        queryset = HealthRecord.objects\
            .prefetch_related(
                'prescription_set',
                Prefetch(
                    lookup = 'prescription_set__prescriptiondetail_set',
                    queryset = PrescriptionDetail.objects.select_related('medicine')
                ),
                Prefetch(
                    lookup = 'medical_instructions',
                    queryset = MedicalInstruction.objects.select_related('category')
                ),
                Prefetch(
                    lookup = 'patient',
                    queryset = Patient.objects.select_related('supervisor')
                )
            )\
            .select_related('doctor')\
            .filter(
                patient_id = patient_id,
                patient__supervisor_id = supervisor.id
            )
        # return get_paginated_response(found.health_records.all(), page, limit, ReadOnlyHealthRecordSerializer2)
        return get_paginated_response(queryset, page, limit, SupervisorHealthRecordSerializer)

    @transaction.atomic
    def create(self, request: Request, *args, **kwargs):
        serializer: SupervisorHealthRecordSerializer = self.get_serializer(data = request.data, context = { 'user': request.user })
        serializer.is_valid(raise_exception = True)
        serializer.save()

        response = format_response(
            success = True,
            status = 201,
            message = ResponseMessage.RECORD_CREATED_SUCCEEDED,
            data = serializer.data
        )

        return Response(response, response['status'])


class GetHealthRecordView(generics.RetrieveAPIView):
    """
    Get health record api
    """
    # permission_classes = [IsSupervisor]
    serializer_class = ReadOnlyHealthRecordSerializer
    queryset = HealthRecord.objects.all()

    @database_debug
    def retrieve(self, request, *args, **kwargs):
        pk = int(kwargs.get('pk', None)) or 0
        print('Querying data ---------------------------------------------------------------')
        health_record: HealthRecord = HealthRecord.objects\
            .prefetch_related(
                'prescription_set',
                Prefetch(
                    lookup = 'prescription_set__prescriptiondetail_set',
                    queryset = PrescriptionDetail.objects.select_related('medicine')
                ),
                Prefetch(
                    lookup = 'medical_instructions',
                    queryset = MedicalInstruction.objects.select_related('category')
                ),
                Prefetch(
                    lookup = 'patient',
                    queryset = Patient.objects.select_related('supervisor')
                )
            )\
            .select_related('doctor')\
            .filter(pk=pk)\
            .first()

        if not health_record:
            raise CustomValidationError(message=ResponseMessage.NOT_FOUND, detail={
                                        'healthRecord': f'There is no health record with id {pk}'})

        health_record.prescription_details = PrescriptionDetail.objects.select_related('medicine').filter(prescription__healthRecord_id = health_record.pk)
        
        serializer: ReadOnlyHealthRecordSerializer = self.get_serializer(
            instance=health_record)

        response = format_response(
            success=True,
            message=ResponseMessage.GET_DATA_SUCCEEDED,
            data=serializer.data
        )

        return Response(response, response['status'])


class DoctorListHealthRecordByContractView(generics.RetrieveAPIView):
    """
    Get health record api
    """
    # permission_classes = [IsSupervisor]
    serializer_class = ReadOnlyHealthRecordSerializer

    def retrieve(self, request, *args, **kwargs):
        contract_id = kwargs.pop('contract', None)
        # health_records = HealthRecord.objects.prefetch_related('patient_medical_history','prescription_set','medical_instructions').select_related('doctor','patient').filter(contract__pk=contract_id)
        health_records: HealthRecord = HealthRecord.objects\
            .prefetch_related(
                'prescription_set',
                Prefetch(
                    lookup = 'prescription_set__prescriptiondetail_set',
                    queryset = PrescriptionDetail.objects.select_related('medicine')
                ),
                Prefetch(
                    lookup = 'medical_instructions',
                    queryset = MedicalInstruction.objects.select_related('category')
                ),
                Prefetch(
                    lookup = 'patient',
                    queryset = Patient.objects.select_related('supervisor')
                )
            )\
            .filter(contract__pk=contract_id)
        serializer: ReadOnlyHealthRecordSerializer = self.get_serializer(
            instance = health_records, 
            many = True
        )
        response = format_response(
            success = True,
            message = ResponseMessage.GET_DATA_SUCCEEDED,
            data = serializer.data
        )
        return Response(response, response['status'])

class ListAllHealthRecordView(generics.ListAPIView):
    
    permission_classes = [permissions.AllowAny]
    
    def list(self, request, *args, **kwargs):
        queryset = HealthRecord.objects\
            .prefetch_related(
                'prescription_set',
                Prefetch(
                    lookup = 'prescription_set__prescriptiondetail_set',
                    queryset = PrescriptionDetail.objects.select_related('medicine')
                ),
                Prefetch(
                    lookup = 'medical_instructions',
                    queryset = MedicalInstruction.objects.select_related('category')
                ),
                Prefetch(
                    lookup = 'patient',
                    queryset = Patient.objects.select_related('supervisor')
                )
            )\
            .select_related('doctor')\
            .all()
        serializer = ReadOnlyHealthRecordSerializer3(queryset, many = True)
        # response = format_response(message = ResponseMessage.GET_DATA_SUCCEEDED, data = serializer.data)
        return Response(serializer.data)
        
