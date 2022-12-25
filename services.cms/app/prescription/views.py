from rest_framework.generics import CreateAPIView, DestroyAPIView, RetrieveAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from doctor.models import Doctor
from prescription.models import Prescription, PrescriptionDetail
from shared.exceptions import CustomValidationError
from shared.formatter import format_response
from user.models import User
from prescription.serializers import PrescriptionSerializer, ReadOnlyPrepsciotionSerializer
from django.db.models import Prefetch
from shared.app_permissions import IsDoctor, IsSupervisor
# Create your views here.


class PrescriptionView(CreateAPIView, DestroyAPIView):
    permission_classes = [IsDoctor]
    serializer_class = PrescriptionSerializer

    def create(self, request: Request, *args, **kwargs):
        data = request.data
        user: User = request.user
        doctor = user.doctor
        detail = data.get('detail', None)
        serializer: PrescriptionSerializer = self.serializer_class(data=data, context={
            'detail': detail,
            'doctor': doctor,
        })
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=201)


class DoctorPrescriptionView(RetrieveAPIView):
    permission_classes = [IsDoctor]
    serializer_class = ReadOnlyPrepsciotionSerializer

    def retrieve(self, request: Request, *args, **kwargs):
        id = kwargs.get('healthRecord')
        doctor: Doctor = request.user.doctor
        prescription = Prescription.objects.prefetch_related(Prefetch(lookup='prescriptiondetail_set', queryset=PrescriptionDetail.objects.all())).filter(healthRecord__pk = id,doctor__pk = doctor.pk)
        serializer = self.get_serializer(instance = prescription,many=True)
        response = format_response(data=serializer.data, success=True, status=200)
        return Response(data=response, status=response['status'])


class HealthRecordPrescriptionView(RetrieveAPIView):
    permission_classes = [IsDoctor]
    serializer_class = ReadOnlyPrepsciotionSerializer

    def retrieve(self, request: Request, *args, **kwargs):
        id = self.kwargs['healthRecord']
        doctor: Doctor = request.user.doctor
        prescription = Prescription.objects.filter(healthRecord__pk= id, healthRecord__doctor = doctor)
        result = self.get_serializer(instance=prescription, many= True)
        response = format_response(data=result.data, success=True, status=200, message='success')
        return Response(response, response['status'])


class DoctorPrescriptionDetailView(RetrieveAPIView):
    permission_classes = [IsDoctor]
    serializer_class = ReadOnlyPrepsciotionSerializer

    def retrieve(self, request: Request, *args, **kwargs):
        id = kwargs.get('prescriptionId', 1)
        doctor: Doctor = request.user.doctor
        prescription = Prescription.objects.prefetch_related(Prefetch(lookup='prescriptiondetail_set', queryset=PrescriptionDetail.objects.filter(prescription__pk = id))).filter(pk = id,doctor__pk = doctor.pk).first()
        if prescription is None:
            raise CustomValidationError(message='Prescription Not Found', detail=f'Not found prescription with id {prescription.pk}', code = 400)
        serializer = self.get_serializer(instance = prescription)
        response = format_response(data=serializer.data, success=True, status=200)
        print(response)
        return Response(data=response, status=response['status'])