from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from doctor.repositories import generate_shifts
from service.models import DoctorService, Service
from shared.exceptions import CustomValidationError
from specialist.models import DoctorSpecialist, Specialist
from shared.response_messages import ResponseMessage
from doctor.models import Doctor, PackageCategory, Specification, WorkingShift, Package
from user.models import User, UserType
from shared.models import Gender
from shared.utils import EmailThread, check_valid_email, get_group_by_name
from django.db import transaction
from myapp.settings import DATETIME_FORMAT, DOB_FORMAT
from django.utils import timezone
from asgiref.sync import async_to_sync

import logging
logger = logging.getLogger(__name__)

class SpecificationSerializer(serializers.Serializer):
    url = serializers.URLField()
    ext = serializers.CharField(max_length = 5)
    
    def validate_ext(self, ext):
        allowed = ['zip', 'rar', 'pdf', 'docx', 'docx', 'jpg', 'jpeg', 'png', 'svg']
        if ext not in allowed:
            raise ValidationError(f'extension must be in {allowed}')
        return ext

class ReadOnlyDoctorSerializer(serializers.BaseSerializer):

    def to_representation(self, instance: Doctor):
        return {
            'id': instance.pk,
            'email': instance.email,
            'phoneNumber': instance.phoneNumber,
            'firstName': instance.firstName,
            'lastName': instance.lastName,
            'ratingPoints': instance.totalPoints,
            'ratingTurns': instance.turns,
            'address': instance.address,
            'avatar': instance.avatar if instance.avatar else None,
            'dob': instance.dob.strftime(DOB_FORMAT) if instance.dob else None,
            'experienceYears': instance.experienceYears,
            'gender': instance.gender,
            'phoneNumber': instance.phoneNumber,
        }

class ReadOnlyDoctorSerializer2(serializers.BaseSerializer):

    def to_representation(self, instance: Doctor):
        return {
            'id': instance.pk,
            'email': instance.email,
            'phoneNumber': instance.phoneNumber,
            'firstName': instance.firstName,
            'lastName': instance.lastName,
            'ratingPoints': instance.totalPoints,
            'ratingTurns': instance.turns,
            'address': instance.address,
            'avatar': instance.avatar if instance.avatar else None,
            'dob': instance.dob.strftime(DOB_FORMAT) if instance.dob else None,
            'experienceYears': instance.experienceYears,
            'gender': instance.gender,
            'phoneNumber': instance.phoneNumber,
            'isApproved': instance.isApproved,
            'specialist': {
                'id': instance.specialist_id,
                'name': instance.specialist_name,
                'description': instance.specialist_desc,
            }
        }
        
class _ReadOnlySpecialistSerializer(serializers.BaseSerializer):
    """DoctorSpecialist serializer

    Args:
        instance (DoctorSpecialist)
    """
    def to_representation(self, instance: DoctorSpecialist):
        return {
            'id': instance.specialist_id,
            'name': instance.specialist.name,
            'description': instance.specialist.description,
        }
class DoctorSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only = True)
    email = serializers.EmailField(max_length = 255)
    firstName = serializers.CharField(max_length = 64)
    lastName = serializers.CharField(max_length = 64)
    dob = serializers.DateField()
    avatar = serializers.URLField(max_length = 255)
    phoneNumber = serializers.CharField(min_length = 10, max_length = 10)
    address= serializers.CharField(max_length = 255)
    gender = serializers.ChoiceField(
        choices = Gender.choices
    )
    experienceYears = serializers.IntegerField()
    specs = serializers.ListSerializer(
        child = SpecificationSerializer()
    )
    specialists = serializers.ListField(
        child = serializers.IntegerField(min_value = 1),
        allow_empty = False
    )
    
    def validate_email(self, email):
        logger.info('DoctorSerializer run email validation')
        if not check_valid_email(email):
            raise CustomValidationError(message = ResponseMessage.EMAIL_WRONG_FORMAT, detail = {'email': "Invalid email format"})
        doctor_user: User = User.objects.filter(email = email).first()
        if doctor_user:
            raise CustomValidationError(message = ResponseMessage.EMAIL_DUPLICATED, detail = {'email': "The email has been existed"})
        
        return email
    
    def validate_specialists(self, specialists: list):
        logger.info('Validating specialists')
        if not specialists:
            raise CustomValidationError(message = ResponseMessage.INVALID_INPUT, detail = { 'specialists': 'Not allow empty' })
        
        ret_list = Specialist.objects.filter(pk__in = specialists)
        
        try:
            ret_list[0]
        except:
            raise CustomValidationError(message = ResponseMessage.INVALID_INPUT, detail = { 'specialists': 'Not found' })
        
        return list(ret_list)
    
    def _create_specs(self, doctor: Doctor, specs_list: list) -> list:
        ret_specs = []
        for spec in specs_list:
            temp = Specification(
                doctor = doctor,
                url = spec['url'],
                type = spec['ext']
            )
            ret_specs.append(temp)
        return ret_specs
    
    @transaction.atomic
    def create(self, validated_data: dict):
        # specifications
        specs_list = validated_data.pop('specs')
        
        # specialists
        specialists: list = validated_data.pop('specialists')
        
        doctor = Doctor(isApproved = False)
        for key, value in validated_data.items():
            if key != 'specs' and hasattr(doctor, key):
                setattr(doctor, key, value)
        doctor.save()
        if specs_list:
            logger.info('Adding spefications...')
            specs = self._create_specs(doctor, specs_list)
            Specification.objects.bulk_create(specs)
            
        logger.info('Adding specialists...')
        temp_specialists = []
        for item in specialists:
            temp_specialists.append(DoctorSpecialist(doctor = doctor, specialist = item))
        
        DoctorSpecialist.objects.bulk_create(temp_specialists)
        return doctor
    
    def _convert_specs_to_list(self, data: list):
        ret_list = []
        for item in data:
            temp_dict = {}
            temp_dict['url'] = item.url
            temp_dict['type'] = item.type
            ret_list.append(temp_dict)
        return ret_list
    
    def _convert_shifts_to_list(self, data):
        ret_list = []
        for item in data:
            temp = {}
            item: WorkingShift = item
            temp['id'] = item.pk
            temp['weekday'] = item.weekday
            temp['startTime'] = item.startTime
            temp['endTime'] = item.endTime
            temp['isActive'] = item.isActive
            ret_list.append(temp)
        return ret_list
    
    def to_representation(self, instance: Doctor):
        data = {}
        data['id'] = instance.id
        data['accountId'] = instance.account.pk
        data['email'] = instance.email
        data['firstName'] = instance.firstName
        data['lastName'] = instance.lastName
        data['age'] = instance.age
        data['dob'] = instance.dob.strftime(DOB_FORMAT) if instance.dob else None
        data['phoneNumber'] = instance.phoneNumber
        data['isApproved'] = instance.isApproved
        data['avatar'] = instance.avatar if instance.avatar else None
        data['experienceYears'] = instance.experienceYears
        data['gender'] = instance.gender
        data['ratingPoints'] = instance.totalPoints
        data['ratingTurns'] = instance.turns
        data['address'] = instance.address
        data['specs'] = self._convert_specs_to_list(instance.specs.all())
        data['shifts'] = self._convert_shifts_to_list(instance.shifts.all())
        if hasattr(instance, 'specialist_list'):
            data['specialists'] = _ReadOnlySpecialistSerializer(instance.specialist_list, many = True).data
        return data
        
    
    class Meta:
        fields = [
            'firstName', 'lastName', 'dob', 
            'avatar', 'phoneNumber', 'address',
            'gender', 'age', 'experienceYear', 'id', 
            'specs', 'email',
        ]
        
class WorkingShiftSerializer(serializers.Serializer):
    id = serializers.IntegerField(min_value = 1, required = False)
    weekday = serializers.IntegerField(min_value = 1, max_value = 7)
    startTime = serializers.TimeField()
    endTime = serializers.TimeField()
    isActive = serializers.BooleanField()
    
    def validate(self, attrs):
        super().validate(attrs)
        if attrs['startTime'] >= attrs['endTime']:
            raise CustomValidationError(message = ResponseMessage.END_LESS_THAN_START, detail = {'time': 'End time must be after start time'})
        logger.info('Validated shifts succeeded')
        return attrs
    
    def to_representation(self, instance: WorkingShift):
        return {
            'id': instance.pk,
            'weekday': instance.weekday,
            'startTime': str(instance.startTime),
            'endTime': str(instance.endTime),
            'isActive': instance.isActive
        }
    
    class Meta:
        fields = ['id', 'weekday', 'startTime', 'endTime', 'isActive']
        
class ManyWorkingShiftSerializer(serializers.Serializer):
    shifts = serializers.ListSerializer(
        child = WorkingShiftSerializer()
    )
    newShifts = serializers.ListSerializer(
        allow_empty = True,
        child = WorkingShiftSerializer()
    )
    @transaction.atomic
    def update(self, instance: list, validated_data: dict):
        logger.info('Update list running')
        doctor_account: User = self.context['doctor_account']
        doctor = doctor_account.doctor
        # update
        data: list = validated_data['shifts']
        updatedAt = timezone.now()
        for index, value in enumerate(data):
            shift: WorkingShift = instance[index]
            if shift.pk != value['id']:
                raise CustomValidationError(message = ResponseMessage.INVALID_ID)
            setattr(shift, 'startTime', value['startTime'])
            setattr(shift, 'endTime', value['endTime'])
            setattr(shift, 'isActive', value['isActive'])
            setattr(shift, 'updatedAt', updatedAt)
        WorkingShift.objects.bulk_update(instance, fields = ['startTime', 'endTime', 'isActive', 'updatedAt'])
        
        # create
        create_list: list = validated_data['newShifts']
        if len(create_list) > 0:
            logger.info('Creating new shifts')
            for index, new_shift in enumerate(create_list):
                temp = WorkingShift(doctor = doctor, **new_shift)
                create_list[index] = temp
            WorkingShift.objects.bulk_create(create_list)
            instance.extend(create_list)
        return instance
    
    def to_representation(self, instance: list[WorkingShift]):
        ret_dict = dict()
        for item in instance:
            if item.weekday in ret_dict:
                shift_list: list = ret_dict[item.weekday]
                shift_list.append({
                    'id': item.pk,
                    'weekday': item.weekday,
                    'startTime': item.startTime,
                    'endTime': item.endTime,
                    'isActive': item.isActive,  
                })
            else:
                new_list = []
                new_list.append({
                    'id': item.pk,
                    'weekday': item.weekday,
                    'startTime': item.startTime,
                    'endTime': item.endTime,
                    'isActive': item.isActive,  
                })
                ret_dict[item.weekday] = new_list
        return ret_dict
    
    class Meta:
        fields = ['shifts', 'newShifts']
    
class ViewPackageSerializer(serializers.BaseSerializer):
    
    def to_representation(self, instance: Package):
        return {
            'id': instance.pk,
            'name': instance.name,
            'description': instance.description,
            'price': instance.price,
            'category': instance.category
        }
        
class PackageSerializer(serializers.Serializer):
    
    name = serializers.CharField(max_length = 64)
    description = serializers.CharField(max_length = 255)
    price = serializers.FloatField(min_value = 0.0)
    category = serializers.ChoiceField(choices = PackageCategory.choices)
    
    class Meta:
        fields = ['name', 'description', 'price']
        
class ManyPackageSerializer(serializers.Serializer):
    packages = serializers.ListSerializer(
        child = PackageSerializer()
    )
    
    @transaction.atomic
    def save(self, **kwargs):
        doctor: Doctor = self.context.get('doctor')
        packages = self.validated_data['packages']
        package_list = []
        for item in packages:
            package = Package(doctor = doctor, **item)
            package_list.append(package)
        Package.objects.bulk_create(package_list)
        
        return package_list
    class Meta:
        fields = ['packages']
        
class ReadOnlySpecialistSerializer(serializers.BaseSerializer):
    
    def to_representation(self, instance: DoctorSpecialist):
        return {
            'id': instance.specialist_id,
            'name': instance.specialist.name,
            'description': instance.specialist.description,
        }
class DoctorSerializer2(serializers.Serializer):
    
    email = serializers.EmailField(max_length = 255)
    firstName = serializers.CharField(max_length = 64)
    lastName = serializers.CharField(max_length = 64)
    dob = serializers.DateField(required = False)
    gender = serializers.ChoiceField(choices = Gender.choices, required = False)
    avatar = serializers.URLField(max_length = 255)
    phoneNumber = serializers.CharField(min_length = 10, max_length = 20, required = False)
    address = serializers.CharField(max_length = 255, required = False)
    specialists = serializers.ListField(
        child = serializers.IntegerField(min_value = 1),
        allow_empty = False
    )
    
    def validate_email(self, email):
        logger.info('DoctorSerializer2 run email validation')
        if not check_valid_email(email):
            raise CustomValidationError(message = ResponseMessage.EMAIL_WRONG_FORMAT, detail = {'email': "Invalid email format"})
        doctor_user: User = User.objects.filter(email = email, doctor__email = email).first()
        if doctor_user:
            raise CustomValidationError(message = ResponseMessage.EMAIL_DUPLICATED, detail = {'email': "The email has been existed"})
        
        return email
    
    def validate_specialists(self, specialists: list):
        logger.info('DoctorSerializer2 run specialists validation')
        found_specialists = Specialist.objects.filter(pk__in = specialists)
        if found_specialists.count() != len(specialists):
            raise CustomValidationError(message = ResponseMessage.INVALID_INPUT, detail = {'specialists': "Including invalid specialist"})
        return list(found_specialists)
    
    @transaction.atomic
    def create(self, validated_data: dict):
        raw_password = '123456...'
        doctor_group = get_group_by_name(UserType.DOCTOR)
        logger.info('DoctorSerializer2 creating doctor')
        specialists = validated_data.pop('specialists')
        
        doctor = Doctor(**validated_data)
        doctor.isApproved = True
        
        account = User(**validated_data)
        account.is_staff = False
        account.is_active = True
        account.set_password(raw_password)
        account.type = UserType.DOCTOR
        account.doctor = doctor
        
        doctor.save()
        account.save()
        doctor_group.user_set.add(account)
        
        doctor_specialists = []
        for item in specialists:
            doctor_specialists.append(DoctorSpecialist(doctor = doctor, specialist = item))
        
        DoctorSpecialist.objects.bulk_create(doctor_specialists)
        logger.info('Create doctor')
        
        shifts = generate_shifts(doctor)
        WorkingShift.objects.bulk_create(shifts)
        
        EmailThread(
            subject = '[ĐĂNG KÝ] Chào mừng bạn đã đến với hệ thống HiDoctor',
            body = f'Mật khẩu của bạn là: {raw_password}',
            to = [doctor.email]
        ).start()
        
        return doctor
    
    def to_representation(self, instance: Doctor):
        # specialists = instance.specialists.select_related('specialist').all()
        specialists = DoctorSpecialist.objects.select_related('specialist').filter(doctor_id = instance.pk)
        specs_serializer = ReadOnlySpecialistSerializer(specialists, many = True)
        return {
            'id': instance.pk,
            'firstName': instance.firstName,
            'lastName': instance.lastName,
            'phoneNumber': instance.phoneNumber,
            'address': instance.address,
            'avatar': instance.avatar,
            'gender': instance.gender,
            'specialists': specs_serializer.data,
        }
        
    
    class Meta:
        fields = ['email', 'firstName', 'lastName', 'dob', 'gender', 'specialists']
        
class ManyDoctorServiceSerializer(serializers.Serializer):
    services = serializers.ListField(
        child = serializers.IntegerField(min_value = 1),
        allow_empty = False
    )
    
    def validate_services(self, services: list[int]):
        doctor: Doctor = self.context['doctor']
        
        # remove duplicate
        services = set(services)
        
        ds_exists = DoctorService.objects.filter(doctor_id = doctor.pk, service_id__in = services)
        dss = { ds.service_id for ds in ds_exists }
        
        # set subtract by set
        creates = services - dss
        return creates
    
    # @transaction.atomic
    def create(self, validated_data: dict):
        logger.info('Creating services for doctor')
        service_ids = validated_data['services']
        services = Service.objects.filter(id__in = service_ids)
        services = list(services)
        
        if service_ids == 0:
            return []
        
        if len(services) != len(service_ids):
            raise CustomValidationError(message = ResponseMessage.INVALID_INPUT, detail = {'services': 'invalid service'})
        
        doctor: Doctor = self.context['doctor']
        temp_list = [ DoctorService(doctor = doctor, service = service) for service in services ]
        async_to_sync(DoctorService.objects.abulk_create)(temp_list)
        logger.info('Creating services successfully')
        return temp_list
    
    def to_representation(self, ds_list: list[DoctorService]):
        ret_list = []
        for ds in ds_list:
            ret_list.append({
                'id': ds.pk,
                'doctor': {
                    'id': ds.doctor_id,
                    'firstName': ds.doctor.firstName,
                    'lastName': ds.doctor.lastName,
                },
                'service': {
                    'id': ds.service_id,
                    'name': ds.service.name,
                    'description': ds.service.description,
                    'price': ds.service.price,
                    'category': ds.service.category,
                }
            })
        return ret_list
    
    class Meta:
        fields = ['services']
        
class DSSerializer(serializers.BaseSerializer):
    
    def to_representation(self, instance: DoctorService):
        return {
            'id': instance.pk,
            'doctor': {
                'id': instance.doctor_id,
                'firstName': instance.doctor.firstName,
                'lastName': instance.doctor.lastName,
            },
            'service': {
                'id': instance.service_id,
                'name': instance.service.name,
                'description': instance.service.description,
                'price': instance.service.price,
                'category': instance.service.category,
            },
            'isActive': instance.isActive
        }

class UpdateDSSerializer(serializers.Serializer):
    
    service = serializers.IntegerField(min_value = 1)
    
    def validate_service(self, service_id: int):
        doctor_id = self.context['doctor_id']
        service = DoctorService.objects.filter(
            doctor_id = doctor_id,
            service_id = service_id
        ).first()
        if service:
            raise CustomValidationError(message = ResponseMessage.INVALID_INPUT, detail = {'service': f'This service is registered by doctor id {doctor_id}'})
        
        return service_id
    
    def update(self, instance: DoctorService, validated_data: dict):
        new_service: Service = validated_data['service']
        instance.service_id = new_service
        instance.save(update_fields = ['updatedAt', 'service_id'])
        return instance
    
    def to_representation(self, instance: DoctorService):
        return {
            'id': instance.pk,
            'doctor': {
                'id': instance.doctor_id,
                'firstName': instance.doctor.firstName,
                'lastName': instance.doctor.lastName,
            },
            'service': {
                'id': instance.service_id,
                'name': instance.service.name,
                'description': instance.service.description,
                'price': instance.service.price,
            },
            'isActive': instance.isActive
        }
    
    class Meta:
        fields = ['service']