import 'package:get/get.dart';

import 'package:hi_doctor_v2/app/common/util/utils.dart';
import 'package:hi_doctor_v2/app/models/doctor.dart';
import 'package:hi_doctor_v2/app/modules/appointment/controllers/booking/booking_controller.dart';
import 'package:hi_doctor_v2/app/modules/appointment/models/working_hour_item.dart';

class SlotsCreator {
  final Doctor doctor;
  final _cBooking = Get.find<BookingController>();
  final _now = DateTime.now();

  final List<Map<String, dynamic>> _selectedWeekdayShifts = <Map<String, dynamic>>[];

  SlotsCreator(this.doctor);

  List<Map<String, dynamic>> _getWeekdayShift(int weekday) {
    _selectedWeekdayShifts.clear();
    for (var shift in doctor.shifts!) {
      if (shift['isActive'] == true && shift['weekday'] == weekday) {
        _selectedWeekdayShifts.add(shift);
      }
    }
    return _selectedWeekdayShifts;
  }

  Future<List<WorkingHour>?> getAvailableSlot(int weekDay) async {
    // return null;
    List<WorkingHour> slots = [];
    final selectedDate = _cBooking.selectedDate;
    final dateStr = '${selectedDate.year}-${selectedDate.month}-${selectedDate.day}';
    String start, end;
    DateTime? startTime, endTime;
    int id = 1;
    // --------------------------------

    final suggestShifts = await _cBooking.getSuggestHours();
    print('SUGGEST: ${suggestShifts.toString()}');

    if (suggestShifts != null && suggestShifts.isNotEmpty) {
      for (var shift in suggestShifts) {
        start = shift['from'] as String;
        end = shift['to'] as String;
        startTime = Utils.parseStrToDateTime('$dateStr $start');
        print('suggest startTime: $startTime');
        endTime = Utils.parseStrToDateTime('$dateStr $end');
        print('suggest endTime: $endTime');
        if (startTime != null && endTime != null) {
          DateTime endSlot;

          endSlot = startTime;
          do {
            final isTimeAfter = endSlot.isAfter(_now);
            if (isTimeAfter) {
              slots.add(WorkingHour(
                id: id++,
                title: Utils.formatAMPM(endSlot),
                value: '${Utils.formatHHmmTime(endSlot)}:00',
              ));
            }
            endSlot = DateTime(selectedDate.year, selectedDate.month, selectedDate.day, endSlot.hour, endSlot.minute)
                .add(const Duration(minutes: 30));
          } while (endSlot.isBefore(endTime));
        }
      }
      return slots;
    }

    // --------------------------------
    final listShift = doctor.shifts;
    if (listShift == null || listShift.isEmpty) {
      return null;
    }
    final shifts = _getWeekdayShift(weekDay);

    if (shifts.isEmpty) return List.empty();

    print('ALL SHIFTS: ${shifts.toString()}');

    for (var shift in shifts) {
      print('SHIFT: ${shift.toString()}');
      start = shift['startTime'] as String;
      end = shift['endTime'] as String;
      startTime = Utils.parseStrToDateTime('$dateStr $start');
      print('startTime: $startTime');
      endTime = Utils.parseStrToDateTime('$dateStr $end');
      print('endTime: $endTime');
      if (startTime != null && endTime != null) {
        DateTime endSlot;

        endSlot = startTime;
        do {
          print('endSlot 1: $endSlot');
          final isTimeAfter = endSlot.isAfter(_now);
          if (isTimeAfter) {
            slots.add(WorkingHour(
              id: id++,
              title: Utils.formatAMPM(endSlot),
              value: '${Utils.formatHHmmTime(endSlot)}:00',
            ));
          }
          endSlot = DateTime(selectedDate.year, selectedDate.month, selectedDate.day, endSlot.hour, endSlot.minute)
              .add(const Duration(minutes: 30));
          print('endSlot 2: $endSlot');
        } while (endSlot.isBefore(endTime));
      }
    }
    return slots;
  }
}
