
from datetime import timedelta
from rest_framework import generics
from rest_framework.request import Request
from rest_framework.response import Response
from schedule.models import Schedule
from doctor.models import Doctor, WorkingShift
from appointment.models import Appointment
from appointment.serializers import (
    AppointmentSerializer2,
    CheckOutSerializer, 
    ReadOnlyAppointmentSerializer, 
    RescheduleSerializer,
    CAppointmentSerializer
)
from shared.exceptions import CustomValidationError
from shared.formatter import format_response
from shared.app_permissions import IsSupervisor, IsDoctor
from shared.response_messages import ResponseMessage
from shared.models import AppointmentStatus, NotificationType
from shared.paginations import get_paginated_response
from shared.utils import get_page_limit_from_request, dict_group_by, to_json
from user.models import User, UserType
from django.db import transaction
from django.db.models import F, Prefetch, Q
from django.db.models.query import prefetch_related_objects
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from firebase_admin.messaging import Message, Notification
from fcm_django.models import FCMDevice
from shared.tasks import MyThread

import logging
logger = logging.getLogger(__name__)

class ListCreateAppointmentView(generics.ListCreateAPIView):
    permission_classes = [IsSupervisor]
    serializer_class = AppointmentSerializer2
    queryset = Appointment.objects.filter(status = AppointmentStatus.PENDING)
    
    def list(self, request: Request, *args, **kwargs):
        page: int = int(request.query_params.get('page', 1))
        limit: int = int(request.query_params.get('limit', 10))
        queryset = Appointment.objects\
            .select_related('doctor', 'patient', 'booker', 'service')\
            .filter(status = AppointmentStatus.PENDING)
        
        response: Response = get_paginated_response(ret_list = queryset, page_number = page, limit = limit, serializer_class = self.get_serializer_class())
        return response
    
    def create(self, request: Request, *args, **kwargs):
        supervisor: User = request.user
        serializer: AppointmentSerializer2 = self.get_serializer(data = request.data, context = {'user': supervisor})
        serializer.is_valid(raise_exception = True)
        
        serializer.save()
        response = format_response(
            success = True,
            status = 201, 
            message = ResponseMessage.APPOINTMENT_CREATED_SUCCEEDED,
            data = serializer.data
        )
        return Response(response, status = response['status'])

class GetAppointmentView(generics.RetrieveAPIView):
    serializer_class = ReadOnlyAppointmentSerializer
    queryset = Appointment.objects.all()
    
    def retrieve(self, request: Request, *args, **kwargs):
        pk = int(kwargs.get('pk'))
        # schedule_ctype = ContentType.objects.get_for_model(Schedule)
        queryset: Appointment = Appointment.objects\
            .prefetch_related(
                Prefetch(
                    'schedule',
                    Schedule.objects.all(),
                    'cache_schedule'
                )
            )\
            .select_related('doctor', 'patient', 'booker', 'service').get(pk = pk)
        serializer: ReadOnlyAppointmentSerializer = self.get_serializer(queryset)
        
        response = format_response(
            success = True,
            status = 200,
            message = ResponseMessage.GET_DATA_SUCCEEDED,
            data = serializer.data
        )
        
        return Response(response, response['status'])
    
class CheckInAppointmentView(generics.UpdateAPIView):
    
    permission_classes = [IsDoctor]
    
    def _push_notification_to_supervisor(self, appointment: Appointment):
        devices = FCMDevice.objects.filter(user_id = appointment.booker_id)
        devices.send_message(
            Message(
                data = {
                    'type': NotificationType.INFO,
                    'model': Appointment.__name__,
                    'message': ResponseMessage.APPOINTMENT_ONLINE_CHECK_IN,
                    'payload': to_json({
                        'appointment': ReadOnlyAppointmentSerializer(appointment).data
                    }),
                }
            )
        )
        logger.info('Push notification successfully')
    
    @transaction.atomic
    def update(self, request: Request, *args, **kwargs):
        pk = kwargs.pop('pk')
        appointment: Appointment = Appointment.objects\
            .select_related('doctor', 'patient', 'booker', 'service')\
            .filter(pk = pk)\
            .first()
        if not appointment:
            raise CustomValidationError(message = ResponseMessage.NOT_FOUND, detail = {})
        
        if appointment.status != AppointmentStatus.PENDING:
            raise CustomValidationError(message = ResponseMessage.APPOINTMENT_PROCEEDED, detail = {})
        
        now = timezone.now()
        appointment.beginAt = now + timedelta(hours = 7)
        appointment.status = AppointmentStatus.IN_PROGRESS
        appointment.save()
        
        # TODO: Send notification to supervisor
        MyThread(self._push_notification_to_supervisor, appointment).start()
        
        response = format_response(
            success = True,
            status = 202,
            message = ResponseMessage.APPOINTMENT_CHECKIN_SUCCEEDED,
            data = ReadOnlyAppointmentSerializer(appointment).data
        )
        
        return Response(response, response['status'])

class CheckOutAppointmentView(generics.UpdateAPIView):
    
    permission_classes = [IsDoctor]
    
    def update(self, request: Request, *args, **kwargs):
        pk = kwargs.pop('pk')
        appointment: Appointment = Appointment.objects\
            .select_related('doctor', 'patient', 'booker', 'service')\
            .filter(pk = pk)\
            .first()
        
        serializer = CheckOutSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        
        if not appointment:
            raise CustomValidationError(message = ResponseMessage.NOT_FOUND, detail = {})
        
        if appointment.status != AppointmentStatus.IN_PROGRESS:
            raise CustomValidationError(message = ResponseMessage.APPOINTMENT_PROCEEDED, detail = {})
        
        now = timezone.now()
        with transaction.atomic():
            appointment.endAt = now + timedelta(hours = 7)
            appointment.status = AppointmentStatus.COMPLETED
            app_dict = ReadOnlyAppointmentSerializer(appointment).data
            appointment.historical = app_dict
            appointment.save(update_fields = ['endAt', 'status', 'updatedAt', 'historical'])
        
        serializer.save()
        
        response = format_response(
            success = True,
            status = 202,
            message = ResponseMessage.APPOINTMENT_CHECKOUT_SUCCEEDED,
            data = app_dict
        )
        
        return Response(response, response['status'])

class CancelAppointmentView(generics.UpdateAPIView):
    serializer_class = AppointmentSerializer2
    
    @transaction.atomic
    def update(self, request: Request, *args, **kwargs):
        pk = kwargs.pop('pk', None)
        account: User = request.user
        if account.type == UserType.MEMBER:
            appointment: Appointment = Appointment.objects.get(
                booker_id = account.pk,
                pk = pk,
            )
            serializer = CAppointmentSerializer(instance = appointment, data = request.data, context = { 'account': account })
            serializer.is_valid(raise_exception = True)
            serializer.save()
                
            response = format_response(
                success = True,
                status = 202,
                message = ResponseMessage.APPOINTMENT_CANCELLED_SUCCEEDED,
                data = serializer.data
            )
            return Response(response, response['status'])
        elif account.type == UserType.DOCTOR:
            appointment: Appointment = Appointment.objects.get(
                doctor_id = account.doctor_id,
                pk = pk,
            )
            serializer = CAppointmentSerializer(instance = appointment, data = request.data, context = { 'account': account })
            serializer.is_valid(raise_exception = True)
            serializer.save()
                
            response = format_response(
                success = True,
                status = 202,
                message = ResponseMessage.APPOINTMENT_CANCELLED_SUCCEEDED,
                data = serializer.data
            )
            return Response(response, response['status'])
    
class ListSheduledAppointmentView(generics.ListAPIView):
    """
    List scheduled appointment
    """
    
    def list(self, request: Request, *args, **kwargs):
        account: User = request.user
        page, limit = get_page_limit_from_request(request)
        status = request.query_params.get('status', AppointmentStatus.PENDING)
        
        if status not in AppointmentStatus.values:
            raise CustomValidationError(message = ResponseMessage.INVALID_CHOICE, detail = { 'status': f'status must be in ({AppointmentStatus.values})' })
        
        if account.doctor is not None and account.type == UserType.DOCTOR: # if user is supervisor
            queryset = account.doctor.appointments.select_related('doctor', 'patient', 'booker', 'service')\
                            .prefetch_related(
                                Prefetch(
                                    'schedule',
                                    Schedule.objects.all()
                                )
                            )\
                            .filter(status = status)\
                            .order_by('bookedAt')
        else:
            queryset = account.appointments.select_related('doctor', 'patient', 'booker', 'service').filter(status = status).order_by('bookedAt')
            # queryset = Appointment.objects.select_related('doctor', 'patient', 'booker')\
            #                             .filter(status = status, booker_id = account.pk)\
            #                             .order_by('-bookedAt')
        
        response: Response = get_paginated_response(ret_list = queryset, page_number = page, limit = limit, serializer_class = ReadOnlyAppointmentSerializer)

        return response

class SupervisorListHistoryAppointmentView(generics.ListAPIView):
    """
    List historical appointment: all status except pending
    """
    serializer_class = AppointmentSerializer2
    permission_classes = [IsSupervisor]
    
    def list(self, request: Request, *args, **kwargs):
        supervisor: User = request.user
        page, limit = get_page_limit_from_request(request)
        
        queryset = supervisor.appointments.select_related('doctor', 'patient', 'booker', 'service')\
                                            .prefetch_related(
                                                Prefetch(
                                                    'schedule',
                                                    Schedule.objects.all(),
                                                    to_attr = 'cache_schedule'
                                                )
                                            )\
                                            .filter(status__in = [AppointmentStatus.COMPLETED, AppointmentStatus.CANCELLED])\
                                            .order_by('-bookedAt')
        response: Response = get_paginated_response(
            ret_list = queryset, 
            page_number = page, 
            limit = limit, 
            serializer_class = ReadOnlyAppointmentSerializer
        )
        
        return response
    
class RescheduleAppointmentView(generics.UpdateAPIView):
    
    serializer_class = RescheduleSerializer
    
    def update(self, request: Request, *args, **kwargs):
        pk = kwargs.pop('pk')
        appointment = Appointment.objects.select_related('doctor', 'patient', 'booker', 'service').get(pk = pk)
        print(appointment)
        serializer: RescheduleSerializer = self.get_serializer(instance = appointment, data = request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        
        response = format_response(
            success = True,
            status = 202,
            message = ResponseMessage.APPOINTMENT_RESCHEDULED_SUCCEEDED,
            data = serializer.data
        )
        
        return Response(response, response['status'])
    
class DoctorListAppointmentView(generics.ListAPIView):
    permission_classes = [IsDoctor]
    serializer_class = AppointmentSerializer2
    
    
    def _get_statuses(self, data: str) -> list[str]:
        items = data.replace(',', ' ').strip().split(' ')
        if items[0] == '':
            return [AppointmentStatus.PENDING, AppointmentStatus.IN_PROGRESS]
        return items
    
    def list(self, request: Request, *args, **kwargs):
        logger.info('Invoked DoctorListAppointmentView')
        user: User = request.user
        param: dict = request.query_params.copy()
        allowed_params = ['bookedAt__lte', 'bookedAt__gte', 'bookedAt','status']
        q = Q()
        page, limit = get_page_limit_from_request(request)
        param.pop('page', None)
        param.pop('limit', None)
        for key, value in param.items():
            if key in allowed_params:
                q.add(Q(**{key: value}), Q.AND)
        q.add(Q(doctor_id = user.doctor_id), Q.AND)
        queryset = Appointment.objects.select_related('doctor', 'patient', 'booker', 'service').filter(q).order_by('-bookedAt')
        
        return get_paginated_response(queryset, page, limit, serializer_class = self.get_serializer_class())

class DoctorListPendingAppointmentView(generics.ListAPIView):
    permission_classes = [IsDoctor]
    serializer_class = AppointmentSerializer2
    
    def list(self, request: Request, *args, **kwargs):
        logger.info('Invoked DoctorListAppointmentView')
        user: User = request.user
        page, limit = get_page_limit_from_request(request)
        queryset = Appointment.objects.select_related('doctor', 'patient', 'booker', 'service')\
            .filter(
                status__in = [AppointmentStatus.PENDING, AppointmentStatus.IN_PROGRESS],
                doctor_id = user.doctor_id,
            )\
            .order_by('bookedAt')
        
        return get_paginated_response(queryset, page, limit, serializer_class = self.get_serializer_class())
