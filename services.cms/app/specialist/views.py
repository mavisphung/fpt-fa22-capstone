from rest_framework import generics, permissions
from rest_framework.decorators import api_view, permission_classes 
from rest_framework.response import Response
from rest_framework.request import Request
from asgiref.sync import sync_to_async, async_to_sync
from django.db.models import Prefetch, F
from user.models import User
from doctor.models import Doctor

from specialist.models import Specialist, DoctorSpecialist
from specialist.serializers import (
    ReadOnlyDoctorSpecialistSerializer, 
    ReadOnlyHomeSpecialistSerializer, 
    ReadOnlySpecialistSerializer
)
from shared.response_messages import ResponseMessage
from shared.formatter import format_response
from shared.utils import get_paginated_response, get_page_limit_from_request
from shared.app_permissions import IsDoctor, IsSupervisor
from shared.exceptions import CustomValidationError

import logging
logger = logging.getLogger(__name__)

# Create your views here.

# def _get_specialists():
#     return Specialist.objects.all()

# async def get_specialists():
#     return Specialist.objects.all()

# sync_get_specialists = async_to_sync(get_specialists)

# # @sync_to_async
# # @async_to_sync
# @api_view(['GET'])
# @permission_classes([permissions.AllowAny])
# async def get_doctors_follow_specialists(request: Request):
#     specialists = sync_get_specialists()
#     await sleep(2)
#     logger.info('Async view specialist invoked')
#     print(specialists)
    
#     return Response()

@sync_to_async
@api_view(['GET'])
def get_doctors_follow_specialists(request: Request):
    
    specialists = list(Specialist.objects.all())
    spec_ids = [ spec.pk for spec in specialists ]
    doctors = DoctorSpecialist.objects.select_related('doctor').filter(specialist_id__in = spec_ids)
    
    for doct_spec in doctors:
        temp_spec = next((specialist for specialist in specialists if doct_spec.specialist_id == specialist.pk) , None)
        if not hasattr(temp_spec, 'doctor_list'):
            setattr(temp_spec, 'doctor_list', [])
        temp_spec.doctor_list.append(doct_spec.doctor)
    
    serializer = ReadOnlyHomeSpecialistSerializer(specialists, many = True)
    response = format_response(
        success = True,
        status = 200,
        message = ResponseMessage.GET_DATA_SUCCEEDED,
        data = serializer.data
    )
    return Response(response, response['status'])


@sync_to_async
@api_view(['GET'])
def get_doctors_by_specialist(request: Request, *args, **kwargs):
    logger.info('Get doctors by specialist id invoked')
    pk = kwargs.get('pk')
    page, limit = get_page_limit_from_request(request)
    specialist = Specialist.objects\
        .prefetch_related(
            Prefetch(
                lookup = 'doctors',
                queryset = DoctorSpecialist.objects.select_related('doctor', 'specialist').filter(specialist_id = pk)
            )
        )\
        .get(pk = pk)
    # doctor_specs = DoctorSpecialist.objects.select_related('doctor', 'specialist').filter(specialist_id = pk)
    
    return get_paginated_response(specialist.doctors.all(), page, limit, ReadOnlyDoctorSpecialistSerializer)

@sync_to_async
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_all_specialists(request: Request, *args, **kwargs):
    logger.info('Get all specialists invoked')
    page, limit = get_page_limit_from_request(request)
    specialists = Specialist.objects.all()
    
    return get_paginated_response(specialists, page, limit, ReadOnlySpecialistSerializer)

@sync_to_async
@api_view(['GET'])
@permission_classes([IsDoctor])
def get_specialists_of_doctor(request: Request, *args, **kwargs):
    logger.info('Get doctor\'s specialists invoked')
    user: User = request.user
    page, limit = get_page_limit_from_request(request)
    specialists = Specialist.objects.filter(doctors__doctor_id = user.doctor_id)
    
    return get_paginated_response(specialists, page, limit, ReadOnlySpecialistSerializer)
