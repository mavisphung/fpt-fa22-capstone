from datetime import date, datetime, timedelta
from django.db import transaction
from instruction.models import MedicalInstruction
from prescription.models import PrescriptionDetail
from health_record.models import HealthRecord
from health_record.serializers import SupervisorHealthRecordSerializer
from shared.models import ScheduleType
from doctor.models import Doctor, WorkingShift
from user.models import User, Notification, UserType
from patient.models import Patient
from schedule.models import Schedule
from service.models import DoctorService, Service
from django.contrib.contenttypes.models import ContentType
from django.db.models.query import prefetch_related_objects
from shared.exceptions import CustomValidationError
from shared.tasks import MyThread
from shared.models import AppointmentType, AppointmentStatus, ServiceCategory
from shared.response_messages import ResponseMessage
from shared import my_strings
from shared.utils import (
    convert_weekday,
    from_json,
    get_random_string,
    send_html_mail,
    time_in_range,
    to_json,
)
from rest_framework import serializers, exceptions
from appointment.models import Appointment
from django.utils import timezone
from django.db.models import Prefetch, Avg, F, QuerySet
from myapp.settings import DATETIME_FORMAT, DOB_FORMAT
from shared.schedulers import scheduler
from apscheduler.triggers.date import DateTrigger
from firebase_admin.messaging import Message, Notification as FNotification
from fcm_django.models import FCMDevice
import logging, string, threading
logger = logging.getLogger(__name__)
from transaction.models import Transaction, Order, TransactionStatus, TransactionType, TransactionPlatform

class SendNotificationThread(threading.Thread):
    def __init__(self, receiver: User, title: str, message: str, payload: dict = None):
        self.receiver = receiver
        self.title = title
        self.message = message
        self.payload = payload
        threading.Thread.__init__(self)

    def run(self):
        logger.info('Send notification thread running')
        # send notification
        with transaction.atomic():
            notification = Notification(
                user = self.receiver,
                title = self.title,
                message = self.message,
                payload = self.payload
            )
            notification.save()
        devices = FCMDevice.objects.filter(user_id=self.receiver.pk)
        devices.send_message(
            Message(
                data = {'payload': notification.to_json},
                notification = FNotification(notification.title, notification.message)
            )
        )
        logger.info('Pushed notification successfully')

def perform_check_appointment(appointment_id: int):
    """ A job that perform to cancel the appointment 
    if that appointment does not have status AppointmentStatus.IN_PRGRESS
    """
    logger.info('Scheduler has invoked perform_check_appointment jobs')
    try:
        appointment: Appointment = Appointment.objects\
            .select_related('service', 'patient', 'doctor', 'booker')\
            .get(pk=appointment_id, beginAt__isnull=True, status=AppointmentStatus.PENDING)
    except Exception as e:
        logger.warning(f'{e.args[0]}')
        logger.info('No expiry appointment exists')
        return

    now = timezone.now()
    appointment.cancelReason = my_strings.DEFAULT_CANCELLED_REASON
    appointment.endAt = now + timedelta(hours=7)
    appointment.status = AppointmentStatus.CANCELLED
    appointment.isSystemCancelled = True

    serializer = AppointmentSerializer2(appointment)
    appointment.historical = to_json(serializer.data)
    appointment.save()
    logger.info('Auto cancelled appointment succeeded')


def schedule_job(appointment: Appointment, after: timedelta = timedelta(seconds=5)):
    logger.info('Scheduling job...')
    run_date: datetime = appointment.bookedAt + after
    job_id = f'appointmentId={appointment.pk} | run_date={str(run_date)}'
    trigger = DateTrigger(run_date=run_date)
    scheduler.add_job(
        perform_check_appointment,
        trigger,
        args=[appointment.pk],
        replace_existing=True,
        id=job_id,
        misfire_grace_time=None
    )
    scheduler.print_jobs()
    logger.info(f'Job {job_id} has been scheduled')


def _check_duplicate_appointments(booked_at: datetime) -> bool:
    queryset = Schedule.objects.filter(
        bookedAt__lte=booked_at,
        estEndAt__gte=booked_at,
        appointment__status=AppointmentStatus.PENDING
    ).first()
    print('duplicate appointments', queryset)
    return True if queryset else False


def _calculate_estEndAt(booked_at: datetime, doctor: Doctor, type: str):
    # estimatedEnd = Schedule.objects\
    #     .filter(doctor = doctor)\
    #     .aggregate(
    #         avg = Avg(F('estEndAt') - F('bookedAt'))
    #     )
    completed_list = list(Appointment.objects.filter(
        doctor = doctor,
        status = AppointmentStatus.COMPLETED
    ))
    length = len(completed_list)
    if length == 0:
        if type == ServiceCategory.AT_DOCTOR_HOME or type == ServiceCategory.AT_PATIENT_HOME:
            delta = timedelta(minutes = 45)
        else:
            delta = timedelta(minutes = 30)
        return booked_at + delta

    total = timedelta(0)
    for appointment in completed_list:
        total += (appointment.endAt - appointment.beginAt)

    avg = total / length
    estEnd = booked_at + avg
    return datetime(estEnd.year, estEnd.month, estEnd.day, estEnd.hour, estEnd.minute, 0)

class AppointmentSerializer2(serializers.Serializer):
    doctor = serializers.IntegerField(min_value=1)
    patient = serializers.IntegerField(min_value=1)
    package = serializers.IntegerField(min_value=1, required=False)
    bookedAt = serializers.DateTimeField()
    diseaseDescription = serializers.CharField(required=False, max_length=500)
    historical = serializers.JSONField(read_only=True)

    def validate_doctor(self, doctor_id: int):
        try:
            doctor = Doctor.objects.prefetch_related(
                Prefetch(
                    lookup = 'shifts',
                    queryset = WorkingShift.objects.filter(isActive = True, doctor_id = doctor_id)
                )
            ).get(pk = doctor_id)
        except Doctor.DoesNotExist:
            raise CustomValidationError(message=ResponseMessage.NOT_FOUND, detail={
                                        'doctor': f'Not found doctor with id {doctor_id}'})
        except Doctor.MultipleObjectsReturned as e:
            raise e
        return doctor

    def validate_patient(self, patient_id: int):
        try:
            supervisor: User = self.context.get('user')
            patient = Patient.objects.get(pk = patient_id, supervisor_id = supervisor.pk)
        except Patient.DoesNotExist:
            raise CustomValidationError(
                message = ResponseMessage.NOT_FOUND, 
                detail = {
                    'patient': f'Not found patient with id {patient_id}'
                }
            )
        except Patient.MultipleObjectsReturned as e:
            raise e
        return patient

    def validate_bookedAt(self, booked_at: datetime):
        now = timezone.now()
        outbound = now + timedelta(days=30)
        if booked_at < now or booked_at > outbound:
            raise CustomValidationError(
                message = ResponseMessage.DATE_OUT_OF_BOUND,
                detail = {
                    'bookedAt': 'Booking date must be after today and before 30 dates next'
                }
            )
        if _check_duplicate_appointments(booked_at):
            raise CustomValidationError(
                message = ResponseMessage.APPOINTMENT_DUPLICATED, 
                detail = {'bookedAt': 'Booking time is booked by another patient'}
            )
        return booked_at

    def validate_package(self, package_id: int):
        doctor_id: int = self.initial_data['doctor']
        # Change package to service
        ds = DoctorService.objects\
            .select_related('service')\
            .filter(doctor_id = doctor_id, service_id = package_id)\
            .first()
        if not ds:
            raise CustomValidationError(
                message = ResponseMessage.NOT_FOUND,
                detail = {
                    'package': f'Not found package id {package_id} in doctor id {doctor_id}\'s services'
                }
            )
        return ds.service

    def validate(self, data: dict):
        return super().validate(data)

    def _check_if_out_service_hours(self, shifts: QuerySet, booked_at: datetime, estEndAt: datetime):
        converted_weekday = convert_weekday(booked_at)
        # upper_end = booked_at + timedelta(minutes=30)
        # if estEndAt - timedelta(minutes = 30) > booked_at:
        #     upper_end = estEndAt
        found_shift: WorkingShift = shifts.filter(
            weekday = converted_weekday, 
            isActive = True, 
            startTime__lte = booked_at.time(),
            endTime__gte = booked_at.time()
        ).first()
        if not found_shift:
            return True, None
        return False, found_shift

    @transaction.atomic
    def create(self, validated_data: dict):
        logger.info('Creating appointment...')
        supervisor: User = self.context.get('user')
        doctor: Doctor = validated_data['doctor']
        patient: Patient = validated_data['patient']
        service: Service = validated_data['package'] # service here
        booked_at: datetime = validated_data['bookedAt']
        estimateEndAt = _calculate_estEndAt(booked_at = booked_at, doctor = doctor, type = service.category)
        shifts = doctor.shifts.all()
        # check out bound of time
        is_outbound_time, found_shift = self._check_if_out_service_hours(shifts, booked_at, estimateEndAt)
        if is_outbound_time and not found_shift:
            raise CustomValidationError(
                message = ResponseMessage.APPOINTMENT_NOT_ACCEPTED,
                detail = {'bookedAt': 'The time is out of range'}
            )

        # 1. Check duplicated date and time appointment
        queryset = Schedule.objects.filter(
            bookedAt__lte = booked_at,
            estEndAt__gte = booked_at,
            appointment__status = AppointmentStatus.PENDING
        )
        # print('scheduled event ', queryset.query)
        if queryset.exists():
            raise CustomValidationError(
                message = ResponseMessage.APPOINTMENT_DUPLICATED,
                detail = {'error': 'Appointment is duplicated'}
            )
        # 2. Appointments are held at least 1 hour apart
        logger.info('Appointments validation 1 hour apart starting...')

        # Check in code = xxxxxx-supervisorId-patientId-doctorId
        check_in_code = f'{get_random_string(chars = string.digits)}-{supervisor.id}-{patient.id}-{doctor.id}'
        appointment = Appointment(
            doctor = doctor,
            patient = patient,
            booker = supervisor,
            bookedAt = booked_at,
            checkInCode = check_in_code,
            service = service,
            diseaseDescription = validated_data.get('diseaseDescription', None)
        )
        appointment.save()
        logger.info('Valid appointment created...')
        newSchedule = Schedule(
            doctor = doctor,
            bookedAt = appointment.bookedAt,
            content_object = appointment,
        )
        logger.info('new schedule creating')
        newSchedule.estEndAt = estimateEndAt
        newSchedule.type = ScheduleType.APPOINTMENT
        newSchedule.save()
        doctUser = User.objects.filter(doctor = doctor).first()
        order = Order(
            amount = service.price, 
            currency = 'VND',
            code = timezone.now().timestamp.__str__,
            content_object = appointment,
        )
        order.save()
        trans = Transaction(
            amount = service.price, 
            status = TransactionStatus.SUCCESS, 
            sender = supervisor, 
            receiver = doctUser, 
            platform = TransactionPlatform.CASH,
            type = TransactionType.TRANSFERRED,
            order = order
        )
        trans.save()
        logger.info('Creating appointment succeeded')
        try:
            SendNotificationThread(supervisor, 'Đặt lịch thành công', f'Bạn đã hẹn bác sĩ {doctor.firstName} thành công').start()
            SendNotificationThread(doctor.account, 'Thông báo đặt lịch', f'Bạn vừa được xếp lịch với {supervisor.firstName}').start()
        except Exception as e:
            print(e.args)
            pass

        schedule_job(appointment, timedelta(minutes=59))
        # schedule_job(appointment)  # for test scheduler
        
        return appointment

    def to_representation(self, instance: Appointment):
        doctor: Doctor = instance.doctor
        patient: Patient = instance.patient
        service: Service = instance.service
        booker: User = instance.booker

        data = {
            'id': instance.id,
            'bookedAt': instance.bookedAt.strftime(DATETIME_FORMAT),
            'beginAt': instance.beginAt.strftime(DATETIME_FORMAT) if instance.beginAt else None,
            'endAt': instance.endAt.strftime(DATETIME_FORMAT) if instance.endAt else None,
            'checkInCode': instance.checkInCode,
            'category': service.category,
            'status': instance.status,
            'patient': {
                'id': patient.id,
                'firstName': patient.firstName,
                'lastName': patient.lastName,
                'dob': patient.dob.strftime(DOB_FORMAT) if instance.beginAt else None,
                'avatar': patient.avatar,
                'address': patient.address,
            },
            'doctor': {
                'id': doctor.id,
                'firstName': doctor.firstName,
                'lastName': doctor.lastName,
                'age': doctor.age,
                'experienceYears': doctor.experienceYears,
                'gender': doctor.gender,
                'address': doctor.address,
                'avatar': doctor.avatar,
                'rate': round(doctor.totalPoints / doctor.turns, 2) if doctor.turns != 0 else 0,
                'email': doctor.email,
            },
            'booker': {
                'id': booker.pk,
                'firstName': booker.firstName,
                'lastName': booker.lastName,
                'phoneNumber': booker.phoneNumber,
                'email': booker.email
            },
            'package': {
                'id': service.pk,
                'name': service.name,
                'price': service.price,
                'description': service.description,
            }
        }
        return data


class ReadOnlyAppointmentSerializer(serializers.BaseSerializer):

    def to_representation(self, instance: Appointment):
        doctor: Doctor = instance.doctor
        patient: Patient = instance.patient
        service: Service = instance.service
        booker: User = instance.booker
        try:
            schedule: Schedule = instance.cache_schedule[0]
        except:
            schedule = None
            
        return {
            'id': instance.id,
            'bookedAt': instance.bookedAt.strftime(DATETIME_FORMAT),
            'beginAt': instance.beginAt.strftime(DATETIME_FORMAT) if instance.beginAt else None,
            'endAt': instance.endAt.strftime(DATETIME_FORMAT) if instance.endAt else None,
            'estEndAt': schedule.estEndAt.strftime(DATETIME_FORMAT) if schedule else None,
            'category': service.category,
            'checkInCode': instance.checkInCode,
            'status': instance.status,
            'cancelReason': instance.cancelReason,
            'diseaseDescription': instance.diseaseDescription,
            'patient': {
                'id': patient.id,
                'firstName': patient.firstName,
                'lastName': patient.lastName,
                'dob': patient.dob.strftime(DOB_FORMAT) if patient.dob else None,
                'avatar': patient.avatar,
                'address': patient.address,
            },
            'doctor': {
                'id': doctor.id,
                'accountId': doctor.account.pk,
                'firstName': doctor.firstName,
                'lastName': doctor.lastName,
                'age': doctor.age,
                'experienceYears': doctor.experienceYears,
                'gender': doctor.gender,
                'address': doctor.address,
                'avatar': doctor.avatar,
                'rate': round(doctor.totalPoints / doctor.turns, 2) if doctor.turns != 0 else 0,
                'email': doctor.email,
            },
            'booker': {
                'id': booker.pk,
                'firstName': booker.firstName,
                'lastName': booker.lastName,
                'phoneNumber': booker.phoneNumber,
                'email': booker.email
            },
            'package': {
                'id': service.pk,
                'name': service.name,
                'price': service.price,
                'description': service.description,
            }
        }


class RescheduleSerializer(serializers.Serializer):
    bookedAt = serializers.DateTimeField()
    type = serializers.ChoiceField(
        choices=AppointmentType.choices, required=False)

    def validate_bookedAt(self, booked_at: datetime):
        now = timezone.now()
        outbound = now + timedelta(days=30)
        if booked_at < now or booked_at > outbound:
            raise CustomValidationError(
                message = ResponseMessage.DATE_OUT_OF_BOUND,
                detail = {
                    'bookedAt': 'Booking date must be after today and before 30 dates next'
                }
            )
        if _check_duplicate_appointments(booked_at):
            raise CustomValidationError(
                message = ResponseMessage.APPOINTMENT_DUPLICATED,
                detail = {
                    'bookedAt': 'Booking time is already booked'
                }
            )
        return booked_at

    @transaction.atomic
    def update(self, instance: Appointment, validated_data: dict):
        booked_at = validated_data['bookedAt']
        for key, value in validated_data.items():
            if hasattr(instance, key):
                setattr(instance, key, value)
        type = ContentType.objects.get_for_model(Appointment)
        updatedSchedule: Schedule = Schedule.objects.filter(object_id = instance.pk, content_type = type).first()
        if updatedSchedule:
            updatedSchedule.bookedAt = booked_at
            updatedSchedule.estEndAt = _calculate_estEndAt(booked_at = validated_data['bookedAt'], doctor = updatedSchedule.doctor)
            updatedSchedule.save()
        print(instance.bookedAt)
        instance.save()
        return instance

    def to_representation(self, instance: Appointment):
        doctor: Doctor = instance.doctor
        patient: Patient = instance.patient
        # package_meta: PackageMeta = instance.package_meta
        booker: User = instance.booker

        data = {
            'id': instance.id,
            'bookedAt': instance.bookedAt.strftime(DATETIME_FORMAT),
            'beginAt': instance.beginAt.strftime(DATETIME_FORMAT) if instance.beginAt else None,
            'endAt': instance.endAt.strftime(DATETIME_FORMAT) if instance.endAt else None,
            'patient': {
                'id': patient.id,
                'firstName': patient.firstName,
                'lastName': patient.lastName,
                'dob': patient.dob.strftime(DOB_FORMAT) if instance.dob else None,
                'avatar': patient.avatar,
                'address': patient.address,
            },
            'doctor': {
                'id': doctor.id,
                'firstName': doctor.firstName,
                'lastName': doctor.lastName,
                'age': doctor.age,
                'experienceYears': doctor.experienceYears,
                'gender': doctor.gender,
                'address': doctor.address,
                'avatar': doctor.avatar,
                'rate': round(doctor.totalPoints / doctor.turns, 2) if doctor.turns != 0 else 0,
                'email': doctor.email,
            },
            'booker': {
                'id': booker.pk,
                'firstName': booker.firstName,
                'lastName': booker.lastName,
                'phoneNumber': booker.phoneNumber,
                'email': booker.email
            },
            'checkInCode': instance.checkInCode,
            'status': instance.status
        }
        return data

    class Meta:
        fields = ['bookedAt', 'type']
        
class CAppointmentSerializer(serializers.Serializer):
    cancelReason = serializers.CharField(max_length = 500, allow_null = True, allow_blank = True)
    
    def _cancel_by_supervisor(self, appointment: Appointment, validated_data: dict):
        now = timezone.now() + timedelta(hours = 7)
        appointment.status = AppointmentStatus.CANCELLED
        appointment.endAt = now
        appointment.beginAt = now
        appointment.cancelReason = validated_data.get('cancelReason') or 'Hủy bởi người giám hộ'
        appointment.isSupervisorCancelled = True
        appointment.schedule.all().delete()
        app_dict = ReadOnlyAppointmentSerializer(appointment).data
        if appointment.historical is None:
            appointment.historical = to_json(app_dict)
        appointment.schedule.all().delete()
        appointment.save()
        return appointment
    
    def _cancel_by_doctor(self, appointment: Appointment, validated_data: dict):
        now = timezone.now() + timedelta(hours = 7)
        appointment.status = AppointmentStatus.CANCELLED
        appointment.endAt = now
        appointment.beginAt = now
        appointment.cancelReason = validated_data.get('cancelReason') or 'Hủy bởi bác sĩ'
        appointment.isDoctorCancelled = True
        appointment.schedule.all().delete()
        app_dict = ReadOnlyAppointmentSerializer(appointment).data
        if appointment.historical is None:
            appointment.historical = to_json(app_dict)
        appointment.schedule.all().delete()
        appointment.save()
        return appointment
    
    def update(self, appointment: Appointment, validated_data: dict):
        account: User = self.context.get('account')
        if appointment.status == AppointmentStatus.PENDING:
            if account.type == UserType.MEMBER:
                logger.info('Cancelling appointment by supervisor...')
                appointment = self._cancel_by_supervisor(appointment, validated_data)
            else:
                logger.info('Cancelling appointment by doctor...')
                appointment = self._cancel_by_doctor(appointment, validated_data)
            
            logger.info('Cancelled appointment successfully...')
        return appointment
    
    def to_representation(self, instance: Appointment):

        return {
            'id': instance.id,
            'bookedAt': instance.bookedAt.strftime(DATETIME_FORMAT),
            'beginAt': instance.beginAt.strftime(DATETIME_FORMAT) if instance.beginAt else None,
            'endAt': instance.endAt.strftime(DATETIME_FORMAT) if instance.endAt else None,
            # 'category': instance.category,
            'checkInCode': instance.checkInCode,
            'status': instance.status
        }
    
    class Meta:
        fields = ['cancelReason']

class CheckOutSerializer(serializers.Serializer):
    healthRecord = serializers.IntegerField(min_value = 1)
    receiver = serializers.EmailField(max_length = 255)
    
    def validate_healthRecord(self, health_record):
        try:
            return HealthRecord.objects\
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
                    .get(pk = health_record)
        except:
            raise CustomValidationError(message = ResponseMessage.NOT_FOUND, detail = { 'healthRecord': 'Not found' })
        
    def validate_receiver(self, email):
        try:
            return User.objects.get(email = email)
        except:
            raise CustomValidationError(message = ResponseMessage.NOT_FOUND, detail = { 'email': 'Not found' })

    def create(self, validated_data: dict):
        record: HealthRecord = validated_data.get('healthRecord')
        receiver: User = validated_data.get('receiver')
        
        payload = SupervisorHealthRecordSerializer(instance = record).data
        
        print(payload)
        subject = '[HiDoctor] Xin cảm ơn quý khách đã sử dụng dịch vụ của chúng tôi'
        to = [receiver.email]
        send_html_mail(subject, to, 'send_health_record.html', payload)
        return record
    
    class Meta:
        fields = ['healthRecord', 'receiver']