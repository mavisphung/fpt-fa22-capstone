from django.urls import path
from specialist import views

urlpatterns = [
    # path('prescription/', PrescriptionView.as_view()),
    # path('prescription/doctor/<int:healthRecord>/', DoctorPrescriptionView.as_view()),
    # path('prescription-list/doctor/<int:healthRecord>/', HealthRecordPrescriptionView.as_view()),
    path('specialists/', views.get_all_specialists, name = 'get-all-specialists'),
    path('api/specialists/doctors/', views.get_doctors_follow_specialists, name = 'home-specialists-doctors'),
    path('specialists/<int:pk>/doctors/', views.get_doctors_by_specialist, name = 'get-doctors-by-specialist-id'),
    
    path('doctor/specialists/', views.get_specialists_of_doctor, name = 'get-specialists-of-doctor'),
]
