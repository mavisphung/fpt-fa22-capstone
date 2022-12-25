from rest_framework.response import Response
from rest_framework.request import Request
from user.models import User
from shared.formatter import format_response
from shared.response_messages import ResponseMessage
from shared.app_permissions import IsSupervisor
from shared.utils import get_page_limit_from_request, get_paginated_response
from django.db import transaction
from rest_framework import generics
from patient.models import Patient

from patient.serializers import PatientSerializer, UpdatePatientSerializer

# Create your views here.
class PatientProfileView(generics.CreateAPIView,
                         generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PatientSerializer
    queryset = Patient.objects.all()
    
    def create(self, request: Request, *args, **kwargs):
        serializer: PatientSerializer = self.get_serializer(data = request.data, context = { 'user': request.user })
        serializer.is_valid(raise_exception = True)
        serializer.save()
        
        response = format_response(
            success = True,
            status = 201,
            message = ResponseMessage.PATIENT_CREATED_SUCCEED,
            data = serializer.data
        )
        
        return Response(response, response['status'])

    def retrieve(self, request, *args, **kwargs):
        patient: Patient = self.get_object()
        serializer = self.get_serializer(patient)
        
        response = format_response(
            success = True,
            status = 200,
            message = ResponseMessage.PATIENT_GET_SUCCEED,
            data = serializer.data
        )
        
        return Response(response, response['status'])
    
    def update(self, request, *args, **kwargs):
        patient: Patient = self.get_object()
        serializer = self.get_serializer(instance = patient, data = request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        
        response = format_response(
            success = True,
            status = 202,
            message = ResponseMessage.PATIENT_UPDATED_SUCCEED,
            data = serializer.data
        )
        
        return Response(response, response['status'])
    
    @transaction.atomic
    def perform_destroy(self, instance: Patient):
        user: User = self.request.user
        try:
            user.patient_profiles.remove(instance) # Disassociate
        except:
            pass
        return instance
    
    def destroy(self, request, *args, **kwargs):
        patient: Patient = self.get_object()
        updated_instance = self.perform_destroy(patient)
        serializer: PatientSerializer = self.get_serializer(updated_instance)
        
        response = format_response(
            success = True,
            status = 202,
            message = ResponseMessage.PATIENT_DISCARD_SUCCEED,
            data = serializer.data
        )
        
        return Response(response, response['status'])

class ListUserPatientView(generics.ListAPIView):
    permission_classes = [IsSupervisor]
    serializer_class = PatientSerializer
    
    def list(self, request: Request, *args, **kwargs):
        
        page, limit = get_page_limit_from_request(request)
        supervisor: User = request.user
        queryset = Patient.objects.select_related('supervisor').filter(supervisor_id = supervisor.pk)
        
        response = get_paginated_response(queryset, page, limit, self.get_serializer_class())
        
        return response