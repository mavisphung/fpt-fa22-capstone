from rest_framework.exceptions import APIException, ValidationError
from shared.response_messages import ResponseMessage

class NotActiveUserException(APIException):
    pass

class SocialLoginException(APIException):
    def __init__(self, message = None, detail = None, code = None):
        super().__init__(detail, code)
        if not message:
            message = ResponseMessage.SOCIAL_LOGIN_FAILED
        
        self.message = message

class CustomValidationError(APIException):
    
    def __init__(self, message = None, detail = None, code = None):
        super().__init__(detail, code)
        if not message:
            message = ResponseMessage.INVALID_CUSTOM_ERROR
        
        self.message = message