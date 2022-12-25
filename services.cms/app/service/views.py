from rest_framework import generics, permissions
from shared.app_permissions import IsDoctor, IsManager
from rest_framework.request import Request
from rest_framework.response import Response
from service.models import DoctorService, Service
from service.serializers import ReadOnlyServiceSerializer, ServiceSerializer
from shared.utils import (
    get_page_limit_from_request, 
    get_paginated_response,
)
from shared.formatter import format_response
from shared.response_messages import ResponseMessage
from django.db import transaction
from django.db.models import Prefetch, Q
from django.http import Http404

import logging
logger = logging.getLogger(__name__)
class ListServiceView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ReadOnlyServiceSerializer
    
    def list(self, request: Request, *args, **kwargs):
        page, limit = get_page_limit_from_request(request)
        queryset = Service.objects.filter(is_deleted = False)
        response = get_paginated_response(queryset, page, limit, self.get_serializer_class())
        return response

class ManagerCreateServiceView(generics.CreateAPIView):
    permission_classes = [IsManager]
    serializer_class = ServiceSerializer
    
    @transaction.atomic
    def create(self, request: Request, *args, **kwargs):
        serializer: ServiceSerializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        response = format_response(
            success = True,
            status = 201,
            message = ResponseMessage.SERVICE_CREATE_SUCCEEDED,
            data = serializer.data
        )
        return Response(response, status = response['status'])
    
class ManagerRetrieveUpdateDestroyServiceView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsManager]
    serializer_class = ServiceSerializer
    
    def _get_object(self, service_id: int) -> Service:
        service = Service.objects.filter(id = service_id, is_deleted = False).first()
        if not service:
            raise Http404()
        return service
    
    # @transaction.atomic
    def retrieve(self, request: Request, *args, **kwargs):
        pk = kwargs.pop('pk')
        found = self._get_object(pk)
        serializer = ReadOnlyServiceSerializer(found)
        response = format_response(
            success = True,
            status = 200,
            message = ResponseMessage.GET_DATA_SUCCEEDED,
            data = serializer.data
        )
        return Response(response, status = response['status'])
    
    @transaction.atomic
    def update(self, request: Request, *args, **kwargs):
        pk = kwargs.pop('pk')
        found = self._get_object(pk)
        serializer: ServiceSerializer = self.get_serializer(instance = found, data = request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        response = format_response(
            success = True,
            status = 202,
            message = ResponseMessage.SERVICE_UPDATE_SUCCEEDED,
            data = serializer.data
        )
        return Response(response, status = response['status'])
    
    @transaction.atomic
    def destroy(self, request: Request, *args, **kwargs):
        pk = kwargs.pop('pk')
        found = self._get_object(pk)
        update_fields = ['updatedAt', 'is_deleted']
        found.is_deleted = not found.is_deleted
        found.save(update_fields = update_fields)
        return Response(status = 204)
    
class SearchServiceView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    
    def list(self, request: Request, *args, **kwargs):
        q = request.query_params.get('q') or ''
        page, limit = get_page_limit_from_request(request)
        queryset = Service.objects.filter(Q(name__icontains = q))
        return get_paginated_response(queryset, page, limit, ReadOnlyServiceSerializer)

class ManagerRemoveDoctorServiceView(generics.DestroyAPIView):
    
    permission_classes = [IsManager]
    
    @transaction.atomic
    def destroy(self, request: Request, *args, **kwargs):
        doctor_id = kwargs.get('doctor_id')
        service_id = kwargs.get('service_id')
        obj = DoctorService.objects.get(doctor_id = doctor_id, service_id = service_id)
        obj.delete()
        return Response(status = 204)