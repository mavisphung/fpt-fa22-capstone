from django.utils import timezone
from doctor.models import Doctor, WorkingShift
from slot.models import DoctorSlot, DoctorSlotState
from slot.serializers import SupervisorReadonlySerializer, SlotCreateSerializer
from shared.app_permissions import IsSupervisor, IsDoctor
from shared.formatter import format_response
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from shared.utils import WeekDay
from shared.utils import convert_weekday

def createSlotInShift(shift:WorkingShift, durationInMinutes, slotDate, doctor):
    endShift = slotDate.replace(minute= 0, hour=0, second=0) + timezone.timedelta(hours= shift.endTime.hour, minutes= shift.endTime.minute)
    startShift = slotDate.replace(minute= 0, hour=0, second=0) + timezone.timedelta(hours= shift.startTime.hour, minutes= shift.startTime.minute)
    currentSlotTime:timezone.datetime = startShift
    bulk_createds = []
    number_of_slot = (endShift  - startShift) // timezone.timedelta(minutes=durationInMinutes)
    print('slotDate = ', slotDate)
    for index in range(number_of_slot):
        endSlotTime = currentSlotTime + timezone.timedelta(minutes= durationInMinutes)
        slot = DoctorSlot(date = slotDate, start = currentSlotTime, end = endSlotTime, doctor = doctor)
        bulk_createds.append(slot)
        currentSlotTime = endSlotTime
    return DoctorSlot.objects.bulk_create(bulk_createds)

def autoCreateSlot(targetDoctor, fromDate:timezone.datetime, toDate: timezone.datetime):
    today = fromDate.replace(hour= 0 , minute= 0 , second= 0, microsecond = 0)
    lastDay  = toDate.replace(hour= 1 , minute= 0 , second= 0, microsecond = 0)
    different:timezone.timedelta = lastDay - today
    index = 0
    slots = []
    for index in range(different.days):
        print('index' ,index)
        currentDate = today + timezone.timedelta(days = index, hours= 0, minutes= 0, seconds= 0, microseconds= 0)
        weekday  = convert_weekday(currentDate)
        dayshifts = WorkingShift.objects.select_related('doctor').filter(doctor = targetDoctor,weekday = weekday)
        for shift in dayshifts:
            shiftSlot = createSlotInShift(shift, 30 , currentDate, targetDoctor)
            slots = slots + shiftSlot
    return slots

class SlotRetrieveAPIView(ListAPIView):
    permission_classes = [IsSupervisor,IsDoctor]
    serializer_class = SupervisorReadonlySerializer
    def list(self, request:Request, *args, **kwargs):
        doctor_id = request.query_params['doctorId']
        targetDoctor = Doctor.objects.filter(pk = doctor_id).first()
        emptySlots = DoctorSlot.objects.filter(doctor = targetDoctor, status = DoctorSlotState.AVAILABLE)
        serializer = self.get_serializer(instance = emptySlots, many = True)
        response = format_response(data = serializer.data, status = 200, success= True)
        return Response(data = response['data'], status = response['status'])


class AutoCreateSlotAPIView(CreateAPIView):
    permission_classes = [IsDoctor]
    serializer_class = SupervisorReadonlySerializer

    def create(self, request:Request, *args, **kwargs):
        doctor:Doctor = request.user.doctor
        fromDate = timezone.datetime.strptime(request.data['fromDate'], "%Y-%m-%d")
        toDate =  timezone.datetime.strptime(request.data['toDate'], "%Y-%m-%d")
        slots = autoCreateSlot(doctor, fromDate, toDate)
        serializer = self.get_serializer(instance = slots, many = True)
        response = format_response(data = serializer.data, status = 200, success= True)
        return Response(data = response['data'], status = response['status'])