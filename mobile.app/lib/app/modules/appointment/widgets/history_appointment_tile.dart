import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:get/get.dart';

import 'package:hi_doctor_v2/app/common/util/extensions.dart';
import 'package:hi_doctor_v2/app/common/util/transformation.dart';
import 'package:hi_doctor_v2/app/common/util/utils.dart';
import 'package:hi_doctor_v2/app/common/values/colors.dart';
import 'package:hi_doctor_v2/app/models/appointment.dart';
import 'package:hi_doctor_v2/app/modules/appointment/widgets/appointment_tile.dart';
import 'package:hi_doctor_v2/app/modules/appointment/widgets/appointment_tile_button.dart';
import 'package:hi_doctor_v2/app/modules/widgets/custom_inkwell.dart';
import 'package:hi_doctor_v2/app/modules/widgets/image_container.dart';
import 'package:hi_doctor_v2/app/routes/app_pages.dart';

class HistoryAppointmentTile extends StatelessWidget {
  const HistoryAppointmentTile({
    Key? key,
    required this.data,
  }) : super(key: key);

  final Appointment data;

  Widget buildDay(String strDay) {
    DateTime now = DateTime.now(), theDay;
    try {
      theDay = DateTime.parse(strDay);
    } catch (e) {
      'Parsre day error'.debugLog('buildDay widget');
      theDay = now;
    }
    return theDay.day == now.day && theDay.month == now.month && theDay.year == now.year
        ? Text('Hôm nay | ${Utils.formatAMPM(theDay)}')
        : Text('${Utils.formatDate(theDay)} | Bắt đầu lúc ${Utils.formatAMPM(theDay)}');
  }

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: EdgeInsets.only(bottom: 10.sp),
      child: CustomInkWell(
        height: 180.sp,
        onTap: () {
          data.id != null
              ? Get.toNamed(Routes.MEETING_DETAIL, arguments: data.id)
              : Utils.showAlertDialog('Có lỗi xảy ra khi tải thông tin của cuộc hẹn.');
        },
        child: Column(
          children: [
            Row(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                ImageContainer(
                  width: 75,
                  height: 83,
                  imgUrl: data.doctor?['avatar'],
                ),
                SizedBox(
                  width: 7.sp,
                ),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        Tx.getDoctorName(data.doctor!["lastName"], data.doctor!["firstName"]),
                        overflow: TextOverflow.ellipsis,
                        softWrap: false,
                        style: TextStyle(
                          fontWeight: FontWeight.bold,
                          fontSize: 15.5.sp,
                        ),
                      ),
                      Container(
                        margin: EdgeInsets.symmetric(vertical: 8.sp),
                        child: Row(
                          children: [
                            Text(
                              data.category.toString().enumType.label,
                              style: TextStyle(
                                color: data.category == AppointmentType.online.value ? Colors.green : AppColors.primary,
                                fontSize: 12.sp,
                                fontWeight: FontWeight.w500,
                              ),
                            ),
                            Container(
                              margin: EdgeInsets.symmetric(horizontal: 5.sp),
                              width: 5.sp,
                              child: Divider(
                                thickness: 0.8.sp,
                              ),
                            ),
                            Expanded(
                              child: Container(
                                padding: EdgeInsets.symmetric(horizontal: 12.sp, vertical: 4.sp),
                                decoration: BoxDecoration(
                                  border: Border.all(
                                    color: appointmentStatusColors[data.status.toString().enumStatus]!,
                                    width: 1.6.sp,
                                  ),
                                  borderRadius: BorderRadius.circular(7.sp),
                                ),
                                child: Text(
                                  data.status.toString().enumStatus.label,
                                  textAlign: TextAlign.center,
                                  style: TextStyle(
                                    color: appointmentStatusColors[data.status.toString().enumStatus]!,
                                    fontSize: 12.sp,
                                    fontWeight: FontWeight.w500,
                                  ),
                                ),
                              ),
                            ),
                          ],
                        ),
                      ),
                      buildDay(data.bookedAt!),
                    ],
                  ),
                ),
              ],
            ),
            const Expanded(
              child: Divider(),
            ),
            SizedBox(
              width: double.infinity,
              child: AppointmentButton(
                onTap: () {
                  data.id != null
                      ? Get.toNamed(Routes.MEETING_DETAIL, arguments: data.id)
                      : Utils.showAlertDialog('Có lỗi xảy ra khi tải thông tin của cuộc hẹn.');
                },
                textColor: AppColors.primary,
                borderColor: AppColors.primary,
                label: 'Xem chi tiết',
              ),
            ),
          ],
        ),
      ),
    );
  }
}
