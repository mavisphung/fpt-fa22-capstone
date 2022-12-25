from django.urls import path
from service import views

urlpatterns = [
    # path('prescription/', PrescriptionView.as_view()),
    # path('prescription/doctor/<int:healthRecord>/', DoctorPrescriptionView.as_view()),
    # path('prescription-list/doctor/<int:healthRecord>/', HealthRecordPrescriptionView.as_view()),
    path('service/', views.ListServiceView.as_view(), name = 'list-service-api'),
    path('manager/service/', views.ManagerCreateServiceView.as_view(), name = 'manager-create-service-api'),
    path('manager/service/<int:pk>/', views.ManagerRetrieveUpdateDestroyServiceView.as_view(), name = 'manager-create-service-api'),
    path('manager/doctor/<int:doctor_id>/services/<int:service_id>/', views.ManagerRemoveDoctorServiceView.as_view(), name = 'manager-remove-ds-api'),
    # API Search service
    path('api/service/search/', views.SearchServiceView.as_view(), name = 'search-service-api'),
]
