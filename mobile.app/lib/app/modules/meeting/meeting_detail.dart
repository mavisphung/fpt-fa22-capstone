import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:get/get.dart';
import 'package:hi_doctor_v2/app/modules/appointment/widgets/appointment_tile.dart';
import 'package:intl/intl.dart';
import 'package:permission_handler/permission_handler.dart';

import 'package:hi_doctor_v2/app/common/util/extensions.dart';
import 'package:hi_doctor_v2/app/common/values/strings.dart';
import 'package:hi_doctor_v2/app/modules/appointment/widgets/package_item.dart';
import 'package:hi_doctor_v2/app/modules/widgets/custom_bottom_sheet.dart';
import 'package:hi_doctor_v2/app/modules/meeting/views/service_tile.dart';
import 'package:hi_doctor_v2/app/modules/message/chat_page.dart';
import 'package:hi_doctor_v2/app/modules/widgets/info_container.dart';
import 'package:hi_doctor_v2/app/common/util/transformation.dart';
import 'package:hi_doctor_v2/app/common/util/utils.dart';
import 'package:hi_doctor_v2/app/modules/widgets/content_container.dart';
import 'package:hi_doctor_v2/app/modules/widgets/custom/doctor_card.dart';
import 'package:hi_doctor_v2/app/modules/widgets/custom_title_section.dart';
import 'package:hi_doctor_v2/app/modules/widgets/loading_widget.dart';
import 'package:hi_doctor_v2/app/modules/widgets/response_status_widget.dart';
import 'package:hi_doctor_v2/app/modules/meeting/controllers/meeting_controller.dart';
import 'package:hi_doctor_v2/app/modules/widgets/base_page.dart';
import 'package:hi_doctor_v2/app/modules/widgets/my_appbar.dart';
import 'package:hi_doctor_v2/app/routes/app_pages.dart';
import 'package:hi_doctor_v2/app/common/constants.dart';

class MeetingDetailPage extends StatelessWidget {
  final _cMeeting = Get.put(MeetingController());
  final _appointmentId = Get.arguments as int;

  MeetingDetailPage({super.key});

  Future<void> _onJoin() async {
    final micPermission = await Permission.microphone.request();
    final cameraPermission = await Permission.camera.request();
    if (micPermission.isGranted && cameraPermission.isGranted) {
      final channelEntry = await _cMeeting.getChannelEntry();
      if (channelEntry != null) {
        Get.toNamed(Routes.CHANNEL, arguments: channelEntry);
      }
    }
  }

  Map<String, String>? _getDateTimeMap(String str) {
    final dateTime = str.split(' ');
    final date = DateFormat('yyyy-MM-dd').parse(dateTime[0]);
    final now = DateTime.now();
    bool isToday = false;
    if (date.year == now.year && date.month == now.month && date.day == now.day) isToday = true;
    final time = Utils.parseStrToTime(dateTime[1]);
    if (time != null) {
      final formattedDate = Utils.formatDate(date);
      final endTime = time.add(const Duration(minutes: 30));
      return {
        'date': isToday ? 'Hôm nay' : formattedDate,
        'time': '${Utils.formatAMPM(time)} - ${Utils.formatAMPM(endTime)}',
      };
    }
    return null;
  }

  @override
  Widget build(BuildContext context) {
    print('APPOINTMENT ID: $_appointmentId');
    return BasePage(
      paddingBottom: 30.sp,
      appBar: MyAppBar(
        title: 'Chi tiết cuộc hẹn',
        actions: [
          PopupMenuButton<int>(
            tooltip: '',
            padding: EdgeInsets.zero,
            onSelected: (_) async {
              'Cancelling appointment'.debugLog('Cancellation');
              final isOk = await Utils.showConfirmDialog('Bạn có chắc là muốn hủy cuộc hẹn này không?');
              if (isOk == null || !isOk) {
                return;
              }
              Get.toNamed(Routes.CANCEL, arguments: {
                'appId': _appointmentId,
              });
            },
            itemBuilder: (context) => <PopupMenuEntry<int>>[
              const PopupMenuItem<int>(
                value: 0,
                child: Text('Hủy cuộc hẹn'),
              ),
            ],
          )
        ],
      ),
      body: FutureBuilder(
        future: _cMeeting.getAppointmentDetail(_appointmentId),
        builder: (_, AsyncSnapshot<bool?> snapshot) {
          if (snapshot.hasData && snapshot.data == true) {
            final doctor = _cMeeting.appointment.doctor;
            final patient = _cMeeting.appointment.patient;
            final package = _cMeeting.appointment.package;
            final dateTimeMap = _getDateTimeMap(_cMeeting.appointment.bookedAt!);
            final isNotHistory = _cMeeting.appointment.status == AppointmentStatus.pending.value ||
                _cMeeting.appointment.status == AppointmentStatus.inProgress.value;
            return Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                DoctorCard(
                  avatar: doctor?['avatar'],
                  firstName: doctor?['firstName'],
                  lastName: doctor?['lastName'],
                  specialist: Tx.getGender(doctor?['gender']),
                  address: doctor?['address'],
                ),
                Row(
                  crossAxisAlignment: CrossAxisAlignment.end,
                  children: [
                    Padding(
                      padding: EdgeInsets.only(left: 5.sp, right: 26.sp, top: 20.sp),
                      child: Text(
                        'Trạng thái',
                        style: TextStyle(
                          fontSize: 15.sp,
                          fontWeight: FontWeight.w500,
                        ),
                      ),
                    ),
                    Container(
                      padding: EdgeInsets.symmetric(horizontal: 12.sp, vertical: 4.sp),
                      decoration: BoxDecoration(
                        border: Border.all(
                          color: appointmentStatusColors[_cMeeting.appointment.status.toString().enumStatus]!,
                          width: 1.sp,
                        ),
                        borderRadius: BorderRadius.circular(5.sp),
                      ),
                      child: Text(
                        _cMeeting.appointment.status.toString().enumStatus.label,
                        textAlign: TextAlign.center,
                        style: TextStyle(
                          color: appointmentStatusColors[_cMeeting.appointment.status.toString().enumStatus]!,
                          fontSize: 12.sp,
                          fontWeight: FontWeight.w500,
                        ),
                      ),
                    ),
                  ],
                ),
                const ContentTitle1(title: 'Thông tin lịch hẹn'),
                ContentRow(
                  labelWidth: 100,
                  hozPadding: 5,
                  content: {
                    'Ngày hẹn': '${dateTimeMap?["date"]}',
                    'Giờ hẹn': '${dateTimeMap?["time"]}',
                  },
                ),
                CustomTitleSection(
                  paddingLeft: 5,
                  paddingTop: 20,
                  paddingBottom: 0,
                  title: 'Thông tin bệnh nhân',
                  suffixText: 'Xem ảnh',
                  suffixAction: () =>
                      Get.toNamed(Routes.IMAGE, arguments: patient?['avatar'] ?? Constants.defaultAvatar),
                ),
                ContentRow(
                  labelWidth: 100,
                  hozPadding: 5,
                  content: {
                    'Họ tên': Tx.getFullName(patient?['lastName'], patient?['firstName']),
                    'Tuổi': Tx.getAge(patient?['dob']),
                    'Địa chỉ': patient?['address'],
                  },
                ),
                const ContentTitle1(title: 'Thông tin gói dịch vụ'),
                ContentRow(
                  labelWidth: 100,
                  hozPadding: 5,
                  content: {
                    'Tên dịch vụ': package?['name'],
                    'Mô tả': package?['description'],
                    'Giá dịch vụ': '${Tx.formatPrice(package?['price'])} VNĐ',
                    'Loại khám': _cMeeting.appointment.category!.toString().enumType.label,
                  },
                ),
                if (_cMeeting.appointment.category == CategoryType.ONLINE.name && isNotHistory)
                  Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const InfoContainer(info: 'Dịch vụ chỉ được mở trong thời gian cuộc hẹn.', hasInfoIcon: true),
                      ServiceTile(
                        bookedAt: _cMeeting.appointment.bookedAt!,
                        chatPageArgs: ChatPageArguments(
                          peerId: doctor?['id'],
                          peerAccountId: doctor?['accountId'],
                          peerName: Tx.getDoctorName(doctor?['lastName'], doctor?['firstName']),
                          peerAvatar: doctor?['avatar'] ?? Constants.defaultAvatar,
                          hasInputWidget: true,
                        ),
                        onJoin: _onJoin,
                      ),
                    ],
                  ),
                if (_cMeeting.appointment.category != 'ONLINE' || !isNotHistory) SizedBox(height: 50.sp),
              ],
            );
          } else if (snapshot.hasData && snapshot.data == false) {
            return const SystemErrorWidget();
          } else if (snapshot.connectionState == ConnectionState.none) {
            return const NoInternetWidget2();
          }
          return const LoadingWidget(topPadding: 200);
        },
      ),
      bottomSheet: ObxValue<RxBool>(
        (data) {
          if (data.value == true) {
            if (_cMeeting.appointment.status == AppointmentStatus.pending.value ||
                _cMeeting.appointment.status == AppointmentStatus.inProgress.value) {
              return _cMeeting.appointment.category == 'ONLINE'
                  ? const SizedBox.shrink()
                  : CustomBottomSheet(
                      buttonText: Strings.checkIn,
                      onPressed: () => Get.toNamed(Routes.QR_SCANNER),
                    );
            }
            return CustomBottomSheet(
              buttonText: 'Đánh giá',
              onPressed: () {},
            );
          }
          return const SizedBox.shrink();
        },
        _cMeeting.isAppointmentLoaded,
      ),
    );
  }
}
