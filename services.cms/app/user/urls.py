
from django.urls import path
from user import views, wallet_views as wv

urlpatterns = [
    # account management API
    # path('', views.HelloWorldView.as_view(), name = 'hello_world')
    
    path('users/', views.GetUserView.as_view(), name = 'get-users-list'),
    path('register/', views.UserRegistrationView.as_view(), name = 'registration'),
    path('register/device/', views.DeviceRegistrationView.as_view(), name = 'registration-device'),
    path('user/existed/', views.CheckEmailView.as_view(), name = 'check-email-if-existed'),
    path('user/recovery-password/', views.RecoveryPasswordView.as_view(), name = 'recovery-password'),
    
    # user profile
    path('user/me/', views.UserProfileView.as_view(), name = 'user-profile'),
    path('user/activate/', views.ActivateAccountView.as_view(), name = 'activate-account'),
    path('user/send-code/', views.SendVerificationCodeView.as_view(), name = 'send-code'),
    path('user/resend-code/', views.ResendVerificationCodeView.as_view(), name = 'resend-code'),
    path('user/me/change-password/', views.ChangePasswordView.as_view(), name = 'change-password'),
    path('user/me/password/', views.CheckPasswordView.as_view(), name = 'check-password'),
    path('user/me/existed/', views.CheckAuthenticatedEmailView.as_view(), name = 'check-authenticated-email'),
    
    # Get agora token
    path('user/me/agora-token/', views.get_agora_token, name = 'get-agora-token'),
    
    # Notifications
    path('user/me/notifications/', views.GetNotificationView.as_view(), name = 'get-user-notifications'),
    
    # Admin api
    path('admin2/user/<int:pk>/approved/', views.VerifyDoctorAdminView.as_view(), name = 'check-authenticated-email'),
    # path('admin2/manager/', views.CreateManagerView.as_view(), name = 'create-manager-api'),
    
    # Chat info view
    path('user', views.GetChatInfo.as_view(), name = 'chat-member-info'),
    
    path('user/me/deposit/', wv.DepositView.as_view(), name = 'deposit-views'),
    path('user/me/withdraw/', wv.WithdrawalView.as_view(), name = 'withdraw-views'),
]