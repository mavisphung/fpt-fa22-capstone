
from django.urls import path
from patient import views

urlpatterns = [
    # account management API
    # path('', views.HelloWorldView.as_view(), name = 'hello_world')
    path('user/patients/<int:pk>', views.PatientProfileView.as_view(), name = 'get_patient_by_id'),
    path('user/patients/', views.PatientProfileView.as_view(), name = 'add_patient_api'),
    path('user/patients/data/', views.ListUserPatientView.as_view(), name = 'add_patient_api'),
]