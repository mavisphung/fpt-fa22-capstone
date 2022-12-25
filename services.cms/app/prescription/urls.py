from django.urls import path
from prescription.views import PrescriptionView, DoctorPrescriptionView, HealthRecordPrescriptionView, DoctorPrescriptionDetailView

urlpatterns = [
    path('prescription/', PrescriptionView.as_view()),
    path('prescription/doctor/<int:healthRecord>/', DoctorPrescriptionView.as_view()),
    path('prescription-list/doctor/<int:healthRecord>/', HealthRecordPrescriptionView.as_view()),
    path('prescription-detail/doctor/<int:prescriptionId>/', DoctorPrescriptionDetailView.as_view()),
]
