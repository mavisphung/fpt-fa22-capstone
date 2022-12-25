from datetime import datetime, time, timedelta
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import generics, permissions
from doctor.models import Doctor, WorkingShift
from schedule.models import Schedule
from appointment.models import Appointment
from shared.app_permissions import IsSupervisor
from shared.formatter import format_response
from shared.models import AppointmentStatus, WeekDay
from shared.paginations import get_paginated_response
from shared.utils import convert_weekday, time_to_int, ceil_dt
from shared.response_messages import ResponseMessage
from user.models import User
from datetimerange import DateTimeRange
from django.db.models import Prefetch
from django.db.models.query import prefetch_related_objects
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
import logging
logger = logging.getLogger(__name__)

def format(begin, end):
    time_format = '%H:%M:%S'
    return {
        'from': begin.strftime(time_format), 
        'end': end.strftime(time_format)
    }



def caculateAvailableTimes(selected_date: datetime, doctor_id: int):
    dayOfWeek: WeekDay = convert_weekday(selected_date)
    # upperlimits = datetime(day=selected_date.day, month= selected_date.month, year= selected_date.year, hour=23, minute=59, second=59)
    todayShifts = WorkingShift.objects.select_related('doctor')\
        .filter(
            weekday = dayOfWeek, 
            doctor_id = doctor_id, 
            startTime__gte = selected_date
        )
    # slots = Schedule.objects.filter(doctor=doctor,
    #          bookedAt__gte=selected_date, bookedAt__lte=upperlimits)
    availableSlot = list()
    for shift in todayShifts:
        currentShift: WorkingShift = shift
        slots = Schedule.objects.filter(
            doctor_id = doctor_id,
            bookedAt__date = selected_date.date(),
            bookedAt__time__gte = currentShift.startTime,
            bookedAt__time__lte = currentShift.endTime).order_by('bookedAt')
        count = slots.count()
        traversalSlot = []
        index = 0
        for slot in slots:
            print('slot.bookedAt', slot.bookedAt)
            traversalSlot.append(slot)
            currentSlot: Schedule = slot
            if index != 0 and (index != count - 1) and count != 1:
                prevSlot: Schedule = traversalSlot[index-1]
                tuble = format(prevSlot.estEndAt, currentSlot.bookedAt)
                availableSlot.append(tuble)
                print('47', True)
            if index == 0 and count >= 1:
                currentShift: WorkingShift = shift
                startShiftTime: time = currentShift.startTime
                startAvailable = time(
                    hour=startShiftTime.hour, minute=startShiftTime.minute)
                tuple = format(startAvailable, currentSlot.bookedAt)
                availableSlot.append(tuple)
                print('55 id - bookedAt', currentSlot.pk,currentSlot.bookedAt)
                print('55', True)
            if index == count - 1 and count != 1:
                currentShift: WorkingShift = shift
                endShiftTime: time = currentShift.endTime
                endAvailable = time(
                    hour=endShiftTime.hour, minute=endShiftTime.minute)
                prevSlot: Schedule = traversalSlot[index-1]
                tuble = format(prevSlot.estEndAt, currentSlot.bookedAt)
                availableSlot.append(tuble)
                tuple = format(currentSlot.estEndAt, endAvailable)
                availableSlot.append(tuple)
                print('66 id - bookedAt', currentSlot.pk,currentSlot.bookedAt)
                print('66', True)
            index = index + 1
            
    # availableSlot = filter(lambda slot: slot is not None, availableSlot)
    return availableSlot

class AvailableSlotView(generics.ListAPIView):
    def list(self, request: Request, *args, **kwargs):
        user: User = request.user
        doctor: Doctor = user.doctor
        selected_date: datetime = datetime.strptime(request.query_params['date'], '%Y-%m-%d')
        availableSlot = caculateAvailableTimes(selected_date, doctor=doctor)
        response = format_response(
            success=True, status=200, data=availableSlot)
        return Response(data=response['data'], status=response['status'])

def partition(lst, n):
    division = len(lst) / n
    return [lst[round(division * i):round(division * (i + 1))] for i in range(n)]

def ranges(start, N, nb):
    return [(r.start, r.stop) for r in partition(range(start, N), nb)]

class SuggestHoursOfDoctorView(generics.RetrieveAPIView):
    
    permission_classes = [permissions.AllowAny]
    
    def _get_available_slots(self, list_of_meeting_times):
        # 1 ngày 24 tiếng = 1440 phút
        # Băm thành 1 set busy để tránh có những phút bị trùng
        # và các phần tử trong set mang giá trị True - bận, False - Rảnh
        # get the busy time
        busy = { t for meets in list_of_meeting_times
            for start,end in meets
            for t in range(start-start//100*40,end-end//100*40) }
        # get the free time in a day
        # print('busy', busy)
        free   = [t not in busy for t in range(1440)]
        # print('free', free)

        # Tìm khoảng nghỉ trong free bằng cách compare giá trị thứ k và k+1
        breaks = [i for i,(a,b) in enumerate(zip(free,free[1:]),1) if b!=a]
        
        # list ra các khoảng nghỉ xen kẽ trong 1 ngày
        result = [(s,e) for s,e in zip([0]+breaks,breaks+[1439]) if free[s]]
        # print('free', result)
        # trả về 1 mảng 2 chiều với phần tử có cấu trúc lần lượt là [<from>, <to>]
        return [[s+s//60*40,e+e//60*40] for s,e in result]
    
    def _format_slots(self, slots):
        
        def to_dict(slot: str):
            args = slot.split('-')
            return {
                'from': args[0],
                'to': args[1]
            }
        
        return map(to_dict, slots)
    
    def split_slots(self, shifts: list[WorkingShift]) -> list:
        periods = []
        interval = timedelta(minutes = 30)
        now = timezone.now()
        for shift in shifts:
            start = datetime.combine(now, shift.startTime)
            end = datetime.combine(now, shift.endTime)
            period_start = start
            while period_start < end:
                period_end = min(period_start + interval, end)
                periods.append((period_start, period_end))
                period_start = period_end
        
        periods = [ '{}-{}'.format(pstart.strftime("%H:%M"), pend.strftime("%H:%M")) for pstart, pend in periods ]
        
        return self._format_slots(periods)
    
    def split_slots2(self, bookedAt, estEndAt):
        return ranges(bookedAt, estEndAt, 5)

    def filter_slots(self, slots: list[list[int]]):
        periods = []
        interval = timedelta(minutes = 30)
        now = timezone.now()
        for (bookedAt, estEndAt) in slots:
            if estEndAt - bookedAt >= 30:
                start = datetime.combine(now, time(bookedAt//100, bookedAt%100))
                end = datetime.combine(now, time(estEndAt//100, estEndAt%100))
                period_start = start
                while period_start < end:
                    period_end = min(period_start + interval, end)
                    periods.append((period_start, period_end))
                    period_start = period_end
                    
        for index, (start, end) in enumerate(periods):
            if end - start < timedelta(minutes = 30):
                periods.pop(index)
        periods = [ '{}-{}'.format(pstart.strftime("%H:%M"), pend.strftime("%H:%M")) for pstart, pend in periods ]
        
        return self._format_slots(periods)

    def calculate_available_times(self, selected_date: datetime, doctor_id: int) -> list:
        logger.info('calculating available times')
        weekday = convert_weekday(selected_date)
        # print('day_of_week', weekday)
        schedules = Schedule.objects.filter(
            doctor_id = doctor_id,
            bookedAt__date = selected_date.date()
        )
        
        today_shifts = list(WorkingShift.objects.filter(
            doctor_id = doctor_id,
            weekday = weekday,
            isActive = True,
        ))
        
        if not schedules.exists():
            return self.split_slots(today_shifts)
        
        converted_schedules = [ (time_to_int(sc.bookedAt), time_to_int(sc.estEndAt)) for sc in schedules ]
        available_slots = self._get_available_slots([converted_schedules])
        
        # # get first slot (tuple)
        first_slot = available_slots[0]
        # # print(first_slot)
        # # get last slot (tuple)
        last_slot = available_slots[-1]
        
        earliest_shift = min(today_shifts, key = lambda shift: shift.startTime)
        latest_shift = max(today_shifts, key = lambda shift: shift.endTime)
        
        start_of_shift = time_to_int(earliest_shift.startTime)
        first_slot[0] = start_of_shift
        # last_time = time_to_int(latest_shift.startTime)
        last_slot[1] = time_to_int(latest_shift.endTime)
        
        if start_of_shift == first_slot[1]:
            available_slots.pop(0)
        # if last_slot[0] > last_time:
        #     available_slots.pop(-1)
        # else:
        #    last_slot[1] = time_to_int(latest_shift.endTime)
        # print('available slots before', available_slots)
        filtered_slots = self.filter_slots(available_slots)
        # print('filtered', list(filtered_slots))
        # convert_available_slots = ["-".join(f"{t//100:02}:{t%100:02}" for t in slot) for slot in available_slots]
        # print('converted', available_slots)
        
        return list(filtered_slots)
        
    
    def retrieve(self, request: Request, *args, **kwargs):
        doctor_id: int = kwargs.get('doctor_id')
        try:
            selected_date: datetime = datetime.strptime(request.query_params['date'], '%Y-%m-%d')
        except:
            response = format_response(
                success = True,
                status = 400,
                message = ResponseMessage.INVALID_INPUT,
                data = {
                    'date': 'Input date with format yyyy-MM-dd'
                }  
            )
            return Response(response, response['status'])
        
        available_slots = self.calculate_available_times(selected_date, doctor_id)
        # available_slots2 = caculateAvailableTimes(selected_date, doctor_id)
        
        response = format_response(
            success = True,
            status = 200,
            message = ResponseMessage.GET_DATA_SUCCEEDED,
            data = available_slots
        )
        
        return Response(response, response['status'])