from datetime import datetime, timedelta
from django.utils import timezone
from rest_framework import serializers
from appointment.serializers import SendNotificationThread
from schedule.models import Schedule
from treatment.models import SessionStatus, TreatmentContract, TreatmentSession
from user.models import User
from patient.models import Patient
from doctor.models import Doctor, WorkingShift
from service.models import Service
from shared.models import ContractStatus, NotificationType, ScheduleType
from shared.exceptions import CustomValidationError
from shared.response_messages import ResponseMessage
from myapp.settings import DATETIME_FORMAT 
from health_record.models import HealthRecord
from health_record.serializers import HrDetailSerializer, ReadOnlyHealthRecordSerializer
from shared.clone import clonePrescription, cloneMedicalInstruction
from django.db import transaction
from shared.utils import convert_weekday, from_json, time_to_int, to_json
from django.db.models import Q
from shared.tasks import MyThread
from transaction.models import Transaction, TransactionType, Order, TransactionPlatform
import logging
from fcm_django.models import FCMDevice
from firebase_admin.messaging import Message, Notification as FNotification

logger = logging.getLogger(__name__)

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
        
        
        return self._format_slots(available_slots)
class TreatmentContractCreatorSerializer(serializers.Serializer):
    doctor = serializers.IntegerField(min_value=1)
    patient = serializers.IntegerField(min_value=1)
    package = serializers.IntegerField(min_value=1, required=False)
    startedAt = serializers.DateField(required=False)
    endedAt = serializers.DateField(required=False)
    # detail = HrDetailSerializer()
    prescriptions = serializers.ListField(
        allow_empty=True,
        child=serializers.IntegerField(min_value=1)
    )
    instructions = serializers.ListField(
        allow_empty=True,
        child=serializers.IntegerField(min_value=1)
    )

    def _push_notification_to_doctor(self, contract: TreatmentContract):
        devices = FCMDevice.objects.filter(user_id = contract.doctor.account.pk)
        devices.send_message(
            Message(
                data = {
                    'type': NotificationType.INFO,
                    'model': TreatmentContract.__name__,
                    'message': ResponseMessage.CONTRACT_CREATE_SUCCEEDED,
                    'payload': to_json({
                        'contract': ListTreatmentContractSerializer2(instance= contract).data
                    }),
                }
            )
        )
        logger.info('Push notification successfully')
    class Meta:
        fields = [
            'doctor', 'patient', 'package', 'startedAt',
            'endedAt', 'detail', 'prescription', 'instructions'
        ]

    def validate_doctor(self, doctor_id):
        try:
            return Doctor.objects.get(pk=doctor_id)
        except:
            raise CustomValidationError(message=ResponseMessage.NOT_FOUND, detail={
                                        'doctor': f'Doctor with id {doctor_id} not found'})

    def validate_patient(self, patient_id):
        user: User = self.context.get('supervisor')
        try:
            return Patient.objects.get(pk=patient_id, supervisor_id=user.pk)
        except:
            raise CustomValidationError(message=ResponseMessage.NOT_FOUND, detail={
                                        'patient': f'Patient with id {patient_id} not found'})

    def validate_package(self, service_id):
        try:
            return Service.objects.get(pk=service_id)
        except:
            raise CustomValidationError(message=ResponseMessage.NOT_FOUND, detail={
                                        'package': f'Package with id {service_id} not found'})

    def validate_startedAt(self, startedAt: datetime):
        current = timezone.now() + timedelta(hours=7)
        if current.date() > startedAt:
            raise CustomValidationError(
                message=ResponseMessage.DATE_OUT_OF_BOUND,
                detail={'started': 'Invalid date'}
            )
        return startedAt
    
    def create(self, validated_data: dict):
        logger.info('Creating contract...')
        doctor = validated_data['doctor']
        startedAt = validated_data['startedAt']
        patient = validated_data['patient']
        package: Service = validated_data.get('package')
        supervisor: User = self.context['supervisor']
        detail: dict = self.context.get('detail')
        prescriptions: list = validated_data.get('prescriptions')
        instructions: list = validated_data.get('instructions')
        duplicate_contract = TreatmentContract.objects\
            .filter(
                endedAt__date__gte = startedAt,
                startedAt__date__lte = startedAt,
                service = package,
                patient = patient,
                doctor = doctor
            )\
            .exclude(status__in=[ContractStatus.CANCELLED, ContractStatus.EXPIRED])

        if duplicate_contract:
            raise CustomValidationError(message=ResponseMessage.CONTRACT_DUPLICATED)

        contract = TreatmentContract(
            supervisor = supervisor,
            doctor = doctor,
            patient = patient,
            startedAt = startedAt,
            service = package
        )
        contract.save()
        record = HealthRecord(
            doctor = doctor,
            startedAt = startedAt,
            patient = patient,
            contract = contract,
            detail = detail
        )
        record.save()
        for prescription_id in prescriptions:
            clonePrescription(prescription_id, record)

        for instruction_id in instructions:
            cloneMedicalInstruction(instruction_id, record)
        record.contract = contract
        self._push_notification_to_doctor(contract)
        return contract

    def to_representation(self, instance):
        record = HealthRecord.objects.filter(contract__pk=instance.pk)
        recordSerializer = ReadOnlyHealthRecordSerializer(
            instance=record, many=True)
        return {
            'id': instance.pk,
            'startedAt': instance.startedAt,
            'endedAt': instance.endedAt,
            'price': instance.price,
            'status': instance.status,
            'doctor': {
                'id': instance.doctor.pk,
                'firstName': instance.doctor.firstName,
                'lastName': instance.doctor.lastName,
            },
            'patient': {
                'id': instance.patient.pk,
                'firstName': instance.patient.firstName,
                'lastName': instance.patient.lastName,
            },
            'supervisor': {
                'id': instance.supervisor.pk,
                'firstName': instance.supervisor.firstName,
                'lastName': instance.supervisor.lastName,
            },
            'healthRecord': recordSerializer.data
        }


def valid_action(instance):
    if instance.status == ContractStatus.CANCELLED:
        raise CustomValidationError(
            message='Invalid Action', detail='Contract already cancelled', code=400)
    if instance.status == ContractStatus.EXPIRED:
        raise CustomValidationError(
            message='Invalid Action', detail='Contract already expired', code=400)

def refund(doctor:User, supevisor:User, order: Order):
    doctor.tempBalance -= order.amount
    supevisor.mainBalance += order.amount
    trans: Transaction = Transaction(
        amount = order.amount,
        type = TransactionType.REFUNDED,
        sender = doctor,
        receiver =supevisor,
        order= order,
        platform = TransactionPlatform.SYSTEM
    )
    trans.save()
    doctor.save(update_fields=['tempBalance'])
    supevisor.save(update_fields=['mainBalance'])
    logger.info('refund successfully')

def transfer(doctor:User, supevisor:User, order: Order):
    doctor.tempBalance += order.amount
    supevisor.mainBalance -= order.amount
    trans: Transaction = Transaction(
        amount = order.amount,
        type = TransactionType.TRANSFERRED,
        sender = supevisor,
        receiver = doctor,
        order= order,
        platform = TransactionPlatform.SYSTEM
    )
    trans.save()
    doctor.save(update_fields=['tempBalance'])
    supevisor.save(update_fields=['mainBalance'])
    logger.info('refund successfully')


class TreatmentSessionListSerializer(serializers.ListSerializer): 
    startTime = serializers.DateTimeField(required = False)
    endTime = serializers.DateTimeField(required = False)
    date = serializers.DateField(required = False)
    @transaction.atomic()
    def create(self, validated_data):
        contract: TreatmentContract = self.context['contract']
        for item in validated_data:
            startTime = item.get('startTime')
            endTime = item.get('endTime')
            # print('session', startTime < contract.startedAt, startTime > contract.endedAt)
            # print('session', startTime,  contract.startedAt, startTime, contract.endedAt)
            schedule = Schedule.objects.filter(bookedAt__lte = endTime, bookedAt__gte = startTime).first()
            logger.info('before validation 1')
            print(contract.startedAt, startTime,contract.startedAt < startTime)
            print(contract.startedAt, endTime,contract.startedAt > endTime)
            if contract.startedAt > startTime and contract.endedAt < startTime:
                raise CustomValidationError(message = 'Out of bound', detail = 'Session time outbound of contract', code = 400)
            logger.info('before validation 2')
            if schedule: 
                raise CustomValidationError(message = 'Duplicate Schedule', detail = 'Duplicate Schedule', code = 400)
        result = []
        schedules = []
        for item in validated_data:
            startTime = item.get('startTime')
            endTime = item.get('endTime')
            print('299 session', startTime, endTime)
            session = TreatmentSession(doctor = contract.doctor, patient = contract.patient, startTime = startTime, endTime = endTime, supervisor = contract.supervisor, contract = contract,note = to_json({}), assessment = to_json({}))
            result.append(session)
        ret = TreatmentSession.objects.bulk_create(result)
        for item in ret:
            schedule = Schedule(bookedAt = session.startTime, estEndAt = session.endTime, doctor = contract.doctor, content_object = item, type = ScheduleType.SESSION)
            schedules.append(schedule)
        Schedule.objects.bulk_create(schedules)
        print('294 session', startTime, endTime)
        return ret
class TreatmentSessionSerializer2(serializers.Serializer):
    startTime = serializers.DateTimeField(required = False)
    endTime = serializers.DateTimeField(required = False)
    date = serializers.DateField(required = False)
    def valid_startTime(self, startTime:datetime):
        start = timezone.now().replace(day= startTime.day, month= startTime.month, year= startTime.year, hour= startTime.hour, minute= startTime.minute, second= startTime.second)
        if timezone.now() > start:
            raise CustomValidationError(message = "Time_Out", detail="Start time must be larger than now")
        return start

    def valid_endTime(self, endTime):
        end = timezone.now().replace(day= endTime.day, month= endTime.month, year= endTime.year, hour= endTime.hour, minute= endTime.minute, second= endTime.second)
        if timezone.now() > end:
            raise CustomValidationError(message = "Time_Out", detail="End time must be larger than now")
        return end

    # @transaction.atomic()
    # def create(self, validated_data):
    #     print('created')
    #     start:datetime = validated_data['startTime']
    #     end:datetime = validated_data['endTime']
    #     duplicate  = Schedule.objects.filter(bookedAt__gte = start, bookedAt__lte = end).first()
    #     if duplicate is not None:
    #         raise CustomValidationError(message='Duplicate',detail= 'Session is duplicated schedules', code = 400)
    #     if start > end:
    #         raise CustomValidationError(message='Invalid Time',detail= 'End time must be greater than start time of session', code = 400)
    #     contract: TreatmentContract = validated_data['contract']
    #     doctor: Doctor = self.context['doctor']
    #     patient: Patient = contract.patient
    #     session = TreatmentSession(doctor = doctor, patient = patient, startTime = start, endTime = end, supervisor = patient.supervisor, contract = contract,note = to_json(validated_data['note']), assessment = to_json(validated_data['assessment']))
    #     session.save()
    #     schedule = Schedule(doctor = doctor, bookedAt = start, estEndAt = end, content_object = session)
    #     schedule.save()
    #     return session

    def to_representation(self, instance:TreatmentSession):
        contract: TreatmentContract = instance.contract
        healthRecord = HealthRecord.objects.filter(contract__pk = contract.pk).first()
        return {
            'id': instance.pk,
            'start': datetime.strftime(instance.startTime, '%Y-%m-%d %H:%M:%S'),
            'end': datetime.strftime(instance.endTime, '%Y-%m-%d %H:%M:%S'),
            'date': datetime.strftime(instance.startTime, '%Y-%m-%d'),
            'status': instance.status,
            'note': from_json(instance.note),
            'assessment': from_json(instance.assessment),
            'checkInCode': instance.checkInCode,
            'cancelReason': instance.cancelReason,
            'contract': {
                'id': contract.id,
                'startDate': contract.startedAt,
                'endDate': contract.endedAt,
            },
            'patient':{
                'id': instance.patient.pk,
                'firstName': contract.patient.firstName,
                'lastName': contract.patient.lastName,
                'address': contract.patient.address,
                'dob': contract.patient.dob,
                'gender': contract.patient.gender
            },
            'supervisor':{
                'id': instance.supervisor.pk,
                'firstName': contract.supervisor.firstName,
                'lastName': contract.supervisor.lastName,
            },
            'healthRecord': {
                'id': healthRecord.pk,
            }
        }
    class Meta:
        list_serializer_class = TreatmentSessionListSerializer

class ListTreatmentContractSerializer(serializers.Serializer):
    def to_representation(self, instance: TreatmentContract):
        record = instance.health_records
        serializer = ReadOnlyHealthRecordSerializer(instance=record, many=True)
        print('record', serializer.data)
        order: Order = Order.objects.filter(
            treatment_contract=instance).first()
        return {
            'id': instance.pk,
            'startedAt': datetime.strftime(instance.startedAt, DATETIME_FORMAT) if instance.startedAt else None,
            'endedAt': datetime.strftime(instance.endedAt, DATETIME_FORMAT) if instance.endedAt else None,
            'price': instance.price,
            'status': instance.status,
            'doctor': {
                'id': instance.doctor.pk,
                'firstName': instance.doctor.firstName,
                'lastName': instance.doctor.lastName,
            },
            'patient': {
                'id': instance.patient.pk,
                'firstName': instance.patient.firstName,
                'lastName': instance.patient.lastName,
                'avatar': instance.patient.avatar,
                'address': instance.patient.address,
                'dob': instance.patient.dob,
                'gender': instance.patient.gender,
            },
            'supervisor': {
                'id': instance.supervisor.pk,
                'firstName': instance.supervisor.firstName,
                'lastName': instance.supervisor.lastName,
            },
            'healthRecord': serializer.data,
            'order': {
                'pk': order.pk,
                'amount': order.amount,
                'status': order.currency,
            } if order else {},
            'service': {
                'id': instance.service.pk,
                'name': instance.service.name
            }
        }


class ListTreatmentContractSerializer2(serializers.Serializer):
    def to_representation(self, instance: TreatmentContract):
        return {
            'id': instance.pk,
            'price': instance.price,
            'status': instance.status,
            'doctor': {
                'id': instance.doctor.pk,
                'firstName': instance.doctor.firstName,
                'lastName': instance.doctor.lastName,
            },
            'patient': {
                'id': instance.patient.pk,
                'firstName': instance.patient.firstName,
                'lastName': instance.patient.lastName,
                'avatar': instance.patient.avatar,
                'address': instance.patient.address,
                'gender': instance.patient.gender,
            },
            'service': {
                'id': instance.service.pk,
                'name': instance.service.name
            }
        }
class DoctorTreatmentContractUpdateSerializer(serializers.Serializer):
    cancelReason = serializers.CharField(required=False)
    def _push_notification_to_supervisor(self, contract: TreatmentContract ):
        devices = FCMDevice.objects.filter(user_id = contract.supervisor.pk)
        devices.send_message(
            Message(
                data = {
                    'type': NotificationType.INFO,
                    'model': TreatmentContract.__name__,
                    'message': ResponseMessage.CONTRACT_APPROVED,
                    'payload': to_json({
                        'contract': {
                            'contract': ListTreatmentContractSerializer2(contract).data
                        }
                    }),
                }
            )
        )
        logger.info('Push notification successfully')

    def _push_notification_to_doctor(self, contract: TreatmentContract):
        devices = FCMDevice.objects.filter(user_id = contract.doctor.account.pk)
        devices.send_message(
            Message(
                data = {
                    'type': NotificationType.INFO,
                    'model': TreatmentContract.__name__,
                    'message': ResponseMessage.CONTRACT_APPROVED,
                    'payload': to_json({
                        'contract': {
                            'contract': ListTreatmentContractSerializer2(contract).data
                        }
                    }),
                }
            )
        )
        logger.info('Push notification successfully')

    def _push_cancel_notification_to_supervisor(self, contract: TreatmentContract ):
        devices = FCMDevice.objects.filter(user_id = contract.supervisor.pk)
        devices.send_message(
            Message(
                data = {
                    'type': NotificationType.INFO,
                    'model': TreatmentContract.__name__,
                    'message': ResponseMessage.CONTRACT_CANCELLED_BY_DOCTOR,
                    'payload': to_json({
                        'contract': {
                            'contract': ListTreatmentContractSerializer2(contract).data
                        }
                    }),
                }
            )
        )
        logger.info('Push notification successfully')

    def _push_cancel_notification_to_doctor(self, contract: TreatmentContract):
        devices = FCMDevice.objects.filter(user_id = contract.doctor.account.pk)
        devices.send_message(
            Message(
                data = {
                    'type': NotificationType.INFO,
                    'model': TreatmentContract.__name__,
                    'message': ResponseMessage.CONTRACT_CANCELLED_BY_DOCTOR,
                    'payload': to_json({
                        'contract': {
                            'contract': ListTreatmentContractSerializer2(contract).data
                        }
                    }),
                }
            )
        )
        logger.info('Push notification successfully')



    @transaction.atomic()
    def update(self, instance: TreatmentContract, validated_data):
        update_fields = ['status']
        action: str = self.context['action']
        doctor = self.context['doctor']
        num_of_days: float = self.context['number_of_days']
        endAt: float = self.context['endAt']
        print('num_of_days', num_of_days, instance.pk)
        valid_action(instance)
        print(num_of_days)
        if timezone.now().replace(hour=0, minute=0, second=0) > instance.startedAt:
            raise CustomValidationError(
                message='Time exceeded', detail='Contract is no longer to approve', code=400
            )
        if doctor.pk != instance.doctor.pk:
            raise CustomValidationError(
                message='Not allowed', detail='Contract is not belong this doctor', code=400)

        if action.lower() == 'cancel' and instance.status == ContractStatus.PENDING:
            order = Order.objects.filter(treatment_contract__pk = instance.pk).first()
            docUser = User.objects.filter(doctor__pk = instance.doctor.pk).first()
            refund(doctor = docUser, supevisor= instance.supervisor, order = order)
            
        if action.lower() == 'cancel':
            update_fields.append('cancelReason')
            instance.status = ContractStatus.CANCELLED
            instance.cancelReason = validated_data['cancelReason']
            sessions = TreatmentSession.objects.filter(contract = instance)
            schedules =Schedule.objects.filter(treatment_session__in = sessions)
            print('schedules', schedules, sessions)
            schedules.delete()
            sessions.delete()
            # print(schedules)
            # return instance
        if action.lower() == 'approve':
            if instance.status != ContractStatus.PENDING:
                raise CustomValidationError(message = 'Invalid Status', detail = 'Only approve the contract with a pending status', code = 400)
            if timezone.now() > instance.startedAt:
                raise CustomValidationError(message = 'Expired', detail = 'Only approve the contract before start time of contract reach', code = 400)
            with transaction.atomic():
                sessions = self.context['sessions']
                instance.status = ContractStatus.APPROVED
                instance.price = instance.service.price * num_of_days
                instance.endedAt = endAt
                code = timezone.now().timestamp().__str__
                order = Order(amount=instance.price, code=code,
                              content_object=instance, currency='VND')
                order.save()
                update_fields.append('price')
                update_fields.append('endedAt')
                valid = TreatmentSessionSerializer2(data = sessions, many = True, context = {'contract': instance, 'endTime':  instance.endedAt})
                valid.is_valid(raise_exception = True)
                valid.save()
        else:
            raise CustomValidationError('')
        if action == 'approve':
            self._push_notification_to_doctor(instance)
            self._push_notification_to_supervisor(instance)
        if action == 'cancel':
            self._push_cancel_notification_to_doctor(instance)
            self._push_cancel_notification_to_supervisor(instance)
        instance.save(update_fields=update_fields)
        return instance

    def to_representation(self, instance):
        record = HealthRecord.objects.filter(contract__pk=instance.pk)
        serializer = ReadOnlyHealthRecordSerializer(instance=record, many=True)
        order = Order.objects.filter(treatment_contract = instance).first()
        return {
            'id': instance.pk,
            'startedAt': instance.startedAt,
            'endedAt': instance.endedAt,
            'price': instance.price,
            'status': instance.status,
            'doctor': {
                'id': instance.doctor.pk,
                'firstName': instance.doctor.firstName,
                'lastName': instance.doctor.lastName,
                'address': instance.doctor.address,
                'dob': instance.doctor.dob,
            },
            'patient': {
                'id': instance.patient.pk,
                'firstName': instance.patient.firstName,
                'lastName': instance.patient.lastName,
                'avatar': instance.patient.avatar
            },
            'supervisor': {
                'id': instance.supervisor.pk,
                'firstName': instance.supervisor.firstName,
                'lastName': instance.supervisor.lastName,
            },
            'healthRecord': serializer.data,
            'order': {
                'pk': order.pk,
                'amount': order.amount,
                'status': order.currency,
            } if order else {},
            'service': {
                'id': instance.service.pk,
                'name': instance.service.name,
            }
        }


class PatientTreatmentContractUpdateSerializer(serializers.Serializer):
    cancelReason = serializers.CharField(required=False)
    logger.info('Push notification successfully')
    
    def _push_notification_to_supervisor(self, contract: TreatmentContract ):
        devices = FCMDevice.objects.filter(user_id = contract.supervisor.pk)
        devices.send_message(
            Message(
                data = {
                    'type': NotificationType.INFO,
                    'model': TreatmentContract.__name__,
                    'message': ResponseMessage.CONTRACT_IN_PROGRESS,
                    'payload': to_json({
                        'contract': ListTreatmentContractSerializer2(instance = contract).data
                    }),
                }
            )
        )
        logger.info('Push notification successfully')

    def _push_notification_to_doctor(self, contract: TreatmentContract):
        devices = FCMDevice.objects.filter(user_id = contract.doctor.account.pk)
        devices.send_message(
            Message(
                data = {
                    'type': NotificationType.INFO,
                    'model': TreatmentContract.__name__,
                    'message': ResponseMessage.CONTRACT_IN_PROGRESS,
                    'payload': to_json({
                        'contract': ListTreatmentContractSerializer2(instance= contract).data
                    }),
                }
            )
        )
        logger.info('Push notification successfully')

    def _push_cancel_notification_to_supervisor(self, contract: TreatmentContract ):
        devices = FCMDevice.objects.filter(user_id = contract.supervisor.pk)
        devices.send_message(
            Message(
                data = {
                    'type': NotificationType.INFO,
                    'model': TreatmentContract.__name__,
                    'message': ResponseMessage.CONTRACT_CANCELLED_BY_SUPERVISOR,
                    'payload': to_json({
                        'contract': ListTreatmentContractSerializer(instance= contract).data
                    }),
                }
            )
        )
        logger.info('Push notification successfully')

    def _push_cancel_notification_to_doctor(self, contract: TreatmentContract):
        devices = FCMDevice.objects.filter(user_id = contract.doctor.account.pk)
        devices.send_message(
            Message(
                data = {
                    'type': NotificationType.INFO,
                    'model': TreatmentContract.__name__,
                    'message': ResponseMessage.CONTRACT_CANCELLED_BY_SUPERVISOR,
                    'payload': to_json({
                        'contract': ListTreatmentContractSerializer2(instance= contract).data
                    }),
                }
            )
        )
        logger.info('Push notification successfully')



    @transaction.atomic()
    def update(self, instance: TreatmentContract, validated_data):
        print('can refund ')
        update_fields = ['status']
        action: str = self.context['action']
        supervisor = self.context['supervisor']
        valid_action(instance)
        if supervisor.pk != instance.supervisor.pk:
            raise CustomValidationError(
                'Invalid Action', 'Contract is not belong to this supervisor', code=400)
        if action.lower() == 'cancel':
            update_fields.append('cancelReason')
            update_fields.append('isSupervisorCancelled')
            status = instance.status
            if status == ContractStatus.IN_PROGRESS and instance.startedAt - timezone.now() > timedelta(days = 1):
                order = Order.objects.filter(treatment_contract= instance).first()
                docUser: User = User.objects.filter(doctor__pk=instance.doctor.pk).first()
                refund(doctor = docUser, supevisor = supervisor, order = order)
            instance.status = ContractStatus.CANCELLED
            instance.isSupervisorCancelled = True
            instance.cancelReason = validated_data['cancelReason']
        if action.lower() == 'sign' and instance.status == ContractStatus.APPROVED:
            instance.status = ContractStatus.IN_PROGRESS
            if supervisor.mainBalance < instance.price:
                raise CustomValidationError(
                    code=400, detail='Balance not enough', message='Not enough')
            docUser: User = User.objects.filter(doctor__pk=instance.doctor.pk).first()
            order = Order.objects.filter(treatment_contract= instance).first()
            transfer(docUser, supervisor, order)
            # trans: Transaction = Transaction(
            #     amount=instance.price,
            #     type=TransactionType.TRANSFERRED,
            #     sender=supervisor,
            #     receiver=docUser,
            #     order= order,
            #     platform=TransactionPlatform.CASH
            # )
            # supervisor.mainBalance -= instance.price
            # docUser.tempBalance += instance.price
            # print('before error', docUser, instance.order)
            # supervisor.save()
            # docUser.save()
            # trans.save()
            update_fields.append('price')
            update_fields.append('endedAt')
        if action == 'sign':
            self._push_notification_to_supervisor(instance)
            self._push_notification_to_doctor(instance)
        if action == 'cancel':
            self._push_cancel_notification_to_doctor(instance)
            self._push_cancel_notification_to_supervisor(instance)
        instance.save(update_fields=update_fields)
        return instance

    def to_representation(self, instance):
        record = HealthRecord.objects.filter(contract__pk=instance.pk)
        serializer = ReadOnlyHealthRecordSerializer(instance=record, many=True)
        return {
            'id': instance.pk,
            'startedAt': instance.startedAt.strftime(DATETIME_FORMAT) if instance.startedAt else None,
            'endedAt': instance.endedAt.strftime(DATETIME_FORMAT) if instance.endedAt else None,
            'price': instance.price,
            'status': instance.status,
            'doctor': {
                'id': instance.doctor.pk,
                'firstName': instance.doctor.firstName,
                'lastName': instance.doctor.lastName,
            },
            'patient': {
                'id': instance.patient.pk,
                'firstName': instance.patient.firstName,
                'lastName': instance.patient.lastName,
                'address': instance.patient.address,
                'dob': instance.patient.dob,
            },
            'supervisor': {
                'id': instance.supervisor.pk,
                'firstName': instance.supervisor.firstName,
                'lastName': instance.supervisor.lastName,
            },
            'healthRecord': serializer.data,
            'service': {
                'id': instance.service.pk,
                'name': instance.service.name,
            }
        }



from slot.models import DoctorSlot, DoctorSlotState
class TreatmentSessionSerializer(serializers.Serializer):
    contract = serializers.IntegerField(min_value = 1)
    slot = serializers.IntegerField(required = False)
    note = serializers.JSONField(required = False)
    assessment = serializers.JSONField(required = False)
    startTime = serializers.DateTimeField(required = False)
    endTime = serializers.DateTimeField(required = False)
    def validate_contract(self, contract: int):
        doctor = self.context['doctor']
        target_contract = TreatmentContract.objects.select_related('doctor', 'patient','supervisor').filter(pk = contract).first()
        if target_contract is None:
            raise CustomValidationError(message= 'Not Found', detail='Không tìm thấy hợp đông', code = 400)
        if target_contract.doctor != doctor:
            raise CustomValidationError(message= 'Invalid Contract', detail='Contract does not match doctor', code =400)
        if target_contract.status == ContractStatus.CANCELLED or target_contract.status == ContractStatus.EXPIRED:
            raise CustomValidationError(message= 'Invalid Contract', detail='Hợp đồng cần phải có trạng thái khác chấp thuận hoặc đã kí hoặc đang tiến hành', code =400)
        return target_contract

    def validate_startTime(self, startTime:datetime):
        # start = timezone.now().replace(day= startTime.day, month= startTime.month, year= startTime.year, hour= startTime.hour, minute= startTime.minute, second= startTime.second)
        if timezone.now() - startTime > timezone.timedelta(seconds=0):
            raise CustomValidationError(message = "Time_Out", detail="Thời gian bắt đầu của phiên đánh giá/điều trị cần phải lớn hơn thời gian hiện tại")
        return startTime

    def validate_endTime(self, endTime):
        end = timezone.now().replace(day= endTime.day, month= endTime.month, year= endTime.year, hour= endTime.hour, minute= endTime.minute, second= endTime.second)
        if timezone.now() > end:
            raise CustomValidationError(message = "Time_Out", detail="Thời gian bắt đầu của phiên đánh giá/điều trị cần phải lớn hơn thời gian hiện tại")
        return end

    @transaction.atomic()
    def create(self, validated_data):
        print('created')
        start:datetime = validated_data['startTime']
        end:datetime = validated_data['endTime']
        contract: TreatmentContract = validated_data['contract']
        doctor: Doctor = self.context['doctor']
        patient: Patient = contract.patient
        duplicate  = Schedule.objects.filter(bookedAt__gte = start, bookedAt__lte = end).first()
        if duplicate is not None:
            raise CustomValidationError(message='Duplicate',detail= 'Session is duplicated schedules', code = 400)
        if start > end:
            raise CustomValidationError(message='Invalid Time',detail= 'End time must be greater than start time of session', code = 400)
        if contract.status == ContractStatus.PENDING or contract.status == ContractStatus.EXPIRED or contract.status == ContractStatus.CANCELLED:
            raise CustomValidationError(message='INVALID_CONTRACT_STATUS', detail= 'Hợp đồng phải có trạng thái chấp, đã kí, đang tiến hành', code = 400)
        session = TreatmentSession(doctor = doctor, patient = patient, startTime = start, endTime = end, supervisor = patient.supervisor, contract = contract,note = to_json(validated_data['note']), assessment = to_json(validated_data['assessment']))
        session.save()
        schedule = Schedule(doctor = doctor, bookedAt = start, estEndAt = end, content_object = session)
        schedule.save()
        return session

    def to_representation(self, instance:TreatmentSession):
        slot:DoctorSlot = instance.slot
        contract: TreatmentContract = instance.contract
        healthRecord = HealthRecord.objects.filter(contract__pk = contract.pk).first()
        return {
            'id': instance.pk,
            'start': datetime.strftime(instance.startTime, '%Y-%m-%d %H:%M:%S'),
            'end': datetime.strftime(instance.endTime, '%Y-%m-%d %H:%M:%S'),
            'date': datetime.strftime(instance.startTime, '%Y-%m-%d'),
            'status': instance.status,
            'note': from_json(instance.note),
            'assessment': from_json(instance.assessment),
            'checkInCode': instance.checkInCode,
            'cancelReason': instance.cancelReason,
            'contract': {
                'id': contract.id,
                'startDate': contract.startedAt,
                'endDate': contract.endedAt,
            },
            'patient':{
                'id': instance.patient.pk,
                'firstName': contract.patient.firstName,
                'lastName': contract.patient.lastName,
                'address': contract.patient.address,
                'dob': contract.patient.dob,
                'gender': contract.patient.gender
            },
            'supervisor':{
                'id': instance.supervisor.pk,
                'firstName': contract.supervisor.firstName,
                'lastName': contract.supervisor.lastName,
            },
            'healthRecord': {
                'id': healthRecord.pk,
                'startAt': healthRecord.startedAt,
                'endAt': healthRecord.endedAt,
            }
        }


class ReadOnlyTreatmentSessionSerializer(serializers.Serializer): 

        def to_representation(self, instance:TreatmentSession):
            contract: TreatmentContract = instance.contract
            healthRecord = HealthRecord.objects.filter(contract = contract).first()
            return {    
                'id': instance.pk,
                'start': datetime.strftime(instance.startTime, '%Y-%m-%d %H:%M:%S'),
                'end': datetime.strftime(instance.endTime, '%Y-%m-%d %H:%M:%S'),
                'date': datetime.strftime(instance.endTime, '%Y-%m-%d'),
                'status': instance.status,
                'note': from_json(instance.note),
                'assessment': from_json(instance.assessment),
                'checkInCode': instance.checkInCode,
                'cancelReason': instance.cancelReason,
                'isDoctorCancelled': instance.isDoctorCancelled,
                'isSupervisorCancelled': instance.isSupervisorCancelled,
                'isSystemCancelled': instance.isSystemCancelled,
                'contract': {
                    'id': contract.id,
                    'startDate': contract.startedAt,
                    'endDate': contract.endedAt,
                },
                'patient':{
                    'id': instance.patient.pk,
                    'firstName': contract.patient.firstName,
                    'lastName': contract.patient.lastName,
                    'address': contract.patient.address,
                    'dob': contract.patient.dob,
                    'gender': contract.patient.gender
                },
                'supervisor':{
                    'id': instance.supervisor.pk,
                    'firstName': contract.supervisor.firstName,
                    'lastName': contract.supervisor.lastName,
                },
                'healthRecord': {
                    'id': healthRecord.pk,
                    'startAt': healthRecord.startedAt,
                    'endAt': healthRecord.endedAt,
                }
            }


class CancelTreatmentSessionsSerializer(serializers.Serializer):
    cancelReason = serializers.CharField(required = False)
    @transaction.atomic()
    def update(self, instance:TreatmentSession, validated_data):
        cancelReason  = validated_data['cancelReason']
        doctor = self.context['doctor']
        if doctor != instance.doctor: 
            raise CustomValidationError(message= 'Invalid Session', detail= f'Session is not belong to doctor {doctor.pk}', code = 400)
        if instance.status == SessionStatus.CANCELLED or instance.status == SessionStatus.IN_PROGRESS:
            raise CustomValidationError(message= 'Invalid Session', detail= f'Session is not already cancelled or in progress', code = 400)
        schedule = Schedule.objects.filter(treatment_session = instance).first()
        if schedule:
            schedule.delete()
        instance.status = SessionStatus.CANCELLED
        instance.isDoctorCancelled = True
        instance.cancelReason = cancelReason
        print(instance.status)
        instance.save()
        return instance

    def to_representation(self, instance:TreatmentSession):
        contract: TreatmentContract = instance.contract
        healthRecord = HealthRecord.objects.filter(contract = contract).first()
        return {    
                'id': instance.pk,
                'start': datetime.strftime(instance.startTime, '%Y-%m-%d %H:%M:%S'),
                'end': datetime.strftime(instance.endTime, '%Y-%m-%d %H:%M:%S'),
                'status': instance.status,
                'date': datetime.strftime(instance.startTime, '%Y-%m-%d'),
                'status': instance.status,
                'note': from_json(instance.note),
                'assessment': from_json(instance.assessment),
                'checkInCode': instance.checkInCode,
                'cancelReason': instance.cancelReason,
                'isDoctorCancelled': instance.isDoctorCancelled,
                'isSupervisorCancelled': instance.isSupervisorCancelled,
                'isSystemCancelled': instance.isSystemCancelled,
                'contract': {
                    'id': contract.id,
                    'startDate': contract.startedAt,
                    'endDate': contract.endedAt,
                },
                'patient':{
                    'id': instance.patient.pk,
                    'firstName': contract.patient.firstName,
                    'lastName': contract.patient.lastName,
                    'address': contract.patient.address,
                    'dob': contract.patient.dob,
                    'gender': contract.patient.gender
                },
                'supervisor':{
                    'id': instance.supervisor.pk,
                    'firstName': contract.supervisor.firstName,
                    'lastName': contract.supervisor.lastName,
                },
                'healthRecord': {
                    'id': healthRecord.pk,
                    'startAt': healthRecord.startedAt,
                    'endAt': healthRecord.endedAt,
                }
            }



class SupervisorCancelTreatmentSessionsSerializer(serializers.Serializer):
    cancelReason = serializers.CharField()
    @transaction.atomic()
    def update(self, instance:TreatmentSession, validated_data):
        slot:DoctorSlot = instance.slot
        cancelReason = validated_data['cancelReason']
        supervisor = self.context['supervisor']
        if supervisor != instance.supervisor: 
            raise CustomValidationError(message= 'Invalid Session', detail= f'Session is not belong to supervisor {supervisor.pk}', code = 400)
        if instance.status == SessionStatus.CANCELLED or instance.status == SessionStatus.IN_PROGRESS:
            raise CustomValidationError(message= 'Invalid Session', detail= f'Session is not already cancelled or in progress', code = 400)
        schedule = Schedule.objects.filter(treatment_session = instance).first()
        if schedule:
            schedule.delete()
        instance.status = SessionStatus.CANCELLED
        instance.isSupervisorCancelled = True
        instance.cancelReason = cancelReason
        self._push_notification_to_doctor(instance)
        self._push_notification_to_supervisor(instance)
        instance.save()
        return instance
    def to_representation(self, instance:TreatmentSession):
        contract: TreatmentContract = instance.contract
        healthRecord = HealthRecord.objects.filter(contract = contract).first()
        return {    
                'id': instance.pk,
                'start': datetime.strftime(instance.startTime, '%Y-%m-%d %H:%M:%S'),
                'end': datetime.strftime(instance.endTime, '%Y-%m-%d %H:%M:%S'),
                'status': instance.status,
                'date': datetime.strftime(instance.startTime, '%Y-%m-%d'),
                'status': instance.status,
                'note': from_json(instance.note),
                'assessment': from_json(instance.assessment),
                'checkInCode': instance.checkInCode,
                'isDoctorCancelled': instance.isDoctorCancelled,
                'isSupervisorCancelled': instance.isSupervisorCancelled,
                'isSystemCancelled': instance.isSystemCancelled,
                'contract': {
                    'id': contract.id,
                    'startDate': contract.startedAt,
                    'endDate': contract.endedAt,
                },
                'patient':{
                    'id': instance.patient.pk,
                    'firstName': contract.patient.firstName,
                    'lastName': contract.patient.lastName,
                    'address': contract.patient.address,
                    'dob': contract.patient.dob,
                    'gender': contract.patient.gender
                },
                'supervisor':{
                    'id': instance.supervisor.pk,
                    'firstName': contract.supervisor.firstName,
                    'lastName': contract.supervisor.lastName,
                },
                'healthRecord': {
                    'id': healthRecord.pk,
                    'startAt': healthRecord.startedAt,
                    'endAt': healthRecord.endedAt,
                }
            }



class CompleteTreatmentSessionsSerializer(serializers.Serializer):
    assessment = serializers.JSONField(required = False)
    note = serializers.JSONField(required = False)
    @transaction.atomic()
    def update(self, instance:TreatmentSession, validated_data):
        assessment = validated_data['assessment']
        note = validated_data['note']
        doctor = self.context['doctor']
        if doctor != instance.doctor: 
            raise CustomValidationError(message= 'Invalid Session', detail= f'Session is not belong to doctor {doctor.pk}', code = 400)
        if instance.status != SessionStatus.IN_PROGRESS:
            raise CustomValidationError(message= 'Invalid Session', detail= f'Session is not already cancelled or in progress', code = 400)
        instance.status = SessionStatus.COMPLETED
        instance.assessment = to_json(assessment)
        instance.note = to_json(note)
        instance.save()
        return instance

    def to_representation(self, instance:TreatmentSession):
        slot:DoctorSlot = instance.slot
        contract: TreatmentContract = instance.contract
        healthRecord = HealthRecord.objects.filter(contract = contract).first()
        return {    
                'id': instance.pk,
                'start': datetime.strftime(instance.startTime, '%Y-%m-%d %H:%M:%S'),
                'end': datetime.strftime(instance.endTime, '%Y-%m-%d %H:%M:%S'),
                'status': instance.status,
                'date': datetime.strftime(instance.startTime, '%Y-%m-%d'),
                'note': from_json(instance.note),
                'assessment': from_json(instance.assessment),
                'checkInCode': instance.checkInCode,
                'contract': {
                    'id': contract.id,
                    'startDate': contract.startedAt,
                    'endDate': contract.endedAt,
                },
                'patient':{
                    'id': instance.patient.pk,
                    'firstName': contract.patient.firstName,
                    'lastName': contract.patient.lastName,
                    'address': contract.patient.address,
                    'dob': contract.patient.dob,
                    'gender': contract.patient.gender
                },
                'supervisor':{
                    'id': instance.supervisor.pk,
                    'firstName': contract.supervisor.firstName,
                    'lastName': contract.supervisor.lastName,
                },
                'healthRecord': {
                    'id': healthRecord.pk,
                    'startAt': healthRecord.startedAt,
                    'endAt': healthRecord.endedAt,
                }
            }


class CheckInTreatmentSessionsSerializer(serializers.Serializer):
    checkInCode = serializers.CharField()
    @transaction.atomic()
    def update(self, instance:TreatmentSession, validated_data):
        checkInCode = validated_data['checkInCode']
        supervisor = self.context['supervisor']
        now = timezone.now() + timedelta(hours = 7)
        slotCheckInTime = timezone.now().replace(year = instance.startTime.year, month = instance.startTime.month, day = instance.startTime.day)\
            .replace(hour = instance.startTime.hour, minute = instance.startTime.minute, second =instance.startTime.second, microsecond = 0)
        print('now', now, 'slotCheckInTime', slotCheckInTime)
        if now < slotCheckInTime: 
            raise CustomValidationError(message = 'INVALID_ACTION', detail = {'Check in time is not reached'}, code = 400)
        if instance.supervisor != supervisor:
            raise CustomValidationError(detail = 'Slot do not belong to this supervisor', message = 'Invalid Session', code = 400)
        if instance.checkInCode != checkInCode:
            raise CustomValidationError(message = 'Invalid Check in code', detail = 'Check in code not match', code = 400)
        if instance.status != SessionStatus.PENDING:
            raise CustomValidationError(message = 'Invalid Action', detail = f'Cannot check in with session has status {instance.status}', code = 400)
        print('validated success')
        instance.status = SessionStatus.IN_PROGRESS
        instance.save()
        # print('success check in')
        return instance

    def to_representation(self, instance:TreatmentSession):
        contract: TreatmentContract = instance.contract
        healthRecord = HealthRecord.objects.filter(contract = contract).first()
        return {    
                'id': instance.pk,
                'start': datetime.strftime(instance.startTime, '%Y-%m-%d %H:%M:%S'),
                'end': datetime.strftime(instance.endTime, '%Y-%m-%d %H:%M:%S'),
                'status': instance.status,
                'date': datetime.strftime(instance.startTime, '%Y-%m-%d'),
                'note': from_json(instance.note),
                'assessment': from_json(instance.assessment),
                'checkInCode': instance.checkInCode,
                'cancelReason': instance.cancelReason,
                'contract': {
                    'id': contract.id,
                    'startDate': contract.startedAt,
                    'endDate': contract.endedAt,
                },
                'patient':{
                    'id': instance.patient.pk,
                    'firstName': contract.patient.firstName,
                    'lastName': contract.patient.lastName,
                    'address': contract.patient.address,
                    'dob': contract.patient.dob,
                    'gender': contract.patient.gender
                },
                'supervisor':{
                    'id': instance.supervisor.pk,
                    'firstName': contract.supervisor.firstName,
                    'lastName': contract.supervisor.lastName,
                },
                'healthRecord': {
                    'id': healthRecord.pk,
                    'startAt': healthRecord.startedAt,
                    'endAt': healthRecord.endedAt,
                }
            }