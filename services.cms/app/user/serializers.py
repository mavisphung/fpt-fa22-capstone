from rest_framework import serializers, status, exceptions
from rest_framework.exceptions import ValidationError, APIException
from doctor.models import Doctor
from shared.utils import (
    generate_verify_code, 
    get_group_by_name, 
    get_mail_body, 
    get_random_string, 
    get_resend_body, 
    get_send_code_body, 
    get_user_by_email, 
    send_html_mail, 
    to_json
)
from user.models import Notification, User, UserType, VerificationCode
from shared.models import Gender
from auth.serializers import PasswordField
from shared.formatter import format_response
from shared.exceptions import CustomValidationError
from shared.response_messages import ResponseMessage
from django.db import transaction
from django.utils import timezone
from django.db.models import Prefetch
from django.contrib.auth.password_validation import validate_password
from fcm_django.models import FCMDevice
from myapp import settings
import string
import logging
logger = logging.getLogger(__name__)
class DefaultUserSerializer(serializers.Serializer):
    
    email = serializers.EmailField(max_length = 255)
    password = PasswordField(min_length = 6, max_length = 64)
    repassword = PasswordField(min_length = 6, max_length = 64)
    firstName = serializers.CharField(max_length = 32)
    lastName = serializers.CharField(max_length = 32)
    type = serializers.ChoiceField(UserType.choices)
    phoneNumber = serializers.CharField(min_length = 10, max_length = 15)
    address = serializers.CharField(max_length = 255)
    gender = serializers.ChoiceField(Gender.choices)
    dob = serializers.DateField()
    
    def validate_email(self, email):
        try:
            user = get_user_by_email(email)
        except ValidationError:
            user = None
        if user:
            logger.error('Email validation failed')
            raise ValidationError(f'Email is duplicated')
        return email
        
    def validate_repassword(self, repassword):
        password = self.initial_data.get('password')
        if password != repassword:
            raise ValidationError(f'Password are not matched!')
    
    @transaction.atomic
    def create(self, validated_data):
        group = get_group_by_name(validated_data['type'])
        
        user = User(
            email = validated_data['email'],
            firstName = validated_data['firstName'],
            lastName = validated_data['lastName'],
            gender = validated_data['gender'],
            address = validated_data['address'],
            phoneNumber = validated_data['phoneNumber'],
            type = validated_data['type'],
            dob = validated_data['dob']
        )
        user.is_active = False
        # verification code
        code = VerificationCode(
            # code = get_random_string(size = 6, chars = string.digits),
            code = '123456', # For testing
            user = user,
            expiredAt = timezone.now() + timezone.timedelta(minutes = 5)
        )
        
        # Save instances to database
        user.set_password(validated_data['password'])
        user.save()
        code.save()
        group.user_set.add(user)
        
        # Send mail
        subject = '[CAPSTONE] Welcome to Cứu Bé'
        to = [user.email]
        send_html_mail(subject, to, 'welcome_email_template.html', { 'verify_code': code.code })
        logger.info('User registration performed successfully')
        logger.info(f'A verification code has been sent to {user.email}')
        return user

    def to_representation(self, instance: User):
        # User instance
        return {
            'id': instance.id if instance.id else None,
            'email': instance.email,
            'firstName': instance.firstName,
            'lastName': instance.lastName,
            'gender': instance.gender,
            'phoneNumber': instance.phoneNumber,
            'address': instance.address,
            'type': instance.type
        }
        
    
    class Meta:
        fields = [
            'email', 'password', 'repassword', 
            'firstName', 'lastName', 'phoneNumber',
            'gender', 'address'
        ]
        extra_kwargs = {
            'password': {
                'write_only': True
            },
            'repassword': {
                'write_only': True
            }
        }
        
class ProfileSerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        if not attrs:
            raise ValidationError({'errors': 'Can not fully blanked'})
        
        return super().validate(attrs)
    
    def to_representation(self, instance: User):
        return {
            'email': instance.email,
            'id': instance.pk if instance.type == UserType.MEMBER else instance.doctor_id,
            'firstName': instance.firstName,
            'lastName': instance.lastName,
            'phoneNumber': instance.phoneNumber,
            'address': instance.address,
            'gender': instance.gender,
            'avatar': instance.avatar,
        }
    
    class Meta:
        model = User
        fields = [
            'email', 'id',
            'firstName', 'lastName', 'phoneNumber',
            'gender', 'address', 'avatar'
        ]
        extra_kwargs = {
            'email': {
                'read_only': True
            },
            'id': {
                'read_only': True
            },
            'firstName': {
                'required': False
            },
            'lastName': {
                'required': False
            },
            'phoneNumber': {
                'required': False
            },
            'gender': {
                'required': False
            },
            'address': {
                'required': False
            },
            'avatar': {
                'required': False
            },
        }
        
class ProfileSerializer2(serializers.Serializer):

    firstName = serializers.CharField(max_length = 64)
    lastName = serializers.CharField(max_length = 64)
    phoneNumber = serializers.CharField(max_length = 15)
    address = serializers.CharField(max_length = 255)
    gender = serializers.ChoiceField(choices = Gender.choices)
    dob = serializers.DateField(required = False)
    avatar = serializers.CharField(max_length = 255)
    
    @transaction.atomic
    def update(self, instance: User, validated_data: dict):
        update_fields = ['updatedAt']
        if instance.type == UserType.DOCTOR:
            doctor: Doctor = instance.doctor
            for key, val in validated_data.items():
                if hasattr(instance, key) and hasattr(doctor, key):
                    setattr(instance, key, val)
                    setattr(doctor, key, val)
                    update_fields.append(key)
            instance.save(update_fields = update_fields)
            instance.doctor.save(update_fields = update_fields)
        else:
            for key, val in validated_data.items():
                if hasattr(instance, key):
                    setattr(instance, key, val)
                    update_fields.append(key)
            instance.save(update_fields = update_fields)
            
        return instance
    
    def to_representation(self, instance: User):
        
        return {
            'id': instance.pk,
            'email': instance.email,
            'firstName': instance.firstName,
            'lastName': instance.lastName,
            'phoneNumber': instance.phoneNumber,
            'address': instance.address,
            'gender': instance.gender,
            'avatar': instance.avatar,
            'dob': instance.dob,
            'type': instance.type,
            'tempBalance': instance.tempBalance,
            'mainBalance': instance.mainBalance,
        } if instance.type == UserType.MEMBER else {
            'id': instance.pk,
            'doctorId': instance.doctor_id,
            'email': instance.email,
            'firstName': instance.firstName,
            'lastName': instance.lastName,
            'phoneNumber': instance.phoneNumber,
            'address': instance.address,
            'gender': instance.gender,
            'avatar': instance.avatar,
            'dob': instance.dob,
            'type': instance.type,
            'tempBalance': instance.tempBalance,
            'mainBalance': instance.mainBalance,
        }
    
    class Meta:
        fields = [
            'firstName', 'lastName', 'phoneNumber',
            'gender', 'address', 'avatar'
        ]

class EmailSerializer(serializers.Serializer):
    
    email = serializers.EmailField(
        max_length = 255, 
        write_only = True
    )
    
    code = serializers.CharField(
        max_length = 6,
        min_length = 6,
        write_only = True,
        required = False
    )
    
    @transaction.atomic
    def validate(self, attrs):
        view_name = self.context['view_name']
        now = timezone.now()
        email = attrs['email']
        if view_name == 'ActivateAccountView': # Do activate
            logger.info('ActivateAccountView: EmailSerializer runs validation')
            if 'code' not in attrs:
                raise ValidationError(detail = {'code': 'This field must be included'})
            code = attrs['code']
            user = get_user_by_email(email)
            # Get the latest code
            latest_code: VerificationCode = user.verify_codes.order_by('-createdAt').all().first()
            # Steps for activate:
            # 1. Check if the code is existed
            # 2. Check if the code is match
            # 3. Check if expiry datetime is still after current datetime
            # 4. If all are valid, change user.is_active = True
            if not latest_code: # Step 1
                raise CustomValidationError(message = ResponseMessage.NO_OBJECT_FOUND, detail = {})
            
            if latest_code.code != code or latest_code.isUsed == True: # Step 2
                # When the code is not matched
                raise CustomValidationError(
                    message = ResponseMessage.NO_MATCHED_CODE\
                            if not latest_code.isUsed else ResponseMessage.VERIFY_CODE_USED, 
                    detail = {}
                )
                
            if latest_code.expiredAt < now: # Step 3
                # When the code is expired
                raise CustomValidationError(message = ResponseMessage.VERIFY_CODE_EXPIRED, detail = {})
            
            user.is_active = True
            latest_code.isUsed = True
            user.save(update_fields = ['updatedAt', 'is_active'])
            latest_code.save(update_fields = ['updatedAt', 'isUsed'])
            logger.info('ActivateAccountView: Perform succeeded')
        elif view_name == 'CheckEmailView': # perform check email is existed
            logger.info('CheckEmailView: EmailSerializer runs validation')
            user = get_user_by_email(email)
            attrs['email'] = user # update str -> User object
        elif view_name == 'ResendVerificationCodeView': # Resend verification code
            logger.info('ResendVerificationCodeView: EmailSerializer runs validation')
            user: User = User.objects\
                .filter(email = email)\
                .prefetch_related(
                    Prefetch(
                        'verify_codes',
                        queryset = VerificationCode.objects.filter(user__email = email, isUsed = False).order_by('-createdAt'),
                        to_attr = 'latest_codes'
                    )
                )\
                .first()
                                    
            if not user:
                raise CustomValidationError(
                    message = ResponseMessage.NO_OBJECT_FOUND, 
                    detail = {'user': 'Input email does not exist'}
                )
                
            if user.is_active:
                raise CustomValidationError(
                    message = ResponseMessage.USER_ALREADY_ACTIVE, 
                    detail = {'user': f'{user.email} has already been active'}
                )
            
            # Check if the code expiration is still have 5 minutes, resend the old code else resend a new code
            if len(user.latest_codes) >= 1:
                found_code: VerificationCode = user.latest_codes[0] # Get the first element in list
                
                if now <= found_code.expiredAt and found_code.expiredAt <= now + timezone.timedelta(minutes = 5):
                    # Send mail
                    subject = '[CAPSTONE] Welcome to Cứu Bé'
                    to = [user.email]
                    logger.info('Resend OLD verification code to client')
                    send_html_mail(subject, to, template = 'welcome_email_template.html', context = {'verify_code': found_code.code})
                else:
                    new_code = generate_verify_code(user)
                    subject = '[CAPSTONE] Resend new verification code'
                    to = [user.email]
                    logger.info('Resend NEW verification code to client')
                    send_html_mail(subject, to, template = 'welcome_email_template.html', context = {'verify_code': new_code.code})
            else:
                # list empty that means there is no verification code of that email created -> create one
                new_code = generate_verify_code(user)
                subject = '[CAPSTONE] Welcome new to Cứu Bé 2'
                to = [user.email]
                logger.info('Resend NEW verification code to client 2')
                send_html_mail(subject, to, template = 'welcome_email_template.html', context = {'verify_code': new_code.code})
        
        elif view_name == 'SendVerificationCodeView': # Send verification code
            logger.info('Sent code to email')
            user: User = get_user_by_email(email)
            subject = '[CAPSTONE] Recovery your password'
            to = [user.email]
            old_code: VerificationCode = user.verify_codes.filter(isUsed = False).order_by('-createdAt').first()
            # When send old code:
            #   - when old code is not expired and is not used
            # Else:
            #   - there is no old_code or expired
            if old_code is None or old_code.expiredAt < now:
                new_code = generate_verify_code(user)

            send_html_mail(subject, to, template = 'welcome_email_template.html', context = { 'verify_code': new_code.code if new_code is not None else old_code.code })
        else:
            logger.error('EmailSerializer occurs an APIException: Invalid view to process')
            raise APIException({'error': 'Invalid view to create'})
        return attrs
    
    class Meta:
        fields = ['email', 'code']
        
class PasswordSerializer(serializers.Serializer):
    currentPassword = PasswordField(max_length = 32)
    newPassword = PasswordField(min_length = 8, max_length = 32)
    reNewPassword = PasswordField(min_length = 8, max_length = 32)
    
    def validate(self, attrs):
        user: User = self.context['user']
        currentPassword = attrs['currentPassword']
        newPassword = attrs['newPassword']
        reNewPassword = attrs['reNewPassword']
        
        is_matched: bool = user.check_password(currentPassword)
        if not is_matched:
            raise CustomValidationError(message = ResponseMessage.OLD_PASSWORD_NOT_MATCHED, detail = {})
        
        if currentPassword == newPassword:
            raise CustomValidationError(message = ResponseMessage.PASSWORD_NO_CHANGE, detail = {})
        
        if newPassword != reNewPassword:
            raise CustomValidationError(message = ResponseMessage.PASSWORD_NOT_MATCHED, detail = {})
        
        valided = validate_password(newPassword)
        if valided is not None:
            raise CustomValidationError(message = ResponseMessage.PASSWORD_NOT_PASS_VALIDATORS, detail = {})
        
        return attrs
    
    @transaction.atomic
    def update(self, instance: User, validated_data):
        instance.set_password(validated_data['newPassword'])
        instance.save(update_fields = ['updatedAt', 'password'])
        return instance
        
    
    class Meta:
        fields = ['currentPassword', 'newPassword', 'reNewPassword']
        
class CheckPasswordSerializer(serializers.Serializer):
    currentPassword = PasswordField(max_length = 32)
    
    def validate(self, attrs):
        user: User = self.context['user']
        password = attrs['currentPassword']
        if user.check_password(password):
            return attrs
        raise CustomValidationError(message = ResponseMessage.PASSWORD_NOT_MATCHED, detail = {})
    
    class Meta:
        fields = ['currentPassword']
        
class AuthEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length = 255, write_only = True)
    
    def validate(self, attrs):
        user: User = self.context['user']
        input_email = attrs['email']
        if user.email == input_email:
            raise CustomValidationError(message = ResponseMessage.EMAIL_NO_CHANGE, detail = {})
        
        try:
            input_user = get_user_by_email(input_email)
            print(input_user)
            raise CustomValidationError(message = ResponseMessage.EMAIL_DUPLICATED, detail = {})
        except exceptions.ValidationError as e:
            pass
        
        subject = '[CAPSTONE] Verification code for new email'
        new_code = generate_verify_code(user)
        to = [user.email]
        
        send_html_mail(subject, to, 'welcome_email_template.html', { 'verify_code': new_code.code })
        
        return attrs
    
    class Meta:
        fields = ['email']
        
class RecoveryPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length = 255, write_only = True)
    newPassword = PasswordField(min_length = 8, max_length = 32, write_only = True)
    reNewPassword = PasswordField(min_length = 8, max_length = 32, write_only = True)
    verifyCode = serializers.CharField(min_length = 6, max_length = 6, write_only = True)
    
    def validate_email(self, email):
        logger.info('email validation run')
        user = get_user_by_email(email)
        user.last_code = user.verify_codes.filter(isUsed = False).order_by('-createdAt').first() or None
        return user
    
    def validate_newPassword(self, password):
        logger.info('password validation run')
        is_valid = validate_password(password)
        if is_valid is not None:
            raise CustomValidationError(message = ResponseMessage.PASSWORD_NOT_PASS_VALIDATORS, detail = {})
        return password
    
    def validate_reNewPassword(self, repassword):
        logger.info('validate_reNewPassword invoking...')
        password = self.initial_data.get('newPassword')
        if repassword != password:
            raise CustomValidationError(message = ResponseMessage.PASSWORD_NOT_MATCHED, detail = {})
        return repassword
    
    def validate(self, attrs):
        logger.info('combined validation invoking...')
        user: User = attrs['email']
        code_from_client = attrs['verifyCode']
        last_code: VerificationCode = user.last_code
        # 1. code is match
        # 2. code must not be expired
        # 3. code must not be used
        
        if last_code is None:
            logger.warning('No code available')
            raise CustomValidationError(message = ResponseMessage.VERIFY_CODE_USED, detail = {'verifyCode': 'No code available'})
        
        if last_code.code != code_from_client:
            logger.warning('code is not matched')
            raise CustomValidationError(message = ResponseMessage.VERIFY_CODE_NOT_MATCHED, detail = {'verifyCode': 'Not matched'})
        
        now = timezone.now()
        logger.info(f'timezone.now()', now)
        if last_code.expiredAt < now:
            raise CustomValidationError(message = ResponseMessage.VERIFY_CODE_EXPIRED, detail = {'verifyCode': 'Expired'})

        return attrs
    
    @transaction.atomic
    def save(self) -> User:
        update_fields = ['password', 'updatedAt']
        user: User = self.validated_data['email']    
        newPassword = self.validated_data['newPassword']
        print(user.last_code.__dict__)
        user.set_password(newPassword)
        user.save(update_fields = update_fields)
        user.last_code.isUsed = True
        user.last_code.save(update_fields = ['updatedAt', 'isUsed'])
        
        return user
    
    def to_representation(self, instance):
        print('to_representation', type(instance))
        return super().to_representation(instance)
    class Meta:
        fields = ['email', 'newPassword', 'reNewPassword', 'verifyCode']
        
class UserModelSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['email', 'firstName', 'lastName', 'dob', 'avatar', 'address', 'is_staff', 'is_active', 'type', 'id']
        
class DeviceSerializer(serializers.Serializer):
    user = serializers.IntegerField(min_value = 1)
    registrationToken = serializers.CharField(max_length = 255)
    deviceName = serializers.CharField(max_length = 255)
    deviceId = serializers.CharField(max_length = 255)
    type = serializers.CharField(max_length = 15)
    
    def validate_user(self, user_id: int):
        try:
            found: User = User.objects.get(pk = user_id)
        except Exception as e:
            raise e
        
        return found
    
    @transaction.atomic
    def create(self, validated_data):
        user: User = validated_data['user']
        device_name: str = validated_data['deviceName']
        registration_token: str = validated_data['registrationToken']
        device_id: str = validated_data['deviceId']
        type: str = validated_data['type']
        
        device = FCMDevice(
            registration_id = registration_token,
            device_id = device_id,
            name = device_name,
            type = type,
            user = user
        )
        
        device.save()
        return device
    
    def to_representation(self, instance: FCMDevice):
        return {
            'id': instance.pk,
            'deviceId': instance.device_id,
            'deviceName': instance.name,
        }
    class Meta:
        fields = ['user', 'registrationToken', 'deviceName', 'deviceId', 'type']
        
class ReadOnlyNotificationSerializer(serializers.BaseSerializer):
    
    def to_representation(self, instance: Notification):
        
        return {
            'id': instance.pk,
            'createdAt': instance.createdAt.strftime(settings.DATETIME_FORMAT),
            'title': instance.title,
            'isRead': instance.isRead,
            'message': instance.message,
            'payload': instance.payload,
            'type': instance.type,
        }
    

class ChatMemberSerializer(serializers.BaseSerializer):
    def to_representation(self, instance):
        return {
            'avatar': instance.avatar,
            'fullName': instance.lastName.join(' ').join(instance.firstName)
        }
        
class CreateManagerSerializer(serializers.Serializer):
    
    email = serializers.EmailField(max_length = 255)
    firstName = serializers.CharField(max_length = 32)
    lastName = serializers.CharField(max_length = 32)
    phoneNumber = serializers.CharField(min_length = 10, max_length = 15)
    address = serializers.CharField(max_length = 255)
    gender = serializers.ChoiceField(Gender.choices)
    avatar = serializers.CharField(max_length = 255)
    dob = serializers.DateField()
    
    def validate_email(self, email):
        try:
            user = get_user_by_email(email)
        except ValidationError:
            user = None
        if user:
            logger.error('Email validation failed')
            raise ValidationError(f'Email is duplicated')
        return email
    
    @transaction.atomic
    def create(self, validated_data):
        group = get_group_by_name(UserType.MANAGER)
        
        user = User(
            email = validated_data['email'],
            firstName = validated_data['firstName'],
            lastName = validated_data['lastName'],
            gender = validated_data['gender'],
            address = validated_data['address'],
            phoneNumber = validated_data['phoneNumber'],
            dob = validated_data['dob'],
            type = UserType.MANAGER,
            avatar = validated_data['avatar']
        )
        user.is_active = True
        # Save instances to database
        user.set_password('123456...')
        user.save()
        group.user_set.add(user)
        logger.info('Create manager account succeeded')
        return user

    def to_representation(self, instance: User):
        # User instance
        return {
            'id': instance.pk,
            'email': instance.email,
            'firstName': instance.firstName,
            'lastName': instance.lastName,
            'gender': instance.gender,
            'phoneNumber': instance.phoneNumber,
            'address': instance.address,
            'type': instance.type
        }
        
    class Meta:
        fields = [
            'email', 'firstName', 'lastName', 'phoneNumber',
            'gender', 'address', 'avatar'
        ]