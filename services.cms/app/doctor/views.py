from rest_framework import generics, permissions, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.request import Request
from specialist.models import DoctorSpecialist, Specialist
from service.models import DoctorService
from user.models import User, UserType
from doctor.models import Doctor, Package, SpecType, Specification, WorkingShift
from doctor.serializers import (
    DSSerializer,
    DoctorSerializer,
    DoctorSerializer2,
    ManyDoctorServiceSerializer, 
    ManyPackageSerializer, 
    ManyWorkingShiftSerializer, 
    PackageSerializer, 
    ReadOnlyDoctorSerializer,
    ReadOnlyDoctorSerializer2,
    UpdateDSSerializer, 
    ViewPackageSerializer, 
    WorkingShiftSerializer
)
from doctor.repositories import get_doctors_with_name, manager_get_doctors_with_name
from shared.formatter import format_response
from shared.paginations import get_paginated_response, get_paginated_data
from shared.utils import get_locations, get_page_limit_from_request
from shared.response_messages import ResponseMessage
from shared.exceptions import CustomValidationError
from shared.models import ServiceCategory
from shared.app_permissions import IsDoctor, IsManager
from django.db.models import Prefetch, Q
from django.db import transaction

import logging
logger = logging.getLogger(__name__)
# Create your views here.
class CreateDoctorView(generics.CreateAPIView):
    """
    API create doctor profile
    """
    serializer_class = DoctorSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer: DoctorSerializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        response = format_response(
            success = True,
            status = 201,
            message = ResponseMessage.REGISTRATION_SUCCESS,
            data = serializer.data
        )
        
        return Response(response, response['status'])
    
class GetDoctorInfoView(generics.RetrieveAPIView):
    serializer_class = DoctorSerializer
    
    def retrieve(self, request, *args, **kwargs):
        # doctor: Doctor = self.get_object(kwargs.pop('pk'))
        doctor_id: int = kwargs.get('pk')
        doctor = Doctor.objects\
                                .prefetch_related(
                                    Prefetch(
                                        'shifts',
                                        WorkingShift.objects.order_by('weekday').filter(doctor_id = doctor_id)
                                    ),
                                    'specs', 
                                )\
                                .select_related('account')\
                                .get(pk = doctor_id, isApproved = True)
                                
        doctor_specialists = DoctorSpecialist.objects.select_related('specialist').filter(doctor_id = doctor.pk)
        doctor.specialist_list = list(doctor_specialists)
        serializer: DoctorSerializer = DoctorSerializer(instance = doctor)
        response = format_response(
            success = True,
            status = 200,
            message = ResponseMessage.GET_DOCTOR_PROFILE,
            data = serializer.to_representation(doctor)
        )
        return Response(response, response['status'])
    
class ListUpdateDoctorShiftsView(generics.RetrieveUpdateAPIView):
    serializer_class = WorkingShiftSerializer
    permission_classes = [IsDoctor]
    
    def retrieve(self, request: Request, *args, **kwargs):
        # doctor: Doctor = self.get_object(kwargs.pop('pk'))
        doctor_account: User = request.user
        working_shifts = WorkingShift.objects.select_related('doctor').filter(doctor = doctor_account.doctor_id)\
                                                                        .order_by('weekday')
                                
        serializer: ManyWorkingShiftSerializer = ManyWorkingShiftSerializer(working_shifts)
        response = format_response(
            success = True,
            status = 200,
            message = ResponseMessage.GET_DATA_SUCCEEDED,
            data = serializer.to_representation(working_shifts)
        )
        logger.info(f'Get working shifts of doctor {doctor_account.doctor_id} succeeded')
        return Response(response, response['status'])
    
    def update(self, request: Request, *args, **kwargs):
        doctor_account: User = request.user
        shifts = list(doctor_account.doctor.shifts.all().order_by('weekday'))
        serializer: ManyWorkingShiftSerializer = ManyWorkingShiftSerializer(instance = shifts, data = request.data, context = {'doctor_account': doctor_account})
        serializer.is_valid(raise_exception = True)
        data = serializer.save()
        response = format_response(
            success = True,
            status = 202,
            message = ResponseMessage.UPDATE_SHIFTS_SUCCESS,
            data = serializer.to_representation(data)
        )
        return Response(response, response['status'])
    
class RemoveDoctorShiftsView(generics.DestroyAPIView):
    serializer_class = WorkingShiftSerializer
    permission_classes = [IsDoctor]
    
    def destroy(self, request: Request, *args, **kwargs):
        
        shift_id = kwargs.pop('pk')
        with transaction.atomic():
            WorkingShift.objects.filter(pk = shift_id).delete()
        
        logger.info(f'Remove shift succeeded')
        return Response(status = status.HTTP_204_NO_CONTENT)
    
class ListDoctorsView(generics.ListAPIView):
    serializer_class = DoctorSerializer

    def list(self, request: Request, *args, **kwargs):
        page, limit = get_page_limit_from_request(request)
        queryset = Doctor.objects\
            .prefetch_related(
                Prefetch(
                    'specialists',
                    DoctorSpecialist.objects.select_related('specialist').all(),
                    'specialist_list'
                ),
                'shifts',
                'specs'
            )\
            .select_related('account')\
            .filter(isApproved = True)
        response: Response = get_paginated_response(queryset, page, limit, self.get_serializer_class())
        return response
    
class ListCreatePackageView(generics.ListCreateAPIView):
    
    def get_permissions(self):
        if self.request.method == 'POST':
            permission_classes = [IsDoctor]
        else:
            permission_classes = [permissions.IsAuthenticated]
            
        return [permission() for permission in permission_classes]
    
    def list(self, request: Request, *args, **kwargs):
        pk = kwargs.pop('pk', None)
        doctor: Doctor = Doctor.objects\
            .prefetch_related(
                Prefetch(
                    'packages',
                    Package.objects.filter(isApproved = True)
                )
            ).filter(pk = pk, isApproved = True).first()
        if not doctor:
            raise CustomValidationError(message = ResponseMessage.NOT_FOUND, detail = {'doctor': f'Not found with id {pk}'})
        
        page, limit = get_page_limit_from_request(request)
        
        packages = doctor.packages.all()
        # package_serializer = ViewPackageSerializer(packages, many = True)
        response = get_paginated_response(packages, page, limit, ViewPackageSerializer)
        return response
    
    def create(self, request: Request, *args, **kwargs):
        pk = kwargs.pop('pk', None)
        doctor: Doctor = Doctor.objects.prefetch_related('packages').filter(pk = pk, isApproved = True).first()
        if not doctor:
            raise CustomValidationError(message = ResponseMessage.NOT_FOUND, detail = {'doctor': f'Not found with id {pk}'})
        serializer = ManyPackageSerializer(data = request.data, context = {'doctor': doctor})
        serializer.is_valid(raise_exception = True)
        package_list = serializer.save()
        
        data = PackageSerializer(package_list, many = True).data
        
        response = format_response(
            success = True,
            status = 201,
            message = ResponseMessage.PACKAGE_CREATE_SUCCEEDED,
            data = data
        )
        
        return Response(response, response['status'])
    
    
class RemovePackageView(generics.DestroyAPIView):
    
    serializer_class = DoctorSerializer
    permission_classes = [IsDoctor]
    
    def destroy(self, request: Request, *args, **kwargs):
        doctor_id = kwargs.pop('doctor_id', None)
        package_id = kwargs.pop('package_id', None)
        
        queryset = Package.objects\
            .filter(pk = package_id, doctor_id = doctor_id, isApproved = True)\
            .update(isApproved = False)
        
        if queryset == 0:
            response = format_response(
                success = True,
                status = 200,
                message = ResponseMessage.NO_AFFECTED_ROWS
            )
            return Response(response, status = response['status'])
        
        return Response(status = 204)

class ListNearestDoctorsView(generics.ListAPIView):
    serializer_class = DoctorSerializer
    permission_classes = [ permissions.AllowAny ]
    
    def list(self, request: Request, *args, **kwargs):
        origin = request.query_params.get('address')
        if not origin:
            raise CustomValidationError(message = ResponseMessage.INVALID_INPUT, detail = [{'address': 'Missing this param'}])
        page, limit = get_page_limit_from_request(request)
        queryset = Doctor.objects\
            .prefetch_related(
                Prefetch(
                    'specialists',
                    DoctorSpecialist.objects.select_related('specialist').all(),
                    'specialist_list'
                ),
                'shifts',
                'specs'
            )\
            .select_related('account')\
            .filter(isApproved = True)
        response: Response = get_paginated_response(queryset, page, limit, self.get_serializer_class())
        
        docts: list = response.data['data']
        destinations = [ doct['address'] for doct in docts ]
        
        distance_obj = get_locations(origin, destinations)
        locations: list = distance_obj.get('locations')
        for index, doctor in enumerate(docts):
            if 'distance' not in locations[index]:
                docts.pop(index)
                continue
            doctor['distance'] = locations[index]['distance']
            doctor['duration'] = locations[index]['duration']
        
        def sort_func(data: dict):
            return data['distance']['value'] if 'distance' in data else 999999
        
        docts.sort(key = sort_func)
        
        return response
    
class ManagerCreateDoctorView(generics.CreateAPIView):
    """
    API create doctor profile by manager
    """
    serializer_class = DoctorSerializer2
    permission_classes = [IsManager]
    
    def create(self, request, *args, **kwargs):
        serializer: DoctorSerializer2 = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        
        response = format_response(
            success = True,
            status = 201,
            message = ResponseMessage.DOCTOR_CREATED_SUCCEED,
            data = serializer.data
        )
        return Response(response, response['status'])

class LockDoctorView(generics.UpdateAPIView):
    """
    API lock doctor profile
    """
    serializer_class = DoctorSerializer
    permission_classes = [IsManager]
    queryset = Doctor.objects.select_related('account').all()
    
    @transaction.atomic
    def update(self, request: Request, *args, **kwargs):
        doctor: Doctor = self.get_object()
        doctor.isApproved = not doctor.isApproved
        doctor.save()
        serializer = DoctorSerializer(doctor)
        response = format_response(
            success = True,
            status = 202,
            message = ResponseMessage.DOCTOR_UNLOCKED_SUCCEEDED if doctor.isApproved else ResponseMessage.DOCTOR_LOCKED_SUCCEEDED,
            data = serializer.data
        )
        return Response(response, response['status'])


class ListCreateDoctorServiceView(generics.ListCreateAPIView):
    
    def get_permissions(self):
        if self.request.method == 'POST':
            permission_classes = [IsManager]
        else:
            permission_classes = [permissions.IsAuthenticated]
            
        return [permission() for permission in permission_classes]
    
    @transaction.atomic
    def create(self, request: Request, *args, **kwargs):
        doctor_id = kwargs.pop('doctor_id')
        doctor = Doctor.objects.select_related('account').get(pk = doctor_id)
        serializer = ManyDoctorServiceSerializer(data = request.data, context = { 'doctor': doctor })
        serializer.is_valid(raise_exception = True)
        service_list = serializer.save()
        
        try:
            service_list[0]
        except:
            response = format_response(
                success = True,
                status = 200,
                message = ResponseMessage.NO_AFFECTED_ROWS,
            )
            return Response(response, response['status'])
        
        data = DSSerializer(service_list, many = True).data
        response = format_response(
            success = True,
            status = 201,
            message = ResponseMessage.SERVICE_CREATE_SUCCEEDED,
            data = data
        )
        return Response(response, response['status'])
    
    def list(self, request: Request, *args, **kwargs):
        logger.info('Listing doctor\' services')
        doctor_id = kwargs.pop('doctor_id')
        page, limit = get_page_limit_from_request(request)
        q: str = request.query_params.get('q') or ''
        account: User = request.user
        if account.type == UserType.MEMBER:
            queryset = DoctorService.objects\
                .select_related('doctor', 'service')\
                .filter(doctor_id = doctor_id, isActive = True).exclude(service__category = ServiceCategory.CONTRACT)
        else:
            queryset = DoctorService.objects\
                .select_related('doctor', 'service')\
                .filter(doctor_id = doctor_id, service__name__icontains = q)
        response = get_paginated_response(queryset, page, limit, DSSerializer)
        return response
    
class ListServiceContractView(generics.ListAPIView):
    
    def list(self, request: Request, *args, **kwargs):
        logger.info('Listing doctor\' services CONTRACT')
        doctor_id = kwargs.pop('pk')
        page, limit = get_page_limit_from_request(request)
        queryset = DoctorService.objects\
            .select_related('doctor', 'service')\
            .filter(doctor_id = doctor_id, service__category = ServiceCategory.CONTRACT)
        response = get_paginated_response(queryset, page, limit, DSSerializer)
        return response

class RetrieveUpdateDestroyDSView(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = [IsDoctor,]
    
    def get_permissions(self):
        permission_map = {
            'PUT': [IsDoctor,],
            'DELETE': [IsDoctor,],
            'GET': [permissions.IsAuthenticated,],
        }
        
        permission_classes = permission_map.get(self.request.method, [permissions.IsAuthenticated,])
        return [ cls() for cls in permission_classes ]
    
    
    def get_object_custom(self, doctor_id: int, service_id: int) -> DoctorService:
        obj = DoctorService.objects\
            .select_related('doctor', 'service')\
            .filter(doctor_id = doctor_id, service_id = service_id)\
            .first()
        if not obj:
            from django.http import Http404
            raise Http404()
        return obj
    
    def retrieve(self, request, *args, **kwargs):
        doctor_id: int = kwargs.pop('doctor_id')
        service_id: int = kwargs.pop('service_id')
        obj = self.get_object_custom(doctor_id, service_id)
        response = format_response(
            success = True,
            status = 200,
            message = ResponseMessage.GET_DATA_SUCCEEDED,
            data = DSSerializer(obj).data
        )
        return Response(response, response['status'])
    
    @transaction.atomic
    def update(self, request: Request, *args, **kwargs):
        doctor_id: int = kwargs.pop('doctor_id')
        service_id: int = kwargs.pop('service_id')
        obj = self.get_object_custom(doctor_id, service_id)
        serializer = UpdateDSSerializer(instance = obj, data = request.data, context = { 'doctor_id': doctor_id })
        serializer.is_valid(raise_exception = True)
        serializer.save()
        response = format_response(
            success = True,
            status = 202,
            message = ResponseMessage.SERVICE_UPDATE_SUCCEEDED,
            data = serializer.data
        )
        return Response(response, response['status'])
    
    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        doctor_id: int = kwargs.pop('doctor_id')
        service_id: int = kwargs.pop('service_id')
        obj = self.get_object_custom(doctor_id, service_id)
        update_fields = ['updatedAt', 'isActive']
        obj.isActive = not obj.isActive
        obj.save(update_fields = update_fields)
        return Response(status = 204)
    
class SearchDoctorView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    
    def list(self, request: Request, *args, **kwargs):
        q = request.query_params.get('q') or ''
        page, limit = get_page_limit_from_request(request)
        queryset = get_doctors_with_name(q)
        # queryset = Doctor.objects.filter(
        #     Q(firstName__search = q) | Q(lastName__search = q)
        # )
        return get_paginated_response(queryset, page, limit, ReadOnlyDoctorSerializer2)
    
class ManagerSearchDoctorView(generics.ListAPIView):
    permission_classes = [IsManager]
    
    def list(self, request: Request, *args, **kwargs):
        q = request.query_params.get('q') or ''
        page, limit = get_page_limit_from_request(request)
        queryset = manager_get_doctors_with_name(q)
        return get_paginated_response(queryset, page, limit, ReadOnlyDoctorSerializer2)