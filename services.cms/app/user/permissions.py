from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from django.contrib.auth.models import AnonymousUser

from user.models import User, UserType
import logging
logger = logging.getLogger(__name__)

class IsCustomAdmin(BasePermission):
    
    def has_permission(self, request: Request, view) -> bool:
        user = getattr(request, 'user', None)
        if user is None or isinstance(user, AnonymousUser):
            return False
        
        if user.type == UserType.ADMIN and user.is_staff and user.is_active:
            logger.info(f'{user.email} with {user.type} type performed approve action')
            return True

        return False