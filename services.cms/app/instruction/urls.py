from django.urls import path
from instruction.views import (
    CreateMedicalInsturctionView,
    DoctorListHealthRecordMedicalInstructionView, 
    SupervisorListHealthRecordMedicalInstructionView, 
    UpdateMedicalInstructionView,
    ListInstCategoryView,
)

urlpatterns = [
    path('doctor/instruction/', CreateMedicalInsturctionView.as_view(), name='create-medical_instruction'),
    path('doctor/instruction/<int:healthrecord>/', DoctorListHealthRecordMedicalInstructionView.as_view(), name = 'doctor-list-medical_instruction'),
    path('doctor/action/instruction/', UpdateMedicalInstructionView.as_view(), name = 'doctor-update-medical_instruction'),
    path('supervisor/instruction/', SupervisorListHealthRecordMedicalInstructionView.as_view(),name='supervisor-list-medical_instruction'),
    
    # API Get all instruction categories,
    path('instructions-categories/', ListInstCategoryView.as_view(),name='list-medical-instr-categories'),
]
