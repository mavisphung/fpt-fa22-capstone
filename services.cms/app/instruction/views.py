from rest_framework.generics import CreateAPIView,ListAPIView, UpdateAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import permissions
from instruction.models import MedicalInstruction, MedicalInstructionCategory
from instruction.serializers import (
    InstructionCateSerializer, 
    ReadOnlyDoctorMedicalInstructionSerializer, 
    CreateInstructionSerializer, 
    UpdateMedicalInstructionSerializer
)
from shared.app_permissions import IsDoctor, IsSupervisor
from shared.exceptions import CustomValidationError
from shared.utils import get_page_limit_from_request, get_paginated_response
from shared.formatter import format_response


class DoctorListHealthRecordMedicalInstructionView(ListAPIView):
    permission_classes = [IsDoctor]
    serializer_class = ReadOnlyDoctorMedicalInstructionSerializer
    queryset = MedicalInstruction.objects.select_related('healthRecord').all()
    def list(self, request, *args, **kwargs):
        record_id = kwargs.pop('healthrecord', None)
        page = kwargs.pop('page', None)
        queryset = self.get_queryset().filter(healthRecord__pk = record_id)
        print(queryset)
        return get_paginated_response(queryset,page,10,self.get_serializer_class())
    
class SupervisorListHealthRecordMedicalInstructionView(ListAPIView):
    permission_classes = [IsSupervisor]
    serializer_class = ReadOnlyDoctorMedicalInstructionSerializer
    queryset = MedicalInstruction.objects.select_related('healthRecord').all()
    def list(self, request:Request, *args, **kwargs):
        record_id = kwargs.pop('record_id', None)
        user = request.user
        page = kwargs.pop('page', None)
        queryset = self.get_queryset().filter(healthRecord__pk = record_id, healthRecord__supervisor = user)
        return get_paginated_response(queryset, page, 10, self.get_serializer_class())

class CreateMedicalInsturctionView(CreateAPIView):
    serializer_class = CreateInstructionSerializer
    permission_classes = [IsDoctor]
    def create(self, request:Request, *args, **kwargs):
        data = request.data.copy()
        serializer: CreateInstructionSerializer= self.get_serializer(data = data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        response = format_response(success=True, message='SUCCESS',status = 201, data=serializer.data)  
        return Response(data = response, status=response['status'])

class UpdateMedicalInstructionView(UpdateAPIView):
    serializer_class = UpdateMedicalInstructionSerializer
    permission_classes = [IsDoctor]
    queryset = MedicalInstruction.objects.all()
    def update(self, request, *args, **kwargs):
        data = request.data
        id = data.get('id', None)
        action  = data.get('action', None)
        instance = self.get_queryset().filter(pk = id).first()
        if instance is None:
            raise CustomValidationError(message= 'Instruction Not found', detail=f'Not found medical instruction with id: {id}' , code= 404)
        serializer: UpdateMedicalInstructionSerializer= self.get_serializer(instance = instance, data = {'submissions': data['submissions']},context = {
            'action': action
        })
        serializer.is_valid(raise_exception = True)
        serializer.save()
        response = format_response(success = True, data = serializer.data, status = 200, message = 'update success')
        return Response(data = response, status=response['status'])

class ListInstCategoryView(ListAPIView):
    
    serializer_class = InstructionCateSerializer
    permission_classes = [permissions.AllowAny]
    
    def list(self, request: Request, *args, **kwargs):
        
        page, limit = get_page_limit_from_request(request)
        queryset = MedicalInstructionCategory.objects.all()
        
        return get_paginated_response(queryset, page, limit, self.get_serializer_class())