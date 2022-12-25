from rest_framework.response import Response
from rest_framework import permissions
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics, exceptions
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from shared.utils import get_group_by_name, get_random_string
from user.models import User, UserType
from shared.models import LoginPlatform
from shared.response_messages import ResponseMessage
from shared.formatter import format_response
from auth.serializers import CustomTokenObtainSerializer, SocialSerializer
from django.utils import timezone
import requests, string
import logging
logger = logging.getLogger(__name__)

class CustomTokenObtainView(TokenObtainPairView):
    serializer_class = CustomTokenObtainSerializer
    permission_classes = [permissions.AllowAny]
    
    def post(self, request, *args, **kwargs):
        serializer: CustomTokenObtainSerializer = self.get_serializer(data = request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        response = format_response(
            status = 201,
            message = ResponseMessage.LOGIN_SUCCEEDED,
            data = serializer.validated_data
        )
        return Response(response, response['status'])

class SocialLoginView(generics.CreateAPIView):
    
    serializer_class = SocialSerializer
    permission_classes = [permissions.AllowAny]
    
    def perform_login_with_google(self, key: str) -> Response:
        """
        The function that perform login with gmail
        
        There are some cases:
        - Case 1: User has registered email and use login_with_google button with role MEMBER, DOCTOR
        - Case 2: User has resistered email but never use login_with_google before with role MEMBER, DOCTOR: Link User to google email
        - Case 3: User has NOT registered email and use login_with_google button with role MEMBER: NEW COMPLETEDLY USER
        - Case 4: User has NOT registered email and use login_with_google button with role DOCTOR: REGISTERED as a DOCTOR -> need admin approve
        """
        base_url = "https://www.googleapis.com/oauth2/v1/userinfo"
        params = {
            'access_token': key
        }
        try:
            res = requests.get(url = base_url, params = params)
            print(res.status_code)
            print(res.text)
        except Exception as e:
            logger.error('Auth module: Login with Google error')
            logger.error(str(e.args))
            raise exceptions.APIException(detail = {'errors': e.args})
        
        if res.status_code >= 400 and res.status_code <= 499:
            logger.error(f'Login with Google API has occured error with status code {res.status_code}')
            response = format_response(
                success = False,
                status = res.status_code,
                message = ResponseMessage.SOCIAL_LOGIN_FAILED,
                data = res.json()
            )
            return Response(response, response['status'])
        
        body = res.json()
        # """
        # {
        #     "id": "106767439546115547624",
        #     "email": "huypc2410@gmail.com",
        #     "verified_email": true,
        #     "name": "Huy Phùng",
        #     "given_name": "Huy",
        #     "family_name": "Phùng",
        #     "picture": "https://lh3.googleusercontent.com/a-/AOh14GjKaj1gSZgt1SuE_HnlR2q7GncqM73Tq8Qc5q6q=s96-c",
        #     "locale": "vi"
        # }
        # """
        email = body['email']
        user: User = User.objects.filter(email = email).first()
        print(type(body))
        print(body)
        ret_data = {}
        if user:
            # has resistered email but never use login_with_google before with role MEMBER
            if user.type == UserType.MEMBER and user.googleId is None:
                logger.info(f'Email {user.email} is existed so that it will link to googleId')
                user.googleId = body['id']
                user.last_login = timezone.now()
                user.save(update_fields = ['updatedAt', 'googleId', 'last_login'])
            
            # If googleId is already existed then return JWT and user info
        else:
            # has NOT registered email and use login_with_google with role MEMBER
            member_group = get_group_by_name(UserType.MEMBER)
            
            user = User(
                email = body['email'],
                is_active = body['verified_email'],
                firstName = body['given_name'],
                lastName = body['family_name'],
                avatar = body['picture'] if body['picture'] else None,
                googleId = body['id'],
                type = UserType.MEMBER
            )
            
            random_password = get_random_string(size = 8, chars = string.ascii_letters + string.digits)
            user.set_password(random_password)
            user.last_login = timezone.now()
            user.save()
            member_group.user_set.add(user)
        # Return JWT and user info
        token: RefreshToken = CustomTokenObtainSerializer.get_token(user)
        ret_data['accessToken'] = str(token.access_token)
        ret_data |= {
            'id': user.id,
            'email': user.email,
            'firstName': user.firstName,
            'lastName': user.lastName,
            'type': user.type,
            'address': user.address,
            'gender': user.gender,
            'phoneNumber': user.phoneNumber,
            'avatar': user.avatar if user.avatar else None,
            'tempBalance': user.tempBalance,
            'mainBalance': user.mainBalance
        }
        
        response = format_response(
            success = True,
            status = 201,
            message = ResponseMessage.SOCIAL_LOGIN_SUCCEEDED,
            data = ret_data
        )
        return Response(response, response['status'])
    
    def create(self, request, *args, **kwargs):
        serializer: SocialSerializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        
        platform = serializer.data['platform']
        if platform == LoginPlatform.GOOGLE:
            response = self.perform_login_with_google(serializer.data['id'])
        elif platform == LoginPlatform.FACEBOOK:
            pass
        
        return response