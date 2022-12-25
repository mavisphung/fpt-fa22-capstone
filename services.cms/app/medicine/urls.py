from django.urls import path
from medicine import views

urlpatterns = [
    # path('prescription/', PrescriptionView.as_view()),
    # path('prescription/doctor/<int:healthRecord>/', DoctorPrescriptionView.as_view()),
    # path('prescription-list/doctor/<int:healthRecord>/', HealthRecordPrescriptionView.as_view()),
    path('medicines/', views.ListMedicinesView.as_view(), name = 'list-medicines'),
]
