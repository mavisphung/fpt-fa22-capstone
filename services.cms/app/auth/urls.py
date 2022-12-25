from django.urls import path
# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView
# )
from auth import views

urlpatterns = [
    # path('', views.HelloWorldView.as_view(), name = 'hello_world')
    path('login/', views.CustomTokenObtainView.as_view(), name = 'login-url'),
    path('social-login/', views.SocialLoginView.as_view(), name = 'social-login-url'),
]