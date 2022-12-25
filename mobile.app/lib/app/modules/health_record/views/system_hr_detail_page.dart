import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:hi_doctor_v2/app/common/constants.dart';
import 'package:hi_doctor_v2/app/common/util/transformation.dart';
import 'package:hi_doctor_v2/app/common/util/utils.dart';

import 'package:hi_doctor_v2/app/modules/health_record/controllers/health_record_controller.dart';
import 'package:hi_doctor_v2/app/modules/health_record/widgets/diagnose_container.dart';
import 'package:hi_doctor_v2/app/modules/health_record/widgets/instructions_container.dart';
import 'package:hi_doctor_v2/app/modules/health_record/widgets/prescriptions_container.dart';
import 'package:hi_doctor_v2/app/modules/widgets/base_page.dart';
import 'package:hi_doctor_v2/app/modules/widgets/content_container.dart';
import 'package:hi_doctor_v2/app/modules/widgets/custom_title_section.dart';
import 'package:hi_doctor_v2/app/modules/widgets/loading_widget.dart';
import 'package:hi_doctor_v2/app/modules/widgets/my_appbar.dart';
import 'package:hi_doctor_v2/app/modules/widgets/response_status_widget.dart';
import 'package:hi_doctor_v2/app/routes/app_pages.dart';

class SystemHrDetailPage extends StatelessWidget {
  final _cHealthRecord = Get.find<HealthRecordController>();
  final recordId = Get.arguments as int?;

  SystemHrDetailPage({super.key});

  @override
  Widget build(BuildContext context) {
    return BasePage(
      backgroundColor: Colors.white,
      appBar: const MyAppBar(title: 'Chi tiết hồ sơ'),
      body: recordId != null
          ? FutureBuilder(
              future: _cHealthRecord.getHrWithId(recordId!),
              builder: (_, AsyncSnapshot<bool?> snapshot) {
                if (snapshot.hasData && snapshot.data == true) {
                  if (_cHealthRecord.systemHrResModel != null) {
                    final record = _cHealthRecord.systemHrResModel!.record!;
                    final patient = _cHealthRecord.systemHrResModel!.patient!;
                    final doctor = _cHealthRecord.systemHrResModel!.doctor!;
                    final supervisor = _cHealthRecord.systemHrResModel!.supervisor!;
                    final detail = _cHealthRecord.systemHrResModel!.detail!;
                    final diseases = detail['diseases'] as List;
                    final prescriptions = detail['prescriptions'] as List;
                    final instructions = detail['instructions'] as List;
                    return Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        const ContentTitle1(title: 'Thông tin hồ sơ', topPadding: 0),
                        ContentContainer(
                          labelWidth: 70,
                          hozPadding: 12,
                          content: {
                            'Mã hồ sơ': '${record["name"]}',
                            'Ngày tạo': Utils.reverseDate(record["createdAt"]),
                          },
                        ),
                        const ContentTitle1(title: 'Thông tin bác sĩ'),
                        ContentContainer(
                          labelWidth: 70,
                          hozPadding: 12,
                          content: {
                            'Họ tên': Tx.getDoctorName(doctor['lastName'], doctor['firstName']),
                          },
                        ),
                        CustomTitleSection(
                          paddingLeft: 12,
                          paddingTop: 20,
                          paddingBottom: 0,
                          title: 'Thông tin bệnh nhân',
                          suffixText: 'Xem ảnh',
                          suffixAction: () =>
                              Get.toNamed(Routes.IMAGE, arguments: patient['avatar'] ?? Constants.defaultAvatar),
                        ),
                        ContentContainer(
                          labelWidth: 70,
                          hozPadding: 12,
                          content: {
                            'Họ tên': Tx.getFullName(patient['lastName'], patient['firstName']),
                            'Tuổi': Tx.getAge(patient['dob']),
                            'Giới tính': Tx.getGender(patient['gender']),
                          },
                        ),
                        const ContentTitle1(title: 'Thông tin người giám hộ'),
                        ContentContainer(
                          labelWidth: 70,
                          hozPadding: 12,
                          content: {
                            'Họ tên': Tx.getFullName(supervisor['lastName'], supervisor['firstName']),
                          },
                        ),
                        if (diseases.isNotEmpty) DiagnoseContainer(diagnoses: diseases),
                        if (prescriptions.isNotEmpty) PrescriptionContainer(prescriptions: prescriptions),
                        if (instructions.isNotEmpty) InstructionContainer(instructions: instructions),
                      ],
                    );
                  }
                  return const SystemErrorWidget();
                } else if (snapshot.data == false) {
                  return const SystemErrorWidget();
                } else if (snapshot.connectionState == ConnectionState.none) {
                  return const NoInternetWidget2();
                }
                return const LoadingWidget();
              },
            )
          : const SizedBox.shrink(),
    );
  }
}
