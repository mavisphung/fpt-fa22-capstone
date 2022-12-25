from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers as rest_serializers
from rest_framework import exceptions
from shared.models import LoginPlatform
from shared import exceptions as custom_excs
from rest_framework_simplejwt.settings import api_settings
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import update_last_login
from django.utils.translation import gettext_lazy as _
from user.models import UserType, User
import logging
logger = logging.getLogger(__name__)

class PasswordField(rest_serializers.CharField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("style", {})

        kwargs["style"]["input_type"] = "password"
        kwargs["write_only"] = True

        super().__init__(*args, **kwargs)

class CustomTokenObtainSerializer(rest_serializers.Serializer):
    username_field = get_user_model().USERNAME_FIELD
    # contructor
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields[self.username_field] = rest_serializers.EmailField()
        self.fields["password"] = PasswordField()
        self.fields['type'] = rest_serializers.ChoiceField(
            choices = UserType.choices
        )
    
    @classmethod
    def get_token(cls, user):
        token = RefreshToken.for_user(user)
        
        # Add custom claims
        token['email'] = user.email
        token['firstName'] = user.firstName
        token['lastName'] = user.lastName
        token['type'] = user.type
        # ...

        return token

    default_error_messages = {
        "no_active_account": _("No active account found with the given credentials")
    }
        
    def validate(self, attrs):
        logger.info('CustomTokenObtainSerializer starts to run...')
        authenticate_kwargs = {
            self.username_field: attrs[self.username_field],
            # 'email': attrs['email'],
            "password": attrs["password"],
            'type': attrs['type']
        }
        try:
            authenticate_kwargs["request"] = self.context["request"]
        except KeyError:
            pass

        user: User = authenticate(**authenticate_kwargs)
        
        if user is None:
            raise exceptions.AuthenticationFailed(
                {'detail': 'Wrong email or password'}
            )
        
        if user.type != attrs['type']:
            raise exceptions.PermissionDenied()
        
        if user.type == UserType.DOCTOR and user.doctor.isApproved == False:
            raise exceptions.PermissionDenied()
        
        # print(dir(self.user.groups))
        # print(self.user.groups._prefetched_objects_cache)
        if not api_settings.USER_AUTHENTICATION_RULE(user):
            raise exceptions.AuthenticationFailed(
                self.error_messages["no_active_account"],
                "no_active_account",
            )
        
        data = {}
        refresh_token: RefreshToken = self.get_token(user)
        
        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, user)
            
        data['accessToken'] = str(refresh_token.access_token)
        fields = [
            'id', 'email', 'firstName', 
            'lastName', 'type', 'address', 
            'gender', 'phoneNumber', 'avatar', 
        ]
        for field in fields:
            value = getattr(user, field)
            data[field] = value or None
        # data['info'] = {
        #     'id': user.id,
        #     'email': user.email,
        #     'firstName': user.firstName,
        #     'lastName': user.lastName,
        #     'type': user.type,
        #     'address': user.address,
        #     'gender': user.gender,
        #     'phoneNumber': user.phoneNumber,
        #     'avatar': user.avatar if user.avatar else None
        #     # ...
        # }
        data['tempBalance'] = user.tempBalance
        data['mainBalance'] = user.mainBalance
        
        if user.type == UserType.DOCTOR:
            data['doctorId'] = user.doctor_id
        logger.info('CustomTokenObtainSerializer runs successfully')
        return data
    
class SocialSerializer(rest_serializers.Serializer):
    
    platform = rest_serializers.ChoiceField(
        choices = LoginPlatform.choices
    )
    id = rest_serializers.CharField(
        max_length = 355
    )
    
    class Meta:
        fields = ['platform', 'id']