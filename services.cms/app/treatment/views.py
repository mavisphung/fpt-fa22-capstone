from django.utils import timezone
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, RetrieveAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from doctor.models import WorkingShift
from health_record.models import HealthRecord
from schedule.models import Schedule
from transaction.models import Order
from shared.utils import convert_weekday, get_page_limit_from_request, time_to_int
from user.models import User
from shared.exceptions import CustomValidationError
from shared.app_permissions import IsDoctor, IsSupervisor
from shared.formatter import format_response
from shared.utils import get_paginated_response
from shared.response_messages import ResponseMessage
from treatment.serializers import (
    CancelTreatmentSessionsSerializer,
    CheckInTreatmentSessionsSerializer,
    CompleteTreatmentSessionsSerializer,
    ReadOnlyTreatmentSessionSerializer,
    SupervisorCancelTreatmentSessionsSerializer,
    TreatmentContractCreatorSerializer,
    DoctorTreatmentContractUpdateSerializer,
    PatientTreatmentContractUpdateSerializer,
    ListTreatmentContractSerializer,
    TreatmentSessionSerializer
)
from treatment.models import TreatmentContract, TreatmentSession
from django.db.models import Q
from django.db.models.query import Prefetch
from django.db import transaction
from datetime import datetime, time, timedelta
import logging
logger = logging.getLogger(__name__)
# Create your views here.


class CreateContractView(CreateAPIView):
    serializer_class = TreatmentContractCreatorSerializer
    permission_classes = [IsSupervisor]

    @transaction.atomic
    def create(self, request: Request, *args, **kwargs):
        supervisor = request.user
        data = request.data.copy()
        detail = data.pop('detail', None)
        serializer: TreatmentContractCreatorSerializer = self.get_serializer(
            data=request.data,
            context={'supervisor': supervisor, 'detail': detail}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = format_response(
            success=True,
            status=201,
            message=ResponseMessage.CONTRACT_CREATE_SUCCEEDED,
            data=serializer.data
        )
        return Response(response, status=response['status'])


class DoctorUpdateContractView(UpdateAPIView):
    serializer_class = DoctorTreatmentContractUpdateSerializer
    permission_classes = [IsDoctor]
    def update(self, request: Request, *args, **kwargs):
        contractId = kwargs['contract']
        doctor = request.user.doctor
        action = kwargs['action']
        contract = TreatmentContract.objects.select_related('supervisor', 'doctor', 'patient', 'service')\
            .filter(pk=contractId).first()
        numOfDays: int = request.data.get('numOfDays', 0)
        endAt = request.data.get('endedAt', None)
        if not endAt:
            raise CustomValidationError(message='INVALID_END_AT', detail='endAt must be specified', code = 400)
        if contract is None:
            raise CustomValidationError(
                message='Not Found', detail='Contract not found', code=404)
        serializer: DoctorTreatmentContractUpdateSerializer = self.get_serializer(instance=contract, data={
            'cancelReason': request.data['cancelReason']
        } 
        if action == 'cancel' else {}, context={
            'action': action,
            'doctor': doctor,
            'number_of_days': numOfDays,
            'sessions': request.data.get('sessions',[]),
            'endAt': endAt
        })
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = format_response(
            success=True, message='SUCCESS', status=202, data=serializer.data)
        return Response(data=response, status=response['status'])


class SupervisorUpdateContractView(UpdateAPIView):
    serializer_class = PatientTreatmentContractUpdateSerializer
    permission_classes = [IsSupervisor]

    def update(self, request, *args, **kwargs):
        contractId = kwargs['contract']
        action = kwargs['action']
        supervisor = request.user
        contract = TreatmentContract.objects.select_related(
            'doctor', 'patient', 'supervisor', 'service').filter(pk=contractId).first()
        if contract is None:
            raise CustomValidationError(
                message='Not Found', detail='Contract not found', code=404)
        print('update 91')
        serializer: PatientTreatmentContractUpdateSerializer = self.get_serializer(instance=contract, data=request.data if action == 'cancel' else {}, context={
            'action': action,
            'supervisor': supervisor,
        })
        print('update 93')
        serializer.is_valid(raise_exception=True)
        print('update 95')
        serializer.save()
        print('update 95')
        response = format_response(
            success=True, message='SUCCESS', status=202, data=serializer.data)
        return Response(data=response, status=response['status'])


class DoctorTreatmentContractListView(ListAPIView):
    serializer_class = ListTreatmentContractSerializer
    permission_classes = [IsDoctor]
    queryset = TreatmentContract.objects.prefetch_related(Prefetch(
        'health_records',
        queryset=HealthRecord.objects.all(),
    )).select_related(
        'doctor', 'patient', 'supervisor', 'service'
    ).all()

    def list(self, request: Request, *args, **kwargs):
        allowed_params: list = ['status', 'startedAt__lte',
                                'startedAt__gte', 'endedAt__lte', 'endAt__gte', 'patient']
        filter = request.query_params.copy()
        doctor = request.user.doctor
        page = filter.pop('page', 1)
        limit = filter.pop('limit', 10)
        page, limit = get_page_limit_from_request(request)
        q = Q()
        for k, v in filter.items():
            if k in allowed_params:
                q.add(Q(**{k: v}), Q.AND)
        result = self.get_queryset().filter(q).filter(doctor__pk=doctor.pk)
        response = get_paginated_response(
            result, page, limit, self.get_serializer_class())
        return response


class SupervisorTreatmentContractListView(ListAPIView):
    serializer_class = ListTreatmentContractSerializer
    permission_classes = [IsSupervisor]
    queryset = TreatmentContract.objects.select_related(
        'doctor', 'patient', 'supervisor', 'service').all()

    def list(self, request: Request, *args, **kwargs):
        allowed_params: list = ['status', 'startedAt__lte',
                                'startedAt__gte', 'endedAt__lte', 'endAt__gte', 'patient']
        filter = request.query_params.copy()
        supervisor = request.user
        page, limit = get_page_limit_from_request(request)
        q = Q()
        for k, v in filter.items():
            if k in allowed_params:
                q.add(Q(**{k: v}), Q.AND)
        # q.add(doctor__pk=doctor.pk)
        result = self.get_queryset().filter(q, supervisor__pk=supervisor.pk)
        print(result)
        self.get_serializer(instance=result, many=True)
        response = get_paginated_response(
            result, page_number=page, limit=limit, serializer_class=self.get_serializer_class())
        return response


class SupervisorTreatmentContractView(ListAPIView):
    serializer_class = ListTreatmentContractSerializer
    permission_classes = [IsSupervisor]
    queryset = TreatmentContract.objects.select_related(
        'doctor', 'patient', 'supervisor', 'service').all()

    def list(self, request: Request, *args, **kwargs):
        contract_id = kwargs['contract']
        supervisor: User = request.user
        contract = self.get_queryset().filter(
            pk=contract_id, supervisor__pk=supervisor.pk).first()
        if contract is None:
            raise CustomValidationError(
                message='Not Found', detail='Contract not found')
        serializer = self.get_serializer(instance=contract)
        response = format_response(
            success=True,
            status=200,
            message=ResponseMessage.GET_DATA_SUCCEEDED,
            data=serializer.data
        )
        return Response(data=response, status=response['status'])


class DoctorTreatmentContractView(ListAPIView):
    serializer_class = ListTreatmentContractSerializer
    permission_classes = [IsDoctor]
    queryset = TreatmentContract.objects.select_related(
        'doctor', 'patient', 'supervisor').all()

    def list(self, request: Request, *args, **kwargs):
        contract_id = kwargs['contract']
        doctor = request.user.doctor
        contract = self.get_queryset().filter(
            pk=contract_id, doctor__pk=doctor.pk).first()
        if contract is None:
            raise CustomValidationError(
                message='Not Found', detail='Contract not found')
        serializer = self.get_serializer(instance=contract)
        response = format_response(
            data=contract, serializer=serializer.data, success=True)
        return Response(data=response, status=response['status'])


class TestOrderView(ListAPIView):
    serializer_class = ListTreatmentContractSerializer
    permission_classes = [IsSupervisor]
    queryset = TreatmentContract.objects.select_related(
        'doctor', 'patient', 'supervisor').all()

    def list(self, request: Request, *args, **kwargs):
        contract_id = kwargs['contract']
        contract: TreatmentContract = TreatmentContract.objects.filter(
            pk=contract_id).first()
        order: Order = Order.objects.filter(
            treatment_contract=contract).first()
        return Response(data={'order': order.pk, 'contract': contract.pk}, status=200)




class DoctorTreatmentSessionCreateView(CreateAPIView):
    serializer_class = TreatmentSessionSerializer
    permission_classes = [IsDoctor]
    queryset = TreatmentSession.objects.select_related(
        'contract', 'doctor', 'supervisor').all()

    def create(self, request:Request, *args, **kwargs):
        doctor = request.user.doctor
        data = request.data.copy()
        data['doctor'] = doctor
        serializer = self.get_serializer(data = data, context = {'doctor': doctor})
        serializer.is_valid(raise_exception = True)
        serializer.save()
        response = format_response(
            data = serializer.data, success=True)
        return Response(data=response, status=response['status'])

class DoctorTreatmentSessionView(ListAPIView):
    serializer_class = ReadOnlyTreatmentSessionSerializer
    permission_classes = [IsDoctor]
    queryset = TreatmentSession.objects.select_related(
        'contract','supervisor', 'doctor','patient').all()

    def list(self, request: Request, *args, **kwargs):
        contract_id = request.query_params['contract']
        doctor = request.user.doctor
        sessions = self.get_queryset().filter(
            contract__pk = contract_id,
            contract__doctor__pk = doctor.pk)
        serializer = self.get_serializer(instance= sessions, many = True)
        response = format_response(
            data=serializer.data, success=True)
        return Response(data=response, status=response['status'])


class SupervisorTreatmentSessionView(ListAPIView):
    serializer_class = ReadOnlyTreatmentSessionSerializer
    permission_classes = [IsSupervisor]
    queryset = TreatmentSession.objects.select_related(
        'contract').all()

    def list(self, request: Request, *args, **kwargs):
        contract_id = kwargs['contract']
        supervisor = request.user
        sessions = self.get_queryset().filter(
            contract__pk=contract_id, contract__supervisor__pk=supervisor.pk)
        serializer = self.get_serializer(instance=sessions, many= True)
        response = format_response(
            data = serializer.data, success = True)
        return Response(data=response, status=response['status'])


class DoctorCancelTreatmentSessions(UpdateAPIView):
    permission_classes = [IsDoctor]
    serializer_class = CancelTreatmentSessionsSerializer
    queryset = TreatmentSession.objects.select_related('doctor', 'contract', 'patient').all()
    def update(self, request, *args, **kwargs):
        session_id = request.data['session']
        doctor = request.user.doctor
        print(doctor.pk)
        sessions = self.get_queryset().filter(pk = session_id, doctor__pk = doctor.pk).first()
        if sessions is None:
            raise CustomValidationError(message='Session Not Found', detail= f'Session not found wit id {session_id}', code = 400)
        serializer = self.get_serializer(instance=sessions, data = {'cancelReason': request.data['cancelReason']}, context ={
            'doctor': doctor,
        })
        serializer.is_valid(raise_exception = True)
        serializer.save()
        response = format_response(success = True, status = 202 , data = serializer.data)
        return Response(data = response, status = response['status'])

class SupervisorCancelTreatmentSessions(UpdateAPIView):
    permission_classes = [IsSupervisor]
    serializer_class = SupervisorCancelTreatmentSessionsSerializer
    queryset = TreatmentSession.objects.select_related('doctor', 'contract','supervisor', 'patient').all()
    def update(self, request, *args, **kwargs):
        session_id = request.data['session']
        supervisor = request.user
        sessions = self.get_queryset().filter(pk = session_id, supervisor = supervisor).first()
        if sessions is None:
            raise CustomValidationError(message='Session Not Found', detail= f'Session not found wit id {session_id}', code = 400)
        serializer = self.get_serializer(instance=sessions, data = {'cancelReason': request.data['cancelReason']},context ={
            'supervisor': supervisor,
        })
        response = format_response(success = True, status = 202 , data = serializer.data)
        return Response(data = response, status = response['status'])    

class SupervisorCheckInSessionView(UpdateAPIView):
    permission_classes = [IsSupervisor]
    serializer_class = CheckInTreatmentSessionsSerializer
    queryset = TreatmentSession.objects.select_related('doctor', 'contract','supervisor', 'patient').all()
    def update(self, request:Request, *args, **kwargs):
        session_id = request.data['session']
        data:dict = request.data.copy()
        data.pop('session', None)
        print('copy fail')
        supervisor = request.user
        sessions = self.get_queryset().filter(pk = session_id, supervisor = supervisor).first()
        if sessions is None:
            raise CustomValidationError(message='Session Not Found', detail= f'Session not found wit id {session_id}', code = 400)
        serializer = self.get_serializer(instance=sessions, data = data, context ={
            'supervisor': supervisor,
        })
        serializer.is_valid(raise_exception = True)
        serializer.save()
        response = format_response(success = True, status = 202 , data = serializer.data)
        return Response(data = response, status = response['status'])    

class DoctorCompleteSessionView(UpdateAPIView):
    permission_classes = [IsSupervisor]
    serializer_class = CompleteTreatmentSessionsSerializer
    queryset = TreatmentSession.objects.select_related('doctor', 'contract','supervisor', 'patient').all()
    def update(self, request, *args, **kwargs):
        session_id = request.data['session']
        data = request.data.copy()
        doctor = request.user.doctor
        sessions = self.get_queryset().filter(pk = session_id, doctor = doctor).first()
        if sessions is None:
            raise CustomValidationError(message='Session Not Found', detail= f'Session not found wit id {session_id}', code = 400)
        serializer = self.get_serializer(instance=sessions, data = {data},context ={
            'doctor': doctor,
        })
        serializer.is_valid(raise_exception = True)
        serializer.save()
        response = format_response(success = True, status = 202 , data = serializer.data)
        return Response(data = response, status = response['status'])    



class SuggestHoursOfDoctorView(RetrieveAPIView):
    permission_classes = [IsDoctor]
    
    def _get_available_slots(self, list_of_meeting_times):
        # 1 ngày 24 tiếng = 1440 phút
        # Băm thành 1 set busy để tránh có những phút bị trùng
        # và các phần tử trong set mang giá trị True - bận, False - Rảnh
        # get the busy time
        busy = { t for meets in list_of_meeting_times
            for start,end in meets
            for t in range(start-start//100*40,end-end//100*40) }
        # get the free time in a day
        free   = [t not in busy for t in range(1440)]
        # Tìm khoảng nghỉ trong free bằng cách compare giá trị thứ k và k+1
        breaks = [i for i,(a,b) in enumerate(zip(free,free[1:]),1) if b!=a]
        
        # list ra các khoảng nghỉ xen kẽ trong 1 ngày
        result = [(s,e) for s,e in zip([0]+breaks,breaks+[1439]) if free[s]]
        
        # trả về 1 mảng 2 chiều với phần tử có cấu trúc lần lượt là [<from>, <to>]
        return [[s+s//60*40,e+e//60*40] for s,e in result]
    
    def _format_slots(self, slots):
        
        def to_dict(slot: str):
            args = slot.split('-')
            return {
                'from': args[0],
                'to': args[1]
            }
        
        return map(to_dict, slots)
    
    def calculate_available_times(self, selected_date: datetime, doctor_id: int) -> list:
        logger.info('calculating available times')
        weekday = convert_weekday(selected_date)
        # print('day_of_week', weekday)
        schedules = Schedule.objects.filter(
            doctor_id = doctor_id,
            bookedAt__date = selected_date.date()
        )
        
        if not schedules.exists():
            return []
        
        converted_schedules = [ (time_to_int(sc.bookedAt), time_to_int(sc.estEndAt)) for sc in schedules ]
        available_slots = self._get_available_slots([converted_schedules])
        
        if available_slots is None or available_slots.__len__() == 0:
            raise CustomValidationError(ResponseMessage.FULL_SLOT,'Lịch trình trong ngày đã kín', 400)
        # get first slot (tuple)
        first_slot = available_slots[0]
        # print(first_slot)
        # get last slot (tuple)
        last_slot = available_slots[-1]
        
        today_shifts = list(WorkingShift.objects.filter(
            doctor_id = doctor_id,
            weekday = weekday
        ))
        
        earliest_shift = min(today_shifts, key = lambda shift: shift.startTime)
        latest_shift = max(today_shifts, key = lambda shift: shift.endTime)
        
        start_of_shift = time_to_int(earliest_shift.startTime)
        first_slot[0] = start_of_shift
        last_time = time_to_int(latest_shift.startTime)
        
        if start_of_shift == first_slot[1]:
            available_slots.pop(0)
        if last_slot[0] > last_time:
            available_slots.pop(-1)
        else:
            last_slot[1] = time_to_int(latest_shift.endTime)
        
        available_slots = ["-".join(f"{t//100:02}:{t%100:02}" for t in slot) for slot in available_slots]
        print('logger info: ', available_slots.__len__() == 0)
        return self._format_slots(available_slots)
        
    
    def retrieve(self, request: Request, *args, **kwargs):
        doctor_id: int = request.user.doctor.pk
        try:
            selected_date: datetime = datetime.strptime(request.query_params['date'], '%Y-%m-%d')
        except:
            response = format_response(
                success = True,
                status = 400,
                message = ResponseMessage.INVALID_INPUT,
                data = {
                    'date': 'Input date with format yyyy-MM-dd'
                }  
            )
            return Response(response, response['status'])
        
        available_slots = self.calculate_available_times(selected_date, doctor_id)
        # available_slots2 = caculateAvailableTimes(selected_date, doctor_id)
        print(available_slots,'slots')
        response = format_response(
            success = True,
            status = 200,
            message = ResponseMessage.GET_DATA_SUCCEEDED,
            data = available_slots
        )
        
        return Response(response, response['status'])