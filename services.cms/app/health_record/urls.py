
from django.urls import path
from health_record import views

urlpatterns = [
    path('user/health-records/', views.SupervisorListCreateHealthRecordView.as_view(), name = 'supervisor-list-create-health-records'),
    path('doctor/health-records/', views.DoctorCreateHealthRecordView.as_view(), name = 'doctor-list-create-health-records'),
    path('health-records2/', views.ListAllHealthRecordView.as_view(), name = 'get-all-records'),
    path('health-records/<int:pk>/', views.GetHealthRecordView.as_view(), name = 'list_create_health_records'),
    path('doctor/health-records/<int:contract>/', views.DoctorListHealthRecordByContractView.as_view(), name = 'list_records'),
]