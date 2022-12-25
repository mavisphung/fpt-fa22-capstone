import 'package:flutter/cupertino.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:get/get.dart';

import 'package:hi_doctor_v2/app/modules/appointment/controllers/booking/slots_creator.dart';
import 'package:hi_doctor_v2/app/modules/appointment/widgets/date_calendar.dart';
import 'package:hi_doctor_v2/app/modules/appointment/widgets/slots_skeleton.dart';
import 'package:hi_doctor_v2/app/common/util/extensions.dart';
import 'package:hi_doctor_v2/app/common/util/utils.dart';
import 'package:hi_doctor_v2/app/common/values/strings.dart';
import 'package:hi_doctor_v2/app/models/doctor.dart';
import 'package:hi_doctor_v2/app/modules/appointment/controllers/booking/booking_controller.dart';
import 'package:hi_doctor_v2/app/modules/appointment/models/working_hour_item.dart';
import 'package:hi_doctor_v2/app/modules/widgets/base_page.dart';
import 'package:hi_doctor_v2/app/modules/widgets/custom_bottom_sheet.dart';
import 'package:hi_doctor_v2/app/modules/appointment/widgets/hour_item.dart';
import 'package:hi_doctor_v2/app/modules/widgets/my_appbar.dart';
import 'package:hi_doctor_v2/app/modules/widgets/custom_title_section.dart';
import 'package:hi_doctor_v2/app/routes/app_pages.dart';
import 'package:intl/intl.dart';

// ignore: must_be_immutable
class BookingDateTimePage extends StatelessWidget {
  BookingDateTimePage({Key? key}) : super(key: key);

  final _cBooking = Get.put(BookingController());
  final _doctor = Get.arguments as Doctor;

  @override
  Widget build(BuildContext context) {
    _cBooking.setDoctor(_doctor);
    final slotsCreator = SlotsCreator(_doctor);
    return BasePage(
      appBar: const MyAppBar(
        title: 'Hẹn khám',
        actions: [BackHomeWidget()],
      ),
      bottomSheet: CustomBottomSheet(
        buttonText: Strings.kContinue,
        onPressed: () async {
          if (_cBooking.selectedTime.isEmpty) {
            Utils.showAlertDialog('Bạn cần chọn giờ bắt đầu cuộc hẹn.');
            return;
          }
          final bookDateTime = DateFormat('yyyy-MM-dd hh:mm:ss')
              .parse("${DateFormat('yyyy-MM-dd').format(_cBooking.selectedDate)} ${_cBooking.selectedTime}");
          final now = DateTime.now();
          final difference = bookDateTime.difference(now);
          if (difference.inDays < 1) {
            final isOk = await Utils.showConfirmDialog(
                'Bạn chỉ có thể được hoàn tiền khi hủy cuộc hẹn trước 1 ngày.\n\n Bạn có chắc muốn tiếp tục?');
            if (isOk == true) {
              Get.toNamed(Routes.BOOKING_PACKAGE);
              return;
            }
            return;
          }
          Get.toNamed(Routes.BOOKING_PACKAGE);
        },
      ),
      body: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          CustomTitleSection(
            title: 'Chọn ngày hẹn',
            paddingLeft: 8.sp,
          ),
          DateCalendar(cBooking: _cBooking),
          // -------------------------------------------------------------------------------
          CustomTitleSection(
            title: 'Chọn thời gian bắt đầu cuộc hẹn',
            paddingLeft: 8.sp,
          ),
          ObxValue<Rx<DateTime>>((data) {
            return FutureBuilder(
              future: slotsCreator.getAvailableSlot(data.value.getWeekday()),
              builder: (_, AsyncSnapshot<List<WorkingHour>?> snapshot) {
                if (snapshot.hasData && snapshot.data!.isNotEmpty) {
                  final slots = snapshot.data!;
                  return GridView.builder(
                    padding: EdgeInsets.only(bottom: 5.sp),
                    physics: const NeverScrollableScrollPhysics(),
                    shrinkWrap: true,
                    itemCount: slots.length,
                    gridDelegate: SliverGridDelegateWithMaxCrossAxisExtent(
                      crossAxisSpacing: 10.sp,
                      mainAxisSpacing: 20.sp,
                      maxCrossAxisExtent: 80.sp,
                      mainAxisExtent: 50.sp,
                    ),
                    itemBuilder: (_, int index) {
                      WorkingHour e = slots[index];
                      return GestureDetector(
                        onTap: () {
                          _cBooking.setSelectedTimeId(e.id!);
                          _cBooking.setSelectedTime(e.value!);
                        },
                        child: ObxValue<RxInt>(
                            (data) => HourItem(
                                  text: e.title!,
                                  id: e.id!,
                                  isSelected: data.value == e.id ? true : false,
                                ),
                            _cBooking.rxSelectedTimeId),
                      );
                    },
                  );
                } else if (snapshot.hasData && snapshot.data!.isEmpty) {
                  return const Center(child: Text('Bác sĩ không có lịch làm việc vào ngày này hoặc quá giờ đặt lịch.'));
                }
                return const SlotsSkeleton();
              },
            );
          }, _cBooking.rxSelectedDate),
          SizedBox(height: 90.sp),
        ],
      ),
    );
  }
}
