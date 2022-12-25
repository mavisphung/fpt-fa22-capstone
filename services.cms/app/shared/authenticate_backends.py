from django.contrib.auth.backends import ModelBackend
from rest_framework.authentication import BasicAuthentication

# Use for test custom authentication
class CustomAuthenication(BasicAuthentication):
    def authenticate(self, request):
        print('CustomeAuthentication invoked')
        # print(request.data)
        return super().authenticate(request)